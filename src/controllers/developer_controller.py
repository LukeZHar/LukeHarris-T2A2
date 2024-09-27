from init import db  # Import the database instance for SQLAlchemy
from models.developer import Developer, developer_schema, developers_schema  # Import the Developer model and schemas
from flask import Blueprint, request, jsonify  # Import necessary components from Flask
from flask_jwt_extended import jwt_required  # JWT helper for authentication

# Create a Blueprint for developer-related routes
developer_bp = Blueprint('developers', __name__, url_prefix='/api/developers')

@developer_bp.route("/", methods=["POST"])
@jwt_required()  # Protect this route with JWT authentication
def create_developer():
    """
    Create a new developer in the database.

    Expects a JSON payload with 'name'.
    
    If successful, returns the created developer with a 201 status code.
    Returns a 400 status code if there are validation errors (e.g., developer already exists).
    """
    json_data = request.get_json()  # Load the incoming JSON data from the request
    name = json_data.get("name")  # Extract the developer name from the JSON payload

    # Validate that the name is provided
    if not name:
        return {"message": "Missing developer name."}, 400  # Return error if no name is provided

    # Check for the existence of an existing developer with the same name
    if Developer.query.filter_by(name=name).first():
        return {"message": "Developer already exists."}, 400  # Return conflict error if developer exists

    # Create a new Developer instance
    new_developer = Developer(name=name)

    # Add the new developer to the database session
    db.session.add(new_developer)
    db.session.commit()  # Commit the transaction to save the new developer

    return developer_schema.jsonify(new_developer), 201  # Return the created developer as JSON


@developer_bp.route("/", methods=["GET"])
def get_developers():
    """
    Retrieve a list of all developers in the database.

    Returns a JSON list of all developers.
    """
    developers = Developer.query.all()  # Query all developers from the database
    return developers_schema.jsonify(developers), 200  # Return the developers as a JSON response


@developer_bp.route("/<int:developer_id>", methods=["GET"])
def get_developer(developer_id):
    """
    Retrieve a single developer by their ID.

    Args:
    - developer_id: The ID of the developer to retrieve.

    Returns:
    A JSON representation of the developer or a 404 error if not found.
    """
    developer = Developer.query.get(developer_id)  # Attempt to retrieve the developer by ID
    if developer:
        return developer_schema.jsonify(developer), 200  # Return the developer as JSON if found
    else:
        return {"message": "Developer not found."}, 404  # Return 404 if the developer does not exist


@developer_bp.route("/<int:developer_id>", methods=["PUT", "PATCH"])
@jwt_required()  # Protect this route with JWT authentication
def update_developer(developer_id):
    """
    Update an existing developer by ID.

    Args:
    - developer_id: The ID of the developer to update.

    Expects a JSON payload with fields to update (optional).

    Returns:
    The updated developer as JSON or a 404 error if the developer is not found.
    """
    developer = Developer.query.get(developer_id)  # Retrieve the developer by ID
    if not developer:
        return {"message": "Developer not found."}, 404  # Return 404 if the developer does not exist

    # Load the incoming data for updates, allowing for partial updates
    body = request.get_json()

    # Update the developer's name if it is provided in the request
    if "name" in body:
        developer.name = body["name"]

    db.session.commit()  # Commit changes to the database

    return developer_schema.jsonify(developer), 200  # Return the updated developer as JSON


@developer_bp.route("/<int:developer_id>", methods=["DELETE"])
@jwt_required()  # Protect this route with JWT authentication
def delete_developer(developer_id):
    """
    Delete a developer by ID.

    Args:
    - developer_id: The ID of the developer to delete.

    Returns:
    A success message or a 404 error if the developer does not exist.
    """
    developer = Developer.query.get(developer_id)  # Attempt to retrieve the developer by ID

    # Check if the developer exists
    if not developer:
        return {"message": "Developer not found."}, 404  # Return a 404 error if not found
    
    # Delete the developer
    db.session.delete(developer)  # Mark the developer for deletion
    db.session.commit()  # Commit the transaction to remove the developer

    # Return a success message indicating the deletion was successful
    return {"message": "Developer deleted successfully"}, 200  # Return a success message with a 200 status code