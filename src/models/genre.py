from src import db, ma  # Import the SQLAlchemy database instance and Marshmallow for serialisation
from marshmallow import fields  # Import fields module from Marshmallow for schema definition

class Genre(db.Model):
    """
    This class represents the Genre model in the database.

    Attributes:
    - id: Primary key for the genre.
    - name: The name of the genre, must be unique to prevent duplicates.
    - games: Relationship field to retrieve all games that fall under this genre.
    """
    __tablename__ = 'genres'  # Define the name of the table in the database

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Primary key
    name = db.Column(db.String(50), unique=True, nullable=False)  # Genre name, unique and non-nullable

    # Relationship to link genres back to their associated games
    games = db.relationship('Game', back_populates='genre', lazy='dynamic')

    def __repr__(self):
        """Provide a string representation for the Genre instance for debugging."""
        return f'<Genre {self.name}>'

class GenreSchema(ma.SQLAlchemySchema):
    """
    Marshmallow schema for the Genre model for serialisation and deserialisation.

    Fields:
    - id
    - name
    - games: Includes a list of games associated with this genre.
    """
    class Meta:
        model = Genre  # Specifies the database model associated with this schema
        load_instance = True  # Deserialises directly to JWT model instances

    id = ma.auto_field()  # Automatically map the ID field
    name = ma.auto_field()  # Automatically map the genre name field

    # Use nested fields to include associated games in the serialisation, if needed
    games = fields.List(fields.Nested("GameSchema", exclude=["genre"]))

# Create schema instances for use in your application to handle single and multiple genre objects
genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)