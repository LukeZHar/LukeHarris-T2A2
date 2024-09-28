from init import db, ma
from marshmallow import fields

class Genre(db.Model):
    """
    This class represents the Genre model in the database.

    Attributes:
    - id: The primary key of the genre.
    - name: The name of the genre, which should be unique and not null.
    - description: A brief description of the genre.
    """
    __tablename__ = "genres"  # Specifies the table name in the database

    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each genre
    name = db.Column(db.String(80), nullable=False, unique=True)  # Genre name, unique and non-null
    description = db.Column(db.String(255))  # Optional description of the genre

    # Relationship to associate games with this genre
    games = db.relationship("Game", back_populates="genre", lazy='dynamic')  # Games that belong to this genre


class GenreSchema(ma.Schema):
    """
    Schema for serialising and deserialising Genre objects.
    
    This schema includes nested relationships for associated games.
    """
    
    # Excludes certain sensitive fields in nested representations to prevent recursive data exposure
    games = fields.List(fields.Nested("GameSchema", exclude=["genre"]))

    class Meta:
        """
        Meta class defining which fields are included in serialisation.
        """
        fields = ("id", "name", "description", "games")  # Fields to include in serialisation

# Instances of GenreSchema for serialising single and multiple genre records
genre_schema = GenreSchema()  # Single genre instance
genres_schema = GenreSchema(many=True)  # Multiple genres instance