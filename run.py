from flask import Flask
from dotenv import load_dotenv
import os
import logging
from app.extensions import db, bcrypt, login_manager, migrate  # Import extensions

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

    # Initialize CORS (Cross-Origin Resource Sharing)
    from flask_cors import CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:5173').split(',')
    CORS(app, resources={r"/api/*": {
        "origins": CORS_ORIGINS,
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    }})

    # Register blueprints
    from app.routes import main  # Main web routes
    app.register_blueprint(main)

    # Import the API v1 Blueprint
    from app.api.v1 import bp as api_v1_bp  # Import the blueprint

    # Register the API v1 Blueprint
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
    app.logger.info("Flask app initialized successfully.")

    return app