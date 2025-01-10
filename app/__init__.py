from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv  # Import load_dotenv to load environment variables
import os

# Load environment variables from .env file
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()

@login_manager.user_loader
def load_user(user_id):
    from .models import User  # Avoid circular imports
    return User.query.get(int(user_id))

def create_app():
    app = Flask(
        __name__,
        template_folder='../templates',
        static_folder='../static'
    )
    
    # Load configuration from environment variables
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback-secret-key')  # Use SECRET_KEY from .env or a fallback
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///app.db')  # Use DATABASE_URI from .env or a fallback
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Debug: Print loaded configuration
    print(f"SECRET_KEY: {app.config['SECRET_KEY']}")
    print(f"DATABASE_URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    # Initialize extensions with the app
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    
    # Configure login manager
    login_manager.login_view = 'main.login'  # Set the login view
    login_manager.login_message_category = 'info'
    
    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)
    
    # Create database tables (if they don't exist)
    with app.app_context():
        db.create_all()
    
    return app