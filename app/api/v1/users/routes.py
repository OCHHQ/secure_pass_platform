# app/api/v1/users/routes.py
from flask import jsonify, request, Blueprint
from app.models import User
from app import db
from app.api.v1.auth.utils import token_required

# Define the Blueprint
users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['GET'])
@token_required
def get_all_users(current_user):
    """
    Get all users.
    """
    users = User.query.all()
    users_list = [{
        'id': user.id,
        'username': user.username,
        'email': user.email
    } for user in users]
    return jsonify(users_list)

@users_bp.route('/me', methods=['GET'])
@token_required
def get_current_user(current_user):
    """
    Get the current authenticated user.
    """
    return jsonify({
        'id': current_user.id,
        'username': current_user.username,
        'email': current_user.email
    })

@users_bp.route('/me', methods=['PUT'])
@token_required
def update_user(current_user):
    """
    Update the current authenticated user.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        if 'username' in data:
            current_user.username = data['username']
        if 'email' in data:
            current_user.email = data['email']
        if 'password' in data:
            current_user.set_password(data['password'])

        db.session.commit()

        return jsonify({
            'message': 'Profile updated successfully',
            'user': {
                'id': current_user.id,
                'username': current_user.username,
                'email': current_user.email
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@users_bp.route('/<int:user_id>', methods=['GET'])
@token_required
def get_user_by_id(current_user, user_id):
    """
    Get a specific user by ID.
    """
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email
    })