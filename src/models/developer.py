from src.init import db, ma  # Import the database (SQLAlchemy) and Marshmallow instances for ORM and serialisation
from marshmallow import fields  # Import fields from Marshmallow for schema definitions

class Developer(db.Model):
    """
    This class represents the Developer model in the database.

    Attributes:
    - id (int): Primary key for the Developer.
    - name (str): Name of the developer. Must be unique to prevent duplicate entries.
    - games (list): Relationship to retrieve the games developed by this developer.
    """
    __tablename__ = 'developers'  # Define the name of the table in the database

    # Auto-incrementing primary key for uniquely identifying each developer
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Developer name, which must be unique across records
    name = db.Column(db.String(100), unique=True, nullable=False)

    # Relationship definition to gather all games linked to this developer
    games = db.relationship('Game', back_populates='developer', lazy='dynamic')

    def __repr__(self):
        """Provide a string representation of the Developer instance for debugging."""
        return f'<Developer {self.name}>'

class DeveloperSchema(ma.SQLAlchemySchema):
    """
    Marshmallow schema for the Developer model.

    This schema handles serialisation and deserialisation of Developer instances, assisting in API response formatting.
    """
    class Meta:
        model = Developer  # Specify the ORM model linked with this schema
        load_instance = True  # Allows de-serialization into Developer model instances

    # Define how attributes of the Developer are serialized/deserialized automatically
    id = ma.auto_field()
    name = ma.auto_field()

    # Nested relationship to include a list of games developed, avoiding cyclic references by excluding 'developer'
    games = fields.List(fields.Nested("GameSchema", exclude=["developer"]))

# Create schema instances for handling single and multiple developers efficiently
developer_schema = DeveloperSchema()
developers_schema = DeveloperSchema(many=True)