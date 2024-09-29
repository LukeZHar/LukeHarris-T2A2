import os
from flask import Flask
from marshmallow.exceptions import ValidationError

# Import initialised instances of database, Marshmallow, Bcrypt, and JWT
from init import db, ma, bcrypt, jwt

# Import controllers 
from controllers.cli_controllers import db_commands
from controllers.auth_controller import auth
from controllers.user_controller import user_controller
from controllers.game_controller import game_controller
from controllers.genre_controller import genre_controller
from controllers.developer_controller import developer_controller
from controllers.session_controller import session_controller
from controllers.score_controller import score_controller
from controllers.achievement_controller import achievement_controller

def create_app():
    # creates the Flask application
    app = Flask(__name__)

    # Configure the app's secret key from environment variables
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

    # Set the SQLAlchemy database URI, read from environment variables
    # This defines the database connection string used by SQLAlchemy
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    
    # Initialise SQLAlchemy with the Flask app instance
    # This sets up the database connection and prepares models
    db.init_app(app)
    
    # Initialise Marshmallow for object serialization/deserialization
    ma.init_app(app)
    
    # Initialise Bcrypt for secure password hashing
    # Used for hashing passwords and authenticating users
    bcrypt.init_app(app)
    
    # Initialise JWTManager for handling JSON Web Tokens
    jwt.init_app(app)

    # Define an error handler for Marshmallow's ValidationError
    # Converts validation errors into JSON responses with status code 400
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        return {"validation_error": error.messages}, 400
    
    # Register CLI-related commands with the app
    # These commands help with database operations via command line
    app.register_blueprint(db_commands)
    
    # Register authentication routes and logic
    app.register_blueprint(auth)

    # Register user management routes
    app.register_blueprint(user_controller)

    # Register game management routes
    app.register_blueprint(game_controller)

    # Register genre management routes
    app.register_blueprint(genre_controller)

    # Register developer data routes
    app.register_blueprint(developer_controller)

    # Register session management routes for multiplayer games
    app.register_blueprint(session_controller)

    # Register score tracking routes
    app.register_blueprint(score_controller)

    # Register achievement management routes
    app.register_blueprint(achievement_controller)
    
    # Return the configured Flask app 
    return app
