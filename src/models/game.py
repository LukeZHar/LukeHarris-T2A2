from init import db, ma
from marshmallow import fields

class Game(db.Model):
    """
    This class represents the Game model in the database.

    Attributes:
    - id: The primary key of the game.
    - title: The title of the game, which should be unique and not null.
    - genre_id: Foreign key linking to the Genre of the game.
    - developer_id: Foreign key linking to the Developer of the game.
    """
    __tablename__ = "games"  # Specifies the table name in the database

    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each game
    title = db.Column(db.String(150), nullable=False, unique=True)  # Game title, unique and non-null
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'), nullable=False)  # Foreign key to Genre
    developer_id = db.Column(db.Integer, db.ForeignKey('developers.id'), nullable=False)  # Foreign key to Developer
    
    # Establishing relationships with related models
    genre = db.relationship("Genre", back_populates="games")  # Relationship with the Genre model
    developer = db.relationship("Developer", back_populates="games")  # Relationship with the Developer model
    scores = db.relationship("Score", back_populates="game", lazy='dynamic')  # Scores achieved in this game
    sessions = db.relationship("Session", back_populates="game", lazy='dynamic')  # Sessions related to this game
    achievements = db.relationship("Achievement", back_populates="game", lazy='dynamic')  # Achievements linked to the game


class GameSchema(ma.Schema):
    """
    Schema for serialising and deserialising Game objects.
    
    Includes nested relationships for user-friendly data responses.
    """
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True)
    # Nested fields for related genre, developer, scores, and sessions, while avoiding recursive data exposure
    genre = fields.Nested("GenreSchema", exclude=["games"])
    developer = fields.Nested("DeveloperSchema", exclude=["games"])
    scores = fields.List(fields.Nested("ScoreSchema", exclude=["game"]))
    sessions = fields.List(fields.Nested("SessionSchema", exclude=["game"]))
    achievements = fields.List(fields.Nested("AchievementSchema", exclude=["game"]))  # Serialize related achievements

    # Meta class specifies the fields in serialisation
    class Meta:
        """
        Meta class defining which fields are included in serialisation.
        """
        fields = ("id", "title", "genre", "developer", "scores", "sessions", "achievements")

# Instances of GameSchema for serialising single and multiple game entries
game_schema = GameSchema()  # Single game instance
games_schema = GameSchema(many=True)  # Multiple games instance