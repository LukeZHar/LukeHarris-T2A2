from init import db, ma
from marshmallow import fields

class Score(db.Model):
    """
    This class represents the Score model in the database.

    Attributes:
    - id: The primary key of the score entry.
    - value: The score value achieved by the user.
    - date_achieved: The date and time when the score was achieved.
    - user_id: Foreign key linking to the User who achieved the score.
    - game_id: Foreign key linking to the Game for which the score is recorded.
    """
    __tablename__ = "scores"  # Specifies the table name in the database

    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each score entry
    value = db.Column(db.Integer, nullable=False)  # The score value, must be non-null
    date_achieved = db.Column(db.DateTime, nullable=False)  # Date and time when the score was achieved

    # Foreign key to associate with a specific user
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Foreign key to associate with a specific game
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)

    # Establishing relationships with the User and Game models
    user = db.relationship("User", back_populates="scores")  # Relationship with User model
    game = db.relationship("Game", back_populates="scores")  # Relationship with Game model


class ScoreSchema(ma.Schema):
    """
    Schema for serialising and deserialising Score objects.
    
    This schema includes nested relationships for user and game details.
    """
    id = fields.Integer(dump_only=True)
    value = fields.Integer(required=True)
    date_achieved = fields.DateTime(dump_only=True)  # Automatically set; not intended for input
    # Nested fields for related user and game, avoiding recursive serialisation issues
    user = fields.Nested("UserSchema", exclude=["scores", "password"])
    game = fields.Nested("GameSchema", exclude=["scores"])

    class Meta:
        """
        Meta class defining which fields should be serialised.
        """
        fields = ("id", "value", "date_achieved", "user", "game")  # Fields included in serialisation

# Instances of ScoreSchema for serialising single and multiple score records
score_schema = ScoreSchema()  # Single score instance
scores_schema = ScoreSchema(many=True)  # Multiple scores instance