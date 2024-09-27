from src.init import db, ma  # Import database (SQLAlchemy) and marshmallow instances for ORM and serialisation
from marshmallow import fields  # Import fields for defining schema attributes
from marshmallow.validate import Length  # Import Length validator for string lengths

class Achievement(db.Model):
    """
    This class represents the Achievement model in the database.

    Attributes:
    - id: Primary key for the achievement.
    - game_id: Foreign key linking to the Game associated with the achievement.
    - title: The title or name of the achievement.
    - description: A description of what is required to achieve this achievement.
    - date_awarded: The date the achievement was awarded (optional).
    """
    __tablename__ = 'achievements'  # Define the database table name

    # Primary key for uniquely identifying each achievement
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Foreign key linking to the Game model
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)

    # The title of the achievement
    title = db.Column(db.String(100), nullable=False)
    
    # Description providing details about the achievement
    description = db.Column(db.Text, nullable=True)

    # Optional date indicating when the achievement was awarded
    date_awarded = db.Column(db.DateTime, nullable=True)

    # Relationship to associate this achievement with a specific game
    game = db.relationship('Game', back_populates='achievements')  # Back-reference to the Game model

    def __repr__(self):
        """Provide a string representation of the Achievement instance for debugging."""
        return f'<Achievement {self.title} for Game ID {self.game_id}>'

class AchievementSchema(ma.SQLAlchemySchema):
    """
    Marshmallow schema for the Achievement model, used for serialization and deserialization.

    This schema helps to validate and format the output and input data for achievements.
    """
    class Meta:
        model = Achievement  # Link the schema to the Achievement model
        load_instance = True  # Deserialize and load instances of the model

    # Automatically map model fields to schema fields
    id = ma.auto_field()
    game_id = ma.auto_field()
    title = ma.auto_field(validate=Length(min=1))  # Ensure title is a non-empty string
    description = ma.auto_field()
    date_awarded = ma.auto_field()  # Optionally include date_awarded for when achievements are earned

    # Optionally, we can include the game information nested when serialising achievements
    game = fields.Nested("GameSchema", only=["id", "name"])

# Instantiate schemas for single and multiple achievements
achievement_schema = AchievementSchema()
achievements_schema = AchievementSchema(many=True)