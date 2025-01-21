from flask import Flask
from dotenv import load_dotenv
import os
import logging
from app.extensions import db, bcrypt, login_manager, migrate
from flask_cors import CORS
from flask import jsonify, request

# Load environment variables from .env
load_dotenv()

def create_app():
    app = Flask(__name__)

    # Load configuration from config.py
    app.config.from_object('config.Config')

    # Initialize extensions with the app
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Configure login manager
    login_manager.login_view = 'main.login'
    login_manager.login_message_category = 'info'

    # Initialize CORS with more permissive settings for development
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:5173').split(',')
    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": CORS_ORIGINS,
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
                "allow_headers": [
                    "Content-Type",
                    "Authorization",
                    "Access-Control-Allow-Credentials",
                    "Access-Control-Allow-Headers",
                    "Access-Control-Allow-Methods",
                    "Access-Control-Allow-Origin",
                    "Origin",
                    "Accept",
                    "X-Requested-With"
                ],
                "expose_headers": [
                    "Content-Type",
                    "Authorization",
                    "Access-Control-Allow-Credentials",
                    "Access-Control-Allow-Headers",
                    "Access-Control-Allow-Methods",
                    "Access-Control-Allow-Origin"
                ],
                "supports_credentials": True,
                "max_age": 600  # Cache preflight requests for 10 minutes
            }
        }
    )

    # Add CORS headers to all responses
    @app.after_request
    def after_request(response):
        # Get the origin from the request headers
        origin = request.headers.get('Origin')
        
        # If the origin is in our allowed origins, set the CORS headers
        if origin in CORS_ORIGINS:
            response.headers['Access-Control-Allow-Origin'] = origin
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, PATCH'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, Origin, Accept, X-Requested-With'
        
        return response

    # Register blueprints
    from app.routes import main  # Main web routes
    app.register_blueprint(main)

    # Import and register the API v1 Blueprint
    from app.api.v1 import bp as api_v1_bp  # API routes
    app.register_blueprint(api_v1_bp, url_prefix='/api/v1')

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('app.log'),
            logging.StreamHandler()
        ]
    )
    
    # Add error handlers
    @app.errorhandler(401)
    def unauthorized_error(error):
        return jsonify({
            'error': 'Unauthorized',
            'message': 'Invalid or expired token'
        }), 401

    @app.errorhandler(403)
    def forbidden_error(error):
        return jsonify({
            'error': 'Forbidden',
            'message': 'You do not have permission to access this resource'
        }), 403

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'Server Error: {error}')
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred'
        }), 500

    app.logger.info("Flask app initialized successfully.")
    return app