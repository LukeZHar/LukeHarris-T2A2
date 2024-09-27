# Import necessary libraries and extensions
from flask import Flask  # Flask is the web framework for building web applications
from flask_sqlalchemy import SQLAlchemy  # SQLAlchemy for ORM (Object Relational Mapping)
from flask_marshmallow import Marshmallow  # Marshmallow for serialisation and deserialisation
from flask_bcrypt import Bcrypt  # Bcrypt for hashing passwords securely
from flask_jwt_extended import JWTManager  # JWTManager for handling JSON Web Tokens
import os  # os allows us to access environment variables

# Initialise the extensions
db = SQLAlchemy()  # SQLAlchemy instance for managing the database
ma = Marshmallow()  # Marshmallow instance for schema and serialisation
bcrypt = Bcrypt()  # Bcrypt instance for password hashing
jwt = JWTManager()  # JWTManager instance for handling token-based authentication

def create_app():
    """
    Create and configure the Flask application.
    
    This function will set up the application with configuration parameters,
    initialise the database, and register the blueprints for the application's 
    controllers.
    
    Returns:
        app (Flask): The configured Flask application instance.
    """
    
    app = Flask(__name__)  # Create a new Flask application instance

    # Load configuration settings from environment variables
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')  # Database connection string
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking for better performance
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  # Secret key for maintaining session data and CSRF protection
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')  # Secret key used for signing JWT tokens

    # Initialise the extensions with the app instance
    db.init_app(app)  # Bind SQLAlchemy instance to the app
    ma.init_app(app)  # Bind Marshmallow instance to the app
    bcrypt.init_app(app)  # Bind Bcrypt instance to the app
    jwt.init_app(app)  # Bind JWTManager instance to the app

    with app.app_context():
        """
        Create the database tables if they do not exist yet.
        
        Using 'app.app_context()' allows us to use 'db' to manage the application’s database
        related operations while having the app context pushed.
        """
        db.create_all()  # Create all tables defined in our models

    # Registering blueprints for modular approach
    from controllers.user_controller import user_bp  # Import user controller
    from controllers.game_controller import game_bp  # Import game controller
    from controllers.session_controller import session_bp  # Import session controller
    from controllers.score_controller import score_bp  # Import score controller
    from controllers.achievement_controller import achievement_bp  # Import achievement controller

    # Registering each blueprint with the app
    app.register_blueprint(user_bp)  # Register user-related routes
    app.register_blueprint(game_bp)  # Register game-related routes
    app.register_blueprint(session_bp)  # Register session-related routes
    app.register_blueprint(score_bp)  # Register score-related routes
    app.register_blueprint(achievement_bp)  # Register achievement-related routes

    return app  # Return the configured Flask application instance