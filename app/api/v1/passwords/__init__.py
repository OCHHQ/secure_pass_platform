from flask import Blueprint

passwords_bp = Blueprint('passwords', __name__)

from app.api.v1.passwords import routes