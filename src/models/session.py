from init import db, ma
from marshmallow import fields
from datetime import datetime

class Session(db.Model):
    
    # This class represents the Session model in the database.
    # - id: The primary key of the session.
    # - start_time: The timestamp indicating when the session started.
    # - end_time: The timestamp indicating when the session ended. This can be null if the session is ongoing.
    # - user_id: Foreign key linking to the User who is participating in the session.
    # - game_id: Foreign key linking to the Game that the session is associated with.
    
    __tablename__ = "sessions"  # Specifies the table name in the database

    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each session

    # Start time of the session, cannot be null
    start_time = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    # End time of the session, can be null if the session is ongoing
    end_time = db.Column(db.DateTime)

    # Foreign key to link the session with a specific user
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Foreign key to link the session with a specific game
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)

    # Establishing relationships with the User and Game models
    user = db.relationship("User", back_populates="sessions")  # User model relationship
    game = db.relationship("Game", back_populates="sessions")  # Game model relationship

class SessionSchema(ma.Schema):

    # Schema for serialising and deserialising Session objects.

    # Fields to include in serialisation
    id = fields.Integer(dump_only=True)
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime()

    # Nested fields for associated user and game, avoiding unnecessary circular references
    user = fields.Nested("UserSchema", exclude=["sessions", "password"])
    game = fields.Nested("GameSchema", exclude=["sessions"])

    class Meta:
        
        fields = ("id", "start_time", "end_time", "user", "game")  # Fields to include in serialisation

# Instances of SessionSchema for serialising single and multiple session data
session_schema = SessionSchema()  # Single session instance
sessions_schema = SessionSchema(many=True)  # Multiple sessions instance