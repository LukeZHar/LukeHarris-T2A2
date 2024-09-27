# Import required extensions from Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# Initialize the extensions
db = SQLAlchemy()  # SQLAlchemy instance for database management
ma = Marshmallow()  # Marshmallow instance for data serialisation
bcrypt = Bcrypt()  # Bcrypt instance for password hashing
jwt = JWTManager()  # JWTManager instance for token management