from flask import Blueprint, request
from flask_jwt_extended import jwt_required  # To enforce user authentication
from init import db  # Import the database instance
from models.developer import Developer, developer_schema, developers_schema  # Import Developer model and schemas

# Create a Blueprint for developer-related routes
developer_controller = Blueprint("developer_controller", __name__)

@developer_controller.route("/developers", methods=["POST"])
@jwt_required()  # Ensure the user is authenticated to create a developer
def create_developer():
    
    # Create a new developer.

    # Expects:
    #     - JSON payload with 'name'.

    # Returns:
    #     - JSON representation of the newly created developer.
    
    body = request.json  # Get JSON payload from the request

    # Create a new developer instance
    new_developer = Developer(
        name=body.get("name")  # The name of the developer
    )

    # Add the new developer to the database and commit the changes
    db.session.add(new_developer)
    db.session.commit()

    return developer_schema.jsonify(new_developer), 201  # Return the created developer with a 201 status


@developer_controller.route("/developers", methods=["GET"])
def get_developers():
    
    # Retrieve all developers.

    # Returns:
    #     - JSON list of all developers in the database.
    
    developers = Developer.query.all()  # Retrieve all developers from the database
    return developers_schema.jsonify(developers)  # Return the list of developers


@developer_controller.route("/developers/<int:id>", methods=["GET"])
def get_developer(id):
   
    # Retrieve a specific developer by ID.

    # Arguments:
    #     - id: The ID of the developer to retrieve.

    # Returns:
    #     - JSON representation of the developer if found.
    #     - Error message if the developer is not found.
    
    developer = Developer.query.get(id)  # Retrieve developer by ID

    if not developer:
        return {"message": "Developer not found"}, 404  # Return error if not found

    return developer_schema.jsonify(developer)  # Return the found developer


@developer_controller.route("/developers/<int:id>", methods=["PUT", "PATCH"])
@jwt_required()  # Ensure the user is authenticated to update a developer
def update_developer(id):
    
    # Update an existing developer's information.

    # Arguments:
    #     - id: The ID of the developer to update.

    # Expects:
    #     - JSON payload with 'name' to update.

    # Returns:
    #     - JSON representation of the updated developer if successful.
    #     - Error message if the developer is not found.
    
    developer = Developer.query.get(id)  # Retrieve the developer by ID

    if not developer:
        return {"message": "Developer not found"}, 404  # Return error if not found

    body = request.json  # Get JSON payload for updates

    # Update the name of the developer if provided
    if "name" in body:
        developer.name = body["name"]

    # Commit changes to the database
    db.session.commit()

    return developer_schema.jsonify(developer)  # Return the updated developer


@developer_controller.route("/developers/<int:id>", methods=["DELETE"])
@jwt_required()  # Ensure the user is authenticated to delete a developer
def delete_developer(id):
    
    # Delete a developer by their ID.

    # Arguments:
    #     - id: The ID of the developer to delete.

    # Returns:
    #     - Success message if deleted, or error message if not found.
    
    developer = Developer.query.get(id)  # Retrieve the developer by ID

    if not developer:
        return {"message": "Developer not found"}, 404  # Return error if not found

    # Delete the developer from the database
    db.session.delete(developer)
    db.session.commit()

    return {"message": "Developer deleted successfully"}, 200  # Return success message