from src.init import db, ma  # Import the database and marshmallow instances for ORM and serialization
from datetime import datetime  # Import for timestamp fields

class Score(db.Model):
    """
    This class represents the Score model in the database.

    Attributes:
    - id: Primary key identifying the score entry.
    - user_id: Foreign key linking to the User who achieved the score.
    - session_id: Foreign key linking to the Session associated with the score.
    - score_value: The actual score achieved by the user in the session.
    - date_achieved: Timestamp marking when the score was achieved.
    """
    __tablename__ = 'scores'  # Explicitly set the table name in the database

    # Primary key for uniquely identifying a score entry
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Foreign key linking to the User table
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Foreign key linking to the Session table
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'), nullable=False)
    
    # Column to store the score value achieved by the user
    score_value = db.Column(db.Float, nullable=False)
    
    # Automatically set the timestamp for when the score was achieved
    date_achieved = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to link Score back to the User model
    user = db.relationship('User', back_populates='scores')
    
    # Relationship to link Score back to the Session model
    session = db.relationship('Session', back_populates='scores')

    def __repr__(self):
        """Provide a string representation of the Score instance."""
        return f'<Score {self.score_value} by User {self.user_id} in Session {self.session_id}>'

class ScoreSchema(ma.SQLAlchemySchema):
    """
    Marshmallow schema for the Score model, used for serializing and deserializing Score objects.
    """
    class Meta:
        model = Score  # Links the schema to the Score model
        load_instance = True  # Deserializes to model instances

    # Automatically map fields from the Score model
    id = ma.auto_field()
    user_id = ma.auto_field()
    session_id = ma.auto_field()
    score_value = ma.auto_field()
    date_achieved = ma.auto_field()

    # Optionally include nested representations for related fields
    user = fields.Nested("UserSchema", only=["id", "username"])
    session = fields.Nested("SessionSchema", only=["id", "start_time", "end_time"])

# Schema instances for serialization and deserialization
score_schema = ScoreSchema()
scores_schema = ScoreSchema(many=True)