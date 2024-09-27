from flask import Flask
from dotenv import load_dotenv
from src.init import db, ma, bcrypt, jwt  # Import extensions
from src.config import Config
from src.models import User, Game, Genre, Developer, Session, Score, Achievement  # Import models
from src.controllers.user_controller import user_bp
from src.controllers.game_controller import game_bp
from src.controllers.session_controller import session_bp
from src.controllers.score_controller import score_bp
from src.controllers.achievement_controller import achievement_bp
from src.controllers.genre_controller import genre_bp  # Ensure there's a blueprint for genres
from src.controllers.developer_controller import developer_bp  # Ensure there's a blueprint for developers

def create_app():
    """
    Create a Flask application instance.

    This function serves as the central factory function for our Flask app. It loads the configuration from
    environment variables, initializes extensions, and registers blueprints for different parts of the application.

    Returns:
        app (Flask): The Flask application instance.
    """
    
    # Load environment variables from the .env file
    load_dotenv()

    # Initialize Flask app
    app = Flask(__name__)

    # Load configuration settings from the Config class, which sources them from environment variables
    app.config.from_object(Config)

    # Initialize Flask extensions with the app instance
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Register blueprints to organize API endpoints by functionality
    # Each blueprint manages a subset of the application's routes
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(game_bp, url_prefix='/api/games')
    app.register_blueprint(session_bp, url_prefix='/api/sessions')
    app.register_blueprint(score_bp, url_prefix='/api/scores')
    app.register_blueprint(achievement_bp, url_prefix='/api/achievements')
    app.register_blueprint(genre_bp, url_prefix='/api/genres')  # Blueprint for genres
    app.register_blueprint(developer_bp, url_prefix='/api/developers')  # Blueprint for developers

    return app

if __name__ == '__main__':
    # Create and configure the app
    app = create_app()

    # Using the application context allows us to safely manipulate the database
    with app.app_context():
        # Create all database tables according to model definitions
        db.create_all()
    
    # Run the app on the local development server. Debug mode gives detailed error pages and automatic reloads.
    app.run(debug=True)