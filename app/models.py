from . import db, login_manager
from flask_login import UserMixin
from cryptography.fernet import Fernet, InvalidToken
import os
from base64 import urlsafe_b64encode

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
    if isinstance(password, str):
        password = password.encode()
    return f.encrypt(password)

def decrypt_password(encrypted_password):
    try:
        return f.decrypt(encrypted_password).decode()
    except (InvalidToken, TypeError):
        return None

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Password(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    site_name = db.Column(db.String(150), nullable=False)
    site_url = db.Column(db.String(200), nullable=False)
    site_password = db.Column(db.String(200), nullable=False)
    user = db.relationship('User', backref=db.backref('passwords', lazy=True))

class SharedPassword(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(200), unique=True, nullable=False)  # Add this field
    expiry_time = db.Column(db.DateTime, nullable=False)
    is_used = db.Column(db.Boolean, default=False, nullable=False) 
    password_id = db.Column(db.Integer, db.ForeignKey('password.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('shared_passwords', lazy=True))
    password = db.relationship('Password', backref=db.backref('shared_passwords', lazy=True))
    

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))