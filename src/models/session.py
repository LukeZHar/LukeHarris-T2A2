from src.init import db, ma  # Import the database (SQLAlchemy) and marshmallow instances for ORM and serialisation
from datetime import datetime  # Import to handle date and time for sessions

# Intermediary table for many-to-many relationship between Users and Sessions
session_participants = db.Table('session_participants',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('session_id', db.Integer, db.ForeignKey('sessions.id'), primary_key=True)
)

class Session(db.Model):
    """
    This class represents the Session model in the database.

    Attributes:
    - id: Primary key for the session.
    - game_id: Foreign key referencing the associated Game.
    - start_time: The timestamp when the session starts.
    - end_time: The timestamp when the session ends.
    - max_players: Maximum number of participants allowed in the session.
    - current_players: Number of players currently in the session.
    - result: Outcome or current status of the session.
    """
    __tablename__ = 'sessions'  # Define the database table name

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.now, nullable=False)
    end_time = db.Column(db.DateTime, nullable=True)
    max_players = db.Column(db.Integer, nullable=False)
    current_players = db.Column(db.Integer, default=0, nullable=False)
    result = db.Column(db.String(50), nullable=True)

    # Relationships
    game = db.relationship('Game', back_populates='sessions')
    scores = db.relationship('Score', back_populates='session', lazy='dynamic')
    participants = db.relationship('User', secondary=session_participants, back_populates='sessions', lazy='dynamic')

    def __repr__(self):
        """Provide a string representation showing essential information about the session."""
        return f'<Session {self.id} for Game {self.game_id}, {self.current_players}/{self.max_players} players>'

class SessionSchema(ma.SQLAlchemySchema):
    """
    Marshmallow schema for the Session model.

    This schema facilitates the serialization and deserialization of Session model instances.
    """
    class Meta:
        model = Session  # The ORM model that this schema represents
        load_instance = True  # Deserialize to model instances

    # Fields that are serialized/deserialized
    id = ma.auto_field()
    game_id = ma.auto_field()
    start_time = ma.auto_field()
    end_time = ma.auto_field()
    max_players = ma.auto_field()
    current_players = ma.auto_field()
    result = ma.auto_field()

    # Nested field to include related game information in session serialization
    game = fields.Nested("GameSchema", only=["id", "name"])
    # Optionally include a summary of scores or participants

# Schema instances to handle single and multiple session objects easily
session_schema = SessionSchema()
sessions_schema = SessionSchema(many=True)