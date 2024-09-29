from init import db, ma
from marshmallow import fields

class Achievement(db.Model):
    
    # This class represents the Achievement model in the database.
    # - id: The primary key of the achievement.
    # - name: The name of the achievement, which should be unique and not null.
    # - description: A brief description of the achievement.
    # - user_id: Foreign key linking to the User who earned the achievement.
    # - game_id: Foreign key linking to the Game where the achievement can be earned.
    
    __tablename__ = "achievements"  # Specifies the table name in the database

    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each achievement
    name = db.Column(db.String(150), nullable=False, unique=True)  # Achievement name, unique and non-null
    description = db.Column(db.String(255), nullable=False)  # Description of what the achievement represents

    # Establishing foreign key relationships
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key to User
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)  # Foreign key to Game

    # Defining relationships
    user = db.relationship("User", back_populates="achievements")  # Relationship with User model
    game = db.relationship("Game", back_populates="achievements")  # Relationship with Game model


class AchievementSchema(ma.Schema):

    # Schema for serialising achievement records
    id = fields.Integer(dump_only=True)  # Only for output serialisation
    name = fields.String(required=True)  # Name of the achievement (required)
    description = fields.String(required=True)  # Description of the achievement (required)
    # Nested fields to include related user and game, avoiding recursive serialisation
    user = fields.Nested("UserSchema", exclude=["achievements", "password"])
    game = fields.Nested("GameSchema", exclude=["achievements"])

    class Meta:
        
        fields = ("id", "name", "description", "user", "game")  # Fields to include in serialisation

# Instances of AchievementSchema for serialising single and multiple achievement records
achievement_schema = AchievementSchema()  # Single achievement instance
achievements_schema = AchievementSchema(many=True)  # Multiple achievements instance