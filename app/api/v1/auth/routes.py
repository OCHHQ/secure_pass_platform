from flask import jsonify, request, g
from . import auth_bp
from app.models import User, db
from app.extensions import bcrypt
from .utils import generate_auth_token, token_required
import logging
from flask_cors import cross_origin

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    logger.info(f"Received registration data: {data}")  # Log the received data

    if not data:
        return jsonify({'status': 'error', 'message': 'No input data provided'}), 400

    # Validate required fields
    required_fields = ['username', 'email', 'password']
    if not all(field in data for field in required_fields):
        return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400

    try:
        # Check if email is already registered
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'status': 'error', 'message': 'Email already registered'}), 409

        # Hash the password
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

        # Create a new user
        new_user = User(
            username=data['username'],
            email=data['email'],
            password=hashed_password
        )

        # Save the user to the database
        db.session.add(new_user)
        db.session.commit()

        # Generate a token for the new user
        token = generate_auth_token(new_user.id)

        # Return success response
        return jsonify({
            'status': 'success',
            'message': 'Registration successful',
            'data': {
                'token': token,
                'user': {
                    'id': new_user.id,
                    'username': new_user.username,
                    'email': new_user.email
                }
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error during registration: {e}")  # Log the error
        return jsonify({'status': 'error', 'message': str(e)}), 500

@auth_bp.route('/login', methods=['POST', 'OPTIONS'])
@cross_origin()
def login():
    # Handle OPTIONS request (preflight)
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'success'})
        return response

    data = request.get_json()
    logger.info(f"Received login data: {data}")

    if not data:
        logger.warning("No input data provided for login")
        return jsonify({
            'status': 'error',
            'message': 'No input data provided'
        }), 400

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        logger.warning("Email or password missing in login request")
        return jsonify({
            'status': 'error',
            'message': 'Email and password are required'
        }), 400

    try:
        # Find the user by email
        user = User.query.filter_by(email=email).first()

        # Check if the user exists and the password is correct
        if user and bcrypt.check_password_hash(user.password, password):
            # Generate a token for the user
            token = generate_auth_token(user.id)

            # Log successful login
            logger.info(f"User {user.email} logged in successfully")

            response = jsonify({
                'status': 'success',
                'message': 'Login successful',
                'data': {
                    'token': token,
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email
                    }
                }
            })
            
            # Set CORS headers explicitly
            response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            return response, 200

        # If user doesn't exist or password is incorrect
        logger.warning(f"Invalid login attempt for email: {email}")
        return jsonify({
            'status': 'error',
            'message': 'Invalid email or password'
        }), 401

    except Exception as e:
        logger.error(f"Error during login: {e}", exc_info=True)
        return jsonify({
            'status': 'error',
            'message': 'An internal error occurred. Please try again later.'
        }), 500
    
@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout():
    try:
        # Optionally, you can blacklist the token here if needed
        # For now, we'll rely on the client to clear the token
        return jsonify({
            'status': 'success',
            'message': 'Logged out successfully'
        }), 200
    except Exception as e:
        logger.error(f"Error during logout: {e}")  # Log the error
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@auth_bp.route('/me', methods=['GET'])
@token_required
def get_current_user():
    try:
        # Return the current user's details
        return jsonify({
            'status': 'success',
            'data': {
                'user': {
                    'id': g.current_user.id,
                    'username': g.current_user.username,
                    'email': g.current_user.email
                }
            }
        }), 200
    except Exception as e:
        logger.error(f"Error fetching current user: {e}")  # Log the error
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500