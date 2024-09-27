from init import db, jwt, bcrypt  # Import the database instance, JWT, and Bcrypt
from models.user import User, user_schema, UserSchema, users_schema  # Import the User model and schemas

from flask import Blueprint, request, jsonify  # Import necessary components from Flask
from flask_jwt_extended import jwt_required, get_jwt_identity  # JWT authentication helpers
from sqlalchemy.exc import IntegrityError  # Import for handling integrity errors
from datetime import timedelta
# Create a Blueprint for user-related routes
user_bp = Blueprint('users', __name__, url_prefix='/api/users')

@user_bp.route("/register", methods=["POST"])
def register():
    """
    Register a new user in the application.

    Expects a JSON payload with 'username', 'email', and 'password'.
    
    If successful, returns the created user with a 201 status code.
    Returns a 400 status code if there is a conflict (e.g., user already exists).
    """
    body = UserSchema.load(request.json)  # Load data from the request
    username = body.get("username")
    email = body.get("email")
    password = body.get("password")

    # Check if a user with the same email already exists
    if User.query.filter_by(email=email).first():
        return {"message": "User already exists"}, 400  # Conflict response

    if not username or not email or not password:
        return {"message": "Missing username, email, or password"}, 400  # Error if fields are missing

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")  # Hash the password
    new_user = User(username=username, email=email, password=hashed_password)  # Create the new user

    db.session.add(new_user)  # Add the user to the session
    db.session.commit()  # Commit to save the new user

    return user_schema.jsonify(new_user), 201  # Return the created user

@user_bp.route("/login", methods=["POST"])
def login():
    """
    This route handles user login.

    Expects a JSON payload with 'email' and 'password'.
    
    If the credentials are valid, returns a JWT token and a success message.
    If the credentials are invalid, returns an error message with a 401 status code.
    """
    email = request.json.get("email", None)  # Get the user's email from the request
    password = request.json.get("password", None)  # Get the user's password from the request

    # Retrieve the user by email
    user = User.query.filter_by(email=email).first()

    # Check if the user exists and the password matches
    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        # If credentials are incorrect, return a 401 error
        return {"message": "Invalid credentials"}, 401

    # If the credentials are correct, create a JWT token with the user ID as the payload
    access_token = create_access_token(identity=user.id, expires_delta=timedelta(days=1))

    # Return the JWT token with a success message
    return {"message": f"Login successful, welcome back {user.username}", "access_token": access_token}, 200

@user_bp.route("/users", methods=["GET"])
@jwt_required()  # Protect this route with JWT authentication
def get_all_users():
    """
    Retrieve a list of all users in the application.

    Returns a JSON list of users.
    """
    users = User.query.all()  # Query all users from the database
    return users_schema.jsonify(users), 200  # Return the list of users as a JSON response


@user_bp.route("/users/<int:user_id>", methods=["GET"])
@jwt_required()  # Protect this route with JWT authentication
def get_user(user_id):
    """
    Retrieve a single user by their ID.

    Args:
    - user_id: The ID of the user to retrieve.

    Returns:
    A JSON representation of the user or a 404 error if not found.
    """
    user = User.query.get(user_id)  # Try to find the user by ID
    if user:
        return user_schema.jsonify(user), 200  # Return the user as JSON if found
    else:
        return {"message": "User not found."}, 404  # Return a 404 if the user does not exist

@user_bp.route("/users/<int:user_id>", methods=["PUT", "PATCH"])
@jwt_required()  # Protect route with JWT authentication
def update_user(user_id):
    """
    Update an existing user by ID.

    Args:
    - user_id: The ID of the user to update.

    Expects a JSON payload with fields to update.

    Returns:
    The updated user as JSON or a 404 error if the user is not found.
    """
    user = User.query.get(user_id)  # Find user by ID
    if not user:
        return {"message": "User not found."}, 404  # Return 404 if user not found

    # Ensure the request is coming from the same user
    if user.id != get_jwt_identity():
        return {"message": "Unauthorized"}, 401  # Return 401 if not authorized

    body = UserSchema.load(request.json, partial=True)  # Load incoming JSON data

    # Update the fields if they are provided in the request
    if "username" in body:
        user.username = body["username"]
    if "email" in body:
        user.email = body["email"]
    if "password" in body:
        user.password = bcrypt.generate_password_hash(body["password"]).decode("utf-8")

    db.session.commit()  # Commit changes
    return user_schema.jsonify(user)  # Return updated user

@user_bp.route("/users/<int:user_id>", methods=["DELETE"])
@jwt_required()  # Protect route
def delete_user(user_id):
    """
    Delete a user by ID.

    Args:
    - user_id: The ID of the user to delete.

    Returns:
    A success message or a not found message if the user does not exist.
    """
    # Get the user by ID
    user = User.query.get(user_id)

    # Check if the user exists
    if not user:
        return {"message": "User not found"}, 404  # Return a 404 error if the user does not exist
    
    # Ensure that the current logged-in user is authorized to delete this user
    if user.id != get_jwt_identity():
        return {"message": "Unauthorized"}, 401  # Return a 401 error for unauthorized access
    
    # Delete the user from the database
    db.session.delete(user)
    db.session.commit()  # Commit the deletion

    # Return a success message indicating deletion was successful
    return {"message": "User deleted successfully"}, 200