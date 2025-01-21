from flask import Blueprint

vaults_bp = Blueprint('vaults', __name__)

from . import routes