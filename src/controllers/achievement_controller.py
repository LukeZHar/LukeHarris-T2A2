from init import db  # Import the database instance for SQLAlchemy
from models.achievement import Achievement, achievement_schema, achievements_schema  # Import the Achievement model and schemas
from models.game import Game  # Import the Game model for validation
from flask import Blueprint, request, jsonify  # Import necessary components from Flask
from flask_jwt_extended import jwt_required  # JWT helper for authentication

# Create a Blueprint for achievement-related routes
achievement_bp = Blueprint('achievements', __name__, url_prefix='/api/achievements')

@achievement_bp.route("/", methods=["POST"])
@jwt_required()  # Protect this route with JWT authentication
def create_achievement():
    """
    Create a new achievement for a specific game in the database.

    Expects a JSON payload with 'game_id', 'title', and 'description'.
    
    If successful, returns the created achievement with a 201 status code.
    Returns a 400 status code if there are validation errors (e.g., game does not exist).
    """
    json_data = request.get_json()  # Load the incoming JSON data

    # Extract necessary fields from the JSON request
    game_id = json_data.get("game_id")
    title = json_data.get("title")
    description = json_data.get("description")

    # Validate if game_id, title, and description are provided
    if not game_id or not title:
        return {"message": "Missing game_id or title."}, 400  # Error if missing fields

    # Check if the associated game exists
    game = Game.query.get(game_id)
    if not game:
        return {"message": "Game not found."}, 404  # Return 404 if the game does not exist

    # Create a new Achievement instance
    new_achievement = Achievement(
        game_id=game_id,
        title=title,
        description=description
    )

    # Add the new achievement to the database session
    db.session.add(new_achievement)
    db.session.commit()  # Commit the transaction to save the new achievement

    return achievement_schema.jsonify(new_achievement), 201  # Return the created achievement as JSON


@achievement_bp.route("/", methods=["GET"])
def get_all_achievements():
    """
    Retrieve a list of all achievements in the database.

    Returns a JSON list of all achievements.
    """
    achievements = Achievement.query.all()  # Query all achievements from the database
    return achievements_schema.jsonify(achievements), 200  # Return the achievements as a JSON response


@achievement_bp.route("/<int:achievement_id>", methods=["GET"])
def get_achievement(achievement_id):
    """
    Retrieve a single achievement by its ID.

    Args:
    - achievement_id: The ID of the achievement to retrieve.

    Returns:
    A JSON representation of the achievement or a 404 error if not found.
    """
    achievement = Achievement.query.get(achievement_id)  # Attempt to retrieve the achievement by ID
    if achievement:
        return achievement_schema.jsonify(achievement), 200  # Return the achievement as JSON if found
    else:
        return {"message": "Achievement not found."}, 404  # Return 404 if the achievement does not exist


@achievement_bp.route("/<int:achievement_id>", methods=["PUT", "PATCH"])
@jwt_required()  # Protect this route with JWT authentication
def update_achievement(achievement_id):
    """
    Update an existing achievement by ID.

    Args:
    - achievement_id: The ID of the achievement to update.

    Expects a JSON payload with fields to update.

    Returns:
    The updated achievement as JSON or a 404 error if the achievement is not found.
    """
    achievement = Achievement.query.get(achievement_id)  # Retrieve the achievement by ID
    if not achievement:
        return {"message": "Achievement not found."}, 404  # Return 404 if the achievement does not exist

    # Load the incoming data for updates, allowing for partial updates
    json_data = request.get_json()

    # Update the achievement fields based on the provided data
    if "title" in json_data:
        achievement.title = json_data["title"]
    if "description" in json_data:
        achievement.description = json_data["description"]

    db.session.commit()  # Commit changes to the database

    return achievement_schema.jsonify(achievement), 200  # Return the updated achievement as JSON

@achievement_bp.route("/<int:achievement_id>", methods=["DELETE"])
@jwt_required()  # Protect this route with JWT authentication
def delete_achievement(achievement_id):
    """
    Delete an achievement by its ID.

    Args:
    - achievement_id: The ID of the achievement to delete.

    Returns:
    A success message or a 404 error if the achievement does not exist.
    """
    # Attempt to retrieve the achievement from the database using the provided achievement_id
    achievement = Achievement.query.get(achievement_id)

    # Check if the achievement exists
    if not achievement:
        return {"message": "Achievement not found."}, 404  # Return a 404 error if the achievement does not exist
    
    # Delete the achievement from the database
    db.session.delete(achievement)  # Mark the achievement for deletion
    db.session.commit()  # Commit the transaction to remove the achievement

    # Return a success message indicating the deletion was successful
    return {"message": "Achievement deleted successfully."}, 200  # Return a success message with a 200 status code