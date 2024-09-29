from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db  # Import the database instance
from models.user import User, user_schema, users_schema  # Import User model and schemas

# Create a Blueprint for user-related routes
user_controller = Blueprint("user_controller", __name__)

@user_controller.route("/users/<int:id>", methods=["GET"])
@jwt_required()  # Ensure the user is authenticated to access this route
def get_user(id):
    
    # Retrieve details of a specific user by their ID.
    # - id: The ID of the user to retrieve.

    # Returns:
    # - JSON representation of the user if found.
    # - Error message if the user does not exist.
    
    # Fetch the user from the database by ID
    user = User.query.get(id)
    
    # If user not found, return error message
    if not user:
        return {"message": "User not found"}, 404

    # Return user data
    return user_schema.jsonify(user)


@user_controller.route("/users", methods=["GET"])
@jwt_required()  # Ensure the user is authenticated to access this route
def get_all_users():
    
    # Retrieve a list of all users.

    # Returns:
    # - JSON list of all users in the database.

    
    users = User.query.all()  # Retrieve all users
    return users_schema.jsonify(users)  # Return user data


@user_controller.route("/users/<int:id>", methods=["PUT", "PATCH"])
@jwt_required()  # Ensure the user is authenticated to access this route
def update_user(id):
    
    # Update an existing user's information.

    # Arguments:
    # - id: The ID of the user to update.

    # Expects a JSON payload with fields to update (name or email).

    # Returns:
    # - Updated user data if successful.
    # - Error message if user not found or if unauthorised.
    
    # Fetch the user from the database
    user = User.query.get(id)

    # If user not found, return an error message
    if not user:
        return {"message": "User not found"}, 404

    # Ensure that the authenticated user can only update their own information
    if user.id != get_jwt_identity():
        return {"message": "Unauthorised"}, 401

    # Get the data from the request, allowing optional updates
    body = request.json

    # Update user fields if present in the request
    if "name" in body:
        user.name = body["name"]
    if "email" in body:
        user.email = body["email"]
    if "password" in body:
        user.password = bcrypt.generate_password_hash(body["password"]).decode("utf-8")

    # Commit changes to the database
    db.session.commit()

    # Return the updated user data
    return user_schema.jsonify(user)


@user_controller.route("/users/<int:id>", methods=["DELETE"])
@jwt_required()  # Ensure the user is authenticated to access this route
def delete_user(id):
    
    # Delete a user by their ID.

    # Arguments:
    # - id: The ID of the user to delete.

    # Returns:
    # - Success message on deletion or an error message if user not found.
    
    # Fetch the user from the database
    user = User.query.get(id)

    # If user not found, return an error message
    if not user:
        return {"message": "User not found"}, 404

    # Ensure the authenticated user can only delete their own account
    if user.id != get_jwt_identity():
        return {"message": "Unauthorised"}, 401

    # Remove the user from the session and commit the deletion
    db.session.delete(user)
    db.session.commit()

    # Return a success message
    return {"message": "User deleted successfully"}, 200