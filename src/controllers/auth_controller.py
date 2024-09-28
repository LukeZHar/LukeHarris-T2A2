from init import db, jwt, bcrypt
from models.user import User, user_schema, UserSchema, users_schema

from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/login", methods=["POST"])
def login():
    """
    This route is used to log in existing users.
    
    Expects JSON payload with 'email' and 'password'.
    Validates credentials and returns a JWT token with a success message if correct.
    Returns an error message with a 401 status code if credentials are incorrect.
    """
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    # Retrieve user with the given email
    user = User.query.filter_by(email=email).first()

    # Verify user and password
    if not user or not bcrypt.check_password_hash(user.password, password):
        return {"message": "Invalid credentials"}, 401

    # Generate JWT token if credentials are correct
    access_token = create_access_token(identity=user.id, expires_delta=timedelta(days=1))

    return {"message": f"Login successful, welcome back {user.name}", "access_token": access_token}


@auth.route("/register", methods=["POST"])
def register():
    """
    This route is used to create new users.
    
    Validates the provided data and registers a new user.
    Returns the new user data or an error message if invalid.
    """
    # Validate request data against User schema
    body = UserSchema().load(request.json)

    name = body.get("name")
    email = body.get("email")
    password = body.get("password")

    # Check if user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return {"message": "User already exists"}, 400

    # Ensure required fields are present
    if not name or not email or not password:
        return {"message": "Missing name, email, or password"}, 400

    # Hash the user's password
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    # Create new User instance
    new_user = User(name=name, email=email, password=hashed_password)

    # Add to database and commit changes
    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)


@auth.route("/users", methods=["GET"])
@jwt_required()
def get_users():
    """
    Returns a list of all users.
    Requires JWT token for authentication.
    """
    users = User.query.all()
    return users_schema.jsonify(users)


@auth.route("/users/<int:id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_user(id):
    """
    Updates an existing user by ID.
    User must be authenticated and authorised.
    Expects JSON payload with fields to be updated.
    """
    user = User.query.get(id)

    # Check if user exists
    if not user:
        return {"message": "User not found"}, 404

    # Ensure the current user is authorised to update their information
    if user.id != get_jwt_identity():
        return {"message": "Unauthorized"}, 401

    # Load and validate data
    body = UserSchema().load(request.json, partial=True)

    # Update user details
    if "name" in body:
        user.name = body["name"]
    if "email" in body:
        user.email = body["email"]
    if "password" in body:
        user.password = bcrypt.generate_password_hash(body["password"]).decode("utf-8")

    db.session.commit()

    return user_schema.jsonify(user)