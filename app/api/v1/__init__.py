from flask import Blueprint

# Create the main API v1 blueprint
api_v1_bp = Blueprint('api_v1', __name__, url_prefix='/api/v1')

# Alias for backward compatibility (if needed)
bp = api_v1_bp

# Import and register sub-blueprints
from .auth import auth_bp
from .passwords import passwords_bp
from .users import users_bp

api_v1_bp.register_blueprint(auth_bp, url_prefix='/auth')
api_v1_bp.register_blueprint(passwords_bp, url_prefix='/passwords')
api_v1_bp.register_blueprint(users_bp, url_prefix='/users')