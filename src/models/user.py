from src.init import db, ma, bcrypt  # Import extensions for database interaction, serialization, and password hashing
from marshmallow import fields  # Import fields module from Marshmallow for schema definition
from marshmallow.validate import Regexp  # Import Regexp validator for email validation
from sqlalchemy.orm import validates  # Import SQLAlchemy validation mechanism
from datetime import datetime  # Import datetime for handling timestamps

class User(db.Model):
    """
    Represents a User in the database.

    Attributes:
    - id: The unique identifier of the user.
    - username: The username of the user, must be unique.
    - email: The user's email address, used as a login credential and must be unique.
    - password_hash: The hashed version of the user's password.
    - date_created: Timestamp marking when the user record was created.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship examples: Assuming users might have scores or other related models
    scores = db.relationship('Score', back_populates='user', lazy='dynamic')
    # Additional relationships can be added here as needed

    def __repr__(self):
        """Provide a string representation of the User instance for debugging."""
        return f'<User {self.username}>'

    @property
    def password(self):
        """Raise an error when trying to access the raw password."""
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        """
        Hash and set the password for the user.

        Args:
        - password (str): The plaintext password from the user.
        """
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """
        Verify a plaintext password against the stored hash.

        Args:
        - password (str): The password provided by the user during login.

        Returns:
        - bool: Result of the password verification.
        """
        return bcrypt.check_password_hash(self.password_hash, password)

    @validates('email')
    def validate_email(self, key, email):
        """
        Validate email format before saving to the database.

        Args:
        - key (str): The key being validated (often 'email').
        - email (str): The email to validate.

        Raises:
        - AssertionError: If email format is invalid.
        
        Returns:
        - str: Validated email address.
        """
        assert '@' in email, "Provided email is not valid"
        return email

class UserSchema(ma.SQLAlchemySchema):
    """
    Marshmallow schema for the User model.

    This schema is utilized for serialization and deserialization of User instances.
    """
    class Meta:
        model = User
        load_instance = True  # Deserialize to model instances

    id = ma.auto_field()
    username = ma.auto_field()
    email = ma.auto_field()
    date_created = ma.auto_field()

    # Here you can define serialization for related fields if necessary
    scores = fields.List(fields.Nested("ScoreSchema", exclude=["user"]))

    # Email validation using regex
    email = fields.String(required=True, validate=Regexp(r"^\S+@\S+\.\S+$", error="Invalid email format"))

# Instances of the schema for use in application logic
user_schema = UserSchema(exclude=["password_hash"])  # Exclude password hash for security reasons
users_schema = UserSchema(exclude=["password_hash"], many=True)  # For handling multiple users