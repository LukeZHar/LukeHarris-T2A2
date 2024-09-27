from src.init import db, ma  # Import database and marshmallow instances
from marshmallow import fields  # Import fields for Marshmallow schema
from datetime import datetime  # Import datetime for handling date fields

class Game(db.Model):
    """
    This class represents the Game model in the database.

    Attributes:
    - id: Primary key for the game.
    - name: Name of the game, must be unique.
    - description: A brief description of the game.
    - release_date: The official release date of the game.
    - genre_id: Foreign key linking to the Genre table.
    - developer_id: Foreign key linking to the Developer table.
    """
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    release_date = db.Column(db.Date, nullable=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'), nullable=False)
    developer_id = db.Column(db.Integer, db.ForeignKey('developers.id'), nullable=False)

    # Relationships
    genre = db.relationship('Genre', back_populates='games')
    developer = db.relationship('Developer', back_populates='games')
    sessions = db.relationship('Session', back_populates='game', lazy='dynamic')
    achievements = db.relationship('Achievement', back_populates='game', lazy='dynamic')

    def __repr__(self):
        """Provide a string representation of this Game instance, useful for debugging."""
        return f'<Game {self.name}>'

class GameSchema(ma.SQLAlchemySchema):
    """
    Marshmallow schema for the Game model, used for serializing and deserializing Game objects.

    Fields:
    - id
    - name
    - description
    - release_date
    - genre: Nested schema for genre information.
    - developer: Nested schema for developer information.
    """
    class Meta:
        model = Game  # References the SQLAlchemy model
        load_instance = True  # Deserialize to model instances

    id = ma.auto_field()
    name = ma.auto_field()
    description = ma.auto_field()
    release_date = ma.auto_field()

    # Nested relationships to ensure complete serialization
    genre = fields.Nested("GenreSchema", exclude=["games"])
    developer = fields.Nested("DeveloperSchema", exclude=["games"])
    sessions = fields.List(fields.Nested("SessionSchema", exclude=["game"]))
    achievements = fields.List(fields.Nested("AchievementSchema", exclude=["game"]))

# Schema instances for single and multiple game instances
game_schema = GameSchema()
games_schema = GameSchema(many=True)