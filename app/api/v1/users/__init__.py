# app/api/v1/users/__init__.py
from flask import Blueprint

users_bp = Blueprint('users', __name__)

from app.api.v1.users import routes