# models/__init__.py

from init import db  # Import the SQLAlchemy database instance

# Import all model classes so they can be easily accessed
from models.user import User
from models.game import Game
from models.genre import Genre
from models.developer import Developer
from models.session import Session
from models.score import Score
from models.achievement import Achievement