# Import required extensions from Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# Initialize the extensions
# These are extension instances that will be initialised with the Flask application

# SQLAlchemy instance for database management
# It provides ORM capabilities to map classes to database tables
db = SQLAlchemy()

# Marshmallow instance for data serialisation and validation
# Used to facilitate conversion between complex data types and Python data types
ma = Marshmallow()

# Bcrypt instance for password hashing
# Ensures that passwords are stored securely using salted hashes
bcrypt = Bcrypt()

# JWTManager instance for token management
# Handles the creation and verification of JSON Web Tokens for authentication
jwt = JWTManager()