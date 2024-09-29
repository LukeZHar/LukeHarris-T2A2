from init import db, ma
from marshmallow import fields

class Developer(db.Model):
    """
    This class represents the Developer model in the database.

    Attributes:
    - id: The primary key of the developer.
    - name: The name of the developer, which should be unique and not null.
    """
    __tablename__ = "developers"  # Specifies the table name in the database

    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each developer
    name = db.Column(db.String(150), nullable=False, unique=True)  # Developer name, unique and non-null

    # Relationship to associate games with this developer
    games = db.relationship("Game", back_populates="developer", lazy='dynamic')  # Games developed by this developer


class DeveloperSchema(ma.Schema):
    """
    Schema for serialising and deserialising Developer objects.
    
    Includes nested relationships for associated games.
    """
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    # Nested fields for related games, avoiding recursive serialisation
    games = fields.List(fields.Nested("GameSchema", exclude=["developer"]))

    class Meta:
        """
        Meta class defining which fields are included in serialization.
        """
        fields = ("id", "name", "games")  # Fields to include in serialization

# Instances of DeveloperSchema for serializing single and multiple developer records
developer_schema = DeveloperSchema()  # Single developer instance
developers_schema = DeveloperSchema(many=True)  # Multiple developers instance