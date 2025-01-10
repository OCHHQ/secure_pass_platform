from flask import Flask
from flask_wtf.csrf import CSRFProtect
import os

def create_app():
    app = Flask(__name__)

    # Load configuration from environment variables or a config file
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback-secret-key')  # Use a secure key
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize Flask-WTF for CSRF protection
    csrf = CSRFProtect(app)

    # Initialize extensions
    from app import db, bcrypt, login_manager  # Import extensions from app/__init__.py
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)  # Initialize LoginManager with the app

    # Configure login manager
    login_manager.login_view = 'main.login'  # Set the login view
    login_manager.login_message_category = 'info'

    # Register blueprints or routes
    from app.routes import main  # Import the blueprint as 'main'
    app.register_blueprint(main)  # Register the blueprint as 'main'

    # Create database tables (if they don't exist)
    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    # Create the Flask app
    app = create_app()

    # Run the app
    app.run(debug=True)