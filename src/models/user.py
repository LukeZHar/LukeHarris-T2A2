from init import db, ma
from marshmallow import fields, validate
from marshmallow.validate import Regexp

class User(db.Model):
    
    # This class represents the User model in the database.
    # - id: The primary key of the user.
    # - name: The name of the user.
    # - email: The email of the user.
    # - password: The password of the user.
    # - is_admin: Whether the user is an admin or not.
    # - achievements: Relationship to track the user's achievements.
    # - scores: Relationship to manage user scores in different games.
    
    __tablename__ = "users"  # Table name in the database

    id = db.Column(db.Integer, primary_key=True)  # Primary key, unique ID for each user
    name = db.Column(db.String(80), nullable=False)  # User's name, non-nullable
    email = db.Column(db.String(120), unique=True, nullable=False)  # User's email, must be unique
    password = db.Column(db.String(255), nullable=False)  # Hashed user password
    is_admin = db.Column(db.Boolean, default=False)  # Boolean flag for admin rights, default is False

    # Relationships to other entities
    achievements = db.relationship("Achievement", back_populates="user")  # Link to Achievement model
    scores = db.relationship("Score", back_populates="user")  # Link to Score model
    sessions = db.relationship("Session", back_populates="user")  # Link to Session model
    
class UserSchema(ma.Schema):
   
    # Fields
    #
    id = fields.Integer(dump_only=True)  # Only for output
    name = fields.String(required=True, validate=[validate.Length(min=1)])
    is_admin = fields.Boolean(dump_only=True)
    password = fields.String(load_only=True, required=True, validate=[validate.Length(min=6)])
    # Ensures that the email field is in a valid format
    email = fields.String(
        required=True,
        validate=Regexp(r"^\S+@\S+\.\S+$", error="Invalid email format")
    )
    # Nested relationships, avoiding circular references by excluding user fields
    achievements = fields.List(fields.Nested("AchievementSchema", exclude=["user"]))
    scores = fields.List(fields.Nested("ScoreSchema", exclude=["user"]))
    sessions = fields.List(fields.Nested("SessionSchema", exclude=["user"]))

    class Meta:
        
        fields = ("id", "name", "email", "password", "is_admin", "achievements", "scores", "sessions")

# Schemas for users; excluding passwords for security
user_schema = UserSchema(exclude=("password",))  # Single user serialisation, password excluded
users_schema = UserSchema(exclude=("password",), many=True)  # Multiple users serialisation, passwords excluded