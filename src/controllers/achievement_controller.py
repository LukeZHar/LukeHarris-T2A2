from flask import Blueprint, request
from flask_jwt_extended import jwt_required  # To enforce user authentication
from init import db  # Import the database instance
from models.achievement import Achievement, achievement_schema, achievements_schema  # Import Achievement model and schemas

# Create a Blueprint for achievement-related routes
achievement_controller = Blueprint("achievement_controller", __name__)

@achievement_controller.route("/achievements", methods=["POST"])
@jwt_required()  # Ensure the user is authenticated to create an achievement
def create_achievement():
    
    # Create a new achievement.

    # Expects:
    #     - JSON payload with 'name', 'description', 'user_id', and 'game_id'.
    
    # Returns:
    #     - JSON representation of the newly created achievement.
    
    body = request.json  # Get JSON payload from the request

    # Create a new achievement instance
    new_achievement = Achievement(
        name=body.get("name"),  # Name of the achievement
        description=body.get("description"),  # Description of what the achievement represents
        user_id=body.get("user_id"),  # User who achieved this
        game_id=body.get("game_id")  # Game where this achievement can be earned
    )

    # Add the new achievement to the database and commit the changes
    db.session.add(new_achievement)
    db.session.commit()

    return achievement_schema.jsonify(new_achievement), 201  # Return the created achievement with a 201 status


@achievement_controller.route("/achievements", methods=["GET"])
def get_achievements():
   
    # Retrieve all achievements.

    # Returns:
    #     - JSON list of all achievements in the database.
    
    achievements = Achievement.query.all()  # Retrieve all achievements from the database
    return achievements_schema.jsonify(achievements)  # Return the list of achievements


@achievement_controller.route("/achievements/<int:id>", methods=["GET"])
def get_achievement(id):
    
    # Retrieve a specific achievement by ID.

    # Arguments:
    #     - id: The ID of the achievement to retrieve.

    # Returns:
    #     - JSON representation of the achievement if found.
    #     - Error message if the achievement is not found.
   
    achievement = Achievement.query.get(id)  # Retrieve achievement by ID

    if not achievement:
        return {"message": "Achievement not found"}, 404  # Return error if not found

    return achievement_schema.jsonify(achievement)  # Return the found achievement


@achievement_controller.route("/achievements/<int:id>", methods=["PUT", "PATCH"])
@jwt_required()  # Ensure the user is authenticated to update an achievement
def update_achievement(id):
    
    # Update an existing achievement's information.

    # Arguments:
    #     - id: The ID of the achievement to update.

    # Expects:
    #     - JSON payload with fields to update, such as 'name' or 'description'.

    # Returns:
    #     - JSON representation of the updated achievement if successful.
    #     - Error message if the achievement is not found.
    
    achievement = Achievement.query.get(id)  # Retrieve the achievement by ID

    if not achievement:
        return {"message": "Achievement not found"}, 404  # Return error if not found

    body = request.json  # Get JSON payload for updates

    # Update fields as necessary
    if "name" in body:
        achievement.name = body["name"]
    if "description" in body:
        achievement.description = body["description"]

    # Commit changes to the database
    db.session.commit()

    return achievement_schema.jsonify(achievement)  # Return the updated achievement


@achievement_controller.route("/achievements/<int:id>", methods=["DELETE"])
@jwt_required()  # Ensure the user is authenticated to delete an achievement
def delete_achievement(id):
    
    # Delete an achievement by its ID.

    # Arguments:
    #     - id: The ID of the achievement to delete.

    # Returns:
    #     - Success message if deleted, or error message if not found.
   
    achievement = Achievement.query.get(id)  # Retrieve the achievement by ID

    if not achievement:
        return {"message": "Achievement not found"}, 404  # Return error if not found

    # Delete the achievement from the database
    db.session.delete(achievement)
    db.session.commit()

    return {"message": "Achievement deleted successfully"}, 200  # Return success message