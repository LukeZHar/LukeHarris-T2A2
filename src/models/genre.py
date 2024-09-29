from init import db, ma
from marshmallow import fields

class Genre(db.Model):
    
    __tablename__ = "genres"  # Specifies the table name in the database

    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each genre
    name = db.Column(db.String(80), nullable=False, unique=True)  # Genre name, unique and non-null

    # Relationship to associate games with this genre
    games = db.relationship("Game", back_populates="genre", lazy='dynamic')  # Games that belong to this genre


class GenreSchema(ma.Schema):
   
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    # Excludes certain sensitive fields in nested representations to prevent recursive data exposure
    games = fields.List(fields.Nested("GameSchema", exclude=["genre"]))

    class Meta:
        
        fields = ("id", "name", "games")  # Fields to include in serialisation

# Instances of GenreSchema for serialising single and multiple genre records
genre_schema = GenreSchema()  # Single genre instance
genres_schema = GenreSchema(many=True)  # Multiple genres instance