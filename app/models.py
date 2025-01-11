from . import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from enum import Enum
import zxcvbn
import secrets
import os
from base64 import urlsafe_b64encode

class User(UserMixin, db.Model):
    """User model for authentication and password management."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False, index=True)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password = db.Column(db.String(200), nullable=False)
    totp_secret = db.Column(db.String(32), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    failed_login_attempts = db.Column(db.Integer, default=0)
    account_locked_until = db.Column(db.DateTime, nullable=True)

    def set_password(self, password):
        """Hash and set the user's password with strength validation."""
        strength_result = zxcvbn.zxcvbn(password)
        
        if strength_result['score'] < 3:
            suggestions = strength_result['feedback']['suggestions']
            raise ValueError(f"Password too weak. Suggestions: {', '.join(suggestions)}")
            
        # Use stronger hashing method
        self.password = generate_password_hash(password, method='pbkdf2:sha256:260000')

    def check_password(self, password):
        """Verify the user's password."""
        return check_password_hash(self.password, password)

    def generate_totp_secret(self):
        """Generate a new TOTP secret for 2FA."""
        self.totp_secret = secrets.token_hex(16)
        return self.totp_secret

class Password(db.Model):
    """Model for storing user passwords."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_password_user_id', ondelete='CASCADE'), nullable=False, index=True)
    site_name = db.Column(db.String(150), nullable=False, index=True)
    site_url = db.Column(db.String(200), nullable=True)
    site_password = db.Column(db.String(200), nullable=False)
    strength = db.Column(db.String(20), default='weak')
    last_modified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    expiry_date = db.Column(db.DateTime, nullable=True)
    
    user = db.relationship('User', backref=db.backref('passwords', lazy=True, cascade='all, delete-orphan'))

    def set_password(self, password):
        """Hash and store the site password."""
        # For stored site passwords, we'll use the same secure hashing
        self.site_password = generate_password_hash(password, method='pbkdf2:sha256:260000')
        self.strength = self.calculate_strength(password)

    def verify_password(self, password):
        """Verify the stored site password."""
        return check_password_hash(self.site_password, password)

    @staticmethod
    def calculate_strength(password):
        """Calculate password strength using zxcvbn."""
        result = zxcvbn.zxcvbn(password)
        strengths = ['very weak', 'weak', 'medium', 'strong', 'very strong']
        return strengths[result['score']]

class SharedPassword(db.Model):
    """Model for managing shared passwords."""
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(200), unique=True, nullable=False, index=True)
    expiry_time = db.Column(db.DateTime, nullable=False)
    is_used = db.Column(db.Boolean, default=False, nullable=False)
    password_id = db.Column(db.Integer, db.ForeignKey('password.id', ondelete='CASCADE'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    password = db.relationship('Password', backref='shared_passwords')
    user = db.relationship('User', backref='shared_passwords')

    @staticmethod
    def generate_share_token():
        """Generate a cryptographically secure token for sharing."""
        return secrets.token_urlsafe(32)

    def is_valid(self):
        """Check if the share is still valid."""
        return (
            datetime.utcnow() < self.expiry_time and
            not self.is_used and
            self.password_id is not None
        )
    
class PasswordHistory(db.Model):
    """Model for tracking password-related actions."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True)
    action = db.Column(db.String(20), nullable=False)
    site_name = db.Column(db.String(150), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    ip_address = db.Column(db.String(45), nullable=True)  # Store IP for audit

@login_manager.user_loader
def load_user(user_id):
    """Load a user by ID for Flask-Login."""
    return User.query.get(int(user_id))