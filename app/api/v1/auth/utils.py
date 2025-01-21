# app/api/v1/auth/utils.py
from functools import wraps
import uuid
from flask import jsonify, request, g, current_app
import jwt
from datetime import datetime, timedelta
import redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Lazy import to avoid circular dependencies
def get_user_model():
    from app.models import User
    return User

def generate_auth_token(user_id):
    """Generate a JWT token for the user
    
    Args:
        user_id: The ID of the user to generate a token for
        
    Returns:
        str: The generated JWT token, or None if generation fails
    """
    try:
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(days=1),
            'iat': datetime.utcnow(),
            'jti': str(uuid.uuid4())  # Add unique token ID for blacklisting
        }
        return jwt.encode(
            payload,
            current_app.config.get('JWT_SECRET_KEY') or current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
    except Exception as e:
        current_app.logger.error(f"Token generation failed: {str(e)}")
        return None

def verify_auth_token(token):
    """Verify and decode a JWT token
    
    Args:
        token: The JWT token to verify
        
    Returns:
        dict: The decoded payload if valid, None otherwise
    """
    try:
        return jwt.decode(
            token,
            current_app.config.get('JWT_SECRET_KEY') or current_app.config['SECRET_KEY'],
            algorithms=['HS256']
        )
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
        current_app.logger.warning(f"Token verification failed: {str(e)}")
        return None

def get_current_user():
    """Retrieve the current user from the Authorization header token
    
    Returns:
        User: The current user object if found and token is valid, None otherwise
    """
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None

    try:
        token = auth_header.split(' ')[1]
        payload = verify_auth_token(token)
        if payload:
            User = get_user_model()
            return User.query.get(payload['user_id'])
    except Exception as e:
        current_app.logger.error(f"Error retrieving current user: {str(e)}")
        return None
    
def admin_required(f):
    """Decorator to ensure the current user has admin privileges
    
    This decorator should be used after @token_required to ensure
    g.current_user is available.
    
    Args:
        f: The function to decorate
        
    Returns:
        function: The decorated function that checks for admin status
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            if not hasattr(g, 'current_user'):
                return jsonify({'error': 'Authentication required'}), 401
                
            if not g.current_user.is_admin:
                return jsonify({'error': 'Admin privileges required'}), 403
                
            return f(*args, **kwargs)
            
        except Exception as e:
            current_app.logger.error(f"Admin verification error: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500
            
    return decorated

def token_required(f):
    """Decorator to protect routes with JWT authentication
    
    Args:
        f: The function to decorate
        
    Returns:
        function: The decorated function that checks for valid JWT token
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({'error': 'Authorization header is missing'}), 401

        if not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Invalid token format'}), 401

        try:
            token = auth_header.split(' ')[1]
            payload = verify_auth_token(token)
            
            if not payload:
                return jsonify({'error': 'Invalid or expired token'}), 401
            
            User = get_user_model()
            g.current_user = User.query.get(payload['user_id'])
            
            if not g.current_user:
                return jsonify({'error': 'User not found'}), 401

        except Exception as e:
            current_app.logger.error(f"Authentication error: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500

        return f(*args, **kwargs)
    return decorated

# Optional: Add rate limiting decorator
def rate_limit(limit=100, per=60):
    """Rate limiting decorator for API endpoints
    
    Args:
        limit: Maximum number of requests allowed
        per: Time period in seconds
        
    Returns:
        function: Decorated function with rate limiting
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            key = f"rate_limit_{request.remote_addr}_{f.__name__}"
            try:
                current_usage = redis_client.get(key)
                if current_usage is None:
                    redis_client.setex(key, per, 1)
                elif int(current_usage) >= limit:
                    return jsonify({'error': 'Rate limit exceeded'}), 429
                else:
                    redis_client.incr(key)
            except Exception as e:
                current_app.logger.error(f"Rate limiting error: {str(e)}")
                # Fail open if Redis is unavailable
                pass
            return f(*args, **kwargs)
        return decorated_function
    return decorator