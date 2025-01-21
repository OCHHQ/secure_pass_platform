# app/extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate

# Initialize extensions
db: SQLAlchemy = SQLAlchemy()
"""SQLAlchemy instance for database management."""

bcrypt: Bcrypt = Bcrypt()
"""Bcrypt instance for password hashing."""

login_manager: LoginManager = LoginManager()
"""LoginManager instance for user session management."""

migrate: Migrate = Migrate()
"""Migrate instance for database migrations."""