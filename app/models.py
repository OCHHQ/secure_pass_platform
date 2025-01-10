from . import db, login_manager
from flask_login import UserMixin
from cryptography.fernet import Fernet, InvalidToken
import os
from base64 import urlsafe_b64encode
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Get secret key from environment
SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    raw_key = Fernet.generate_key()
    SECRET_KEY = raw_key.decode()
    with open('.env', 'a') as f:
        f.write(f'\nSECRET_KEY={SECRET_KEY}')
else:
    raw_key = SECRET_KEY.encode()

f = Fernet(urlsafe_b64encode(raw_key[:32]))

def encrypt_password(password):
    """Encrypt a password using Fernet symmetric encryption."""
    if isinstance(password, str):
        password = password.encode()
    return f.encrypt(password)

def decrypt_password(encrypted_password):
    """Decrypt an encrypted password using Fernet symmetric encryption."""
    try:
        return f.decrypt(encrypted_password).decode()
    except (InvalidToken, TypeError):
        return None

class User(UserMixin, db.Model):
    """User model for authentication and password management."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    totp_secret = db.Column(db.String(32), nullable=True)  # For 2FA
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)

    def set_password(self, password):
        """Hash and set the user's password."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Verify the user's password."""
        return check_password_hash(self.password, password)

class Password(db.Model):
    """Model for storing user passwords."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    site_name = db.Column(db.String(150), nullable=False)
    site_url = db.Column(db.String(200), nullable=True)
    site_password = db.Column(db.String(200), nullable=False)
    strength = db.Column(db.String(20), default='weak')  # Password strength: weak, medium, strong
    last_modified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    expiry_date = db.Column(db.DateTime, nullable=True)  # Optional expiry date for the password
    user = db.relationship('User', backref=db.backref('passwords', lazy=True))


    def set_password(self, password):
        """Encrypt and set the site password."""
        self.site_password = encrypt_password(password)

    def get_password(self):
        """Decrypt and return the site password."""
        return decrypt_password(self.site_password)

class SharedPassword(db.Model):
    """Model for managing shared passwords."""
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(200), unique=True, nullable=False)
    expiry_time = db.Column(db.DateTime, nullable=False)
    is_used = db.Column(db.Boolean, default=False, nullable=False)
    password_id = db.Column(db.Integer, db.ForeignKey('password.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref=db.backref('shared_passwords', lazy=True))
    password = db.relationship('Password', backref=db.backref('shared_passwords', lazy=True))

class PasswordHistory(db.Model):
    """Model for tracking password-related actions (e.g., creation, editing, sharing)."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action = db.Column(db.String(50), nullable=False)  # e.g., 'create', 'edit', 'share', 'view'
    site_name = db.Column(db.String(150), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref=db.backref('password_history', lazy=True))

@login_manager.user_loader
def load_user(user_id):
    """Load a user by ID for Flask-Login."""
    return User.query.get(int(user_id))