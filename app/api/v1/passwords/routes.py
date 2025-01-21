from flask import Blueprint, jsonify, request
from app.models import Password
from app import db
from app.api.v1.auth.utils import token_required

# Define the Blueprint
passwords_bp = Blueprint('passwords', __name__)

@passwords_bp.route('/passwords', methods=['GET'])
@token_required
def get_passwords(current_user):
    try:
        passwords = Password.query.filter_by(user_id=current_user.id).all()
        return jsonify([{
            'id': p.id,
            'title': p.title,
            'url': p.url,
            'username': p.username,
            'encrypted_password': p.encrypted_password,
            'created_at': p.created_at.isoformat()
        } for p in passwords])
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@passwords_bp.route('/passwords', methods=['POST'])
@token_required
def create_password(current_user):
    try:
        data = request.get_json()
        password = Password(
            title=data['title'],
            url=data['url'],
            username=data['username'],
            encrypted_password=data['encrypted_password'],
            user_id=current_user.id
        )
        
        db.session.add(password)
        db.session.commit()
        
        return jsonify({
            'message': 'Password created successfully',
            'password': {
                'id': password.id,
                'title': password.title,
                'url': password.url,
                'username': password.username
            }
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400