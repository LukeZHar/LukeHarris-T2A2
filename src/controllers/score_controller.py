from init import db  # Import the database instance for SQLAlchemy
from models.score import Score, score_schema, scores_schema  # Import the Score model and schemas
from models.session import Session  # Import the Session model for validation
from flask import Blueprint, request, jsonify  # Import necessary components from Flask
from flask_jwt_extended import jwt_required  # JWT helper for authentication

# Create a Blueprint for score-related routes
score_bp = Blueprint('scores', __name__, url_prefix='/api/scores')

@score_bp.route("/", methods=["POST"])
@jwt_required()  # Protect this route with JWT authentication
def create_score():
    """
    Create a new score in the database.

    Expects a JSON payload with 'user_id', 'session_id', and 'score_value'.
    
    If successful, returns the created score with a 201 status code.
    Returns a 400 status code if there are validation errors.
    """
    json_data = request.get_json()  # Load the incoming JSON data

    # Extract the necessary fields from the JSON request
    user_id = json_data.get("user_id")
    session_id = json_data.get("session_id")
    score_value = json_data.get("score_value")

    # Validate that all required fields are provided
    if not user_id or not session_id or score_value is None:
        return {"message": "Missing user_id, session_id, or score_value."}, 400  # Return error if fields are missing

    # Check if the associated session exists
    session = Session.query.get(session_id)
    if not session:
        return {"message": "Session not found."}, 404  # Return 404 if the session does not exist

    # Create a new Score instance
    new_score = Score(
        user_id=user_id,
        session_id=session_id,
        score_value=score_value
    )

    # Add the new score to the database session and commit
    db.session.add(new_score)
    db.session.commit()  # Commit the transaction

    return score_schema.jsonify(new_score), 201  # Return the created score as JSON


@score_bp.route("/", methods=["GET"])
@jwt_required()  # Protect this route with JWT authentication
def get_all_scores():
    """
    Retrieve a list of all scores in the database.

    Returns a JSON list of all scores.
    """
    scores = Score.query.all()  # Query all score records from the database
    return scores_schema.jsonify(scores), 200  # Return the scores as a JSON response


@score_bp.route("/<int:score_id>", methods=["GET"])
@jwt_required()  # Protect this route with JWT authentication
def get_score(score_id):
    """
    Retrieve a single score by its ID.

    Args:
    - score_id: The ID of the score to retrieve.

    Returns:
    A JSON representation of the score or a 404 error if not found.
    """
    score = Score.query.get(score_id)  # Attempt to retrieve the score by ID
    if score:
        return score_schema.jsonify(score), 200  # Return the score as JSON if found
    else:
        return {"message": "Score not found."}, 404  # Return 404 if the score does not exist


@score_bp.route("/<int:score_id>", methods=["PUT", "PATCH"])
@jwt_required()  # Protect this route with JWT authentication
def update_score(score_id):
    """
    Update an existing score by ID.

    Args:
    - score_id: The ID of the score to update.

    Expects a JSON payload with fields to update (optional).

    Returns:
    The updated score as JSON or a 404 error if the score is not found.
    """
    score = Score.query.get(score_id)  # Retrieve the score by ID
    if not score:
        return {"message": "Score not found."}, 404  # Return 404 if the score does not exist

    # Load the incoming data for updates, allowing for partial updates
    json_data = request.get_json()

    # Update the score_value if it is provided in the request
    if "score_value" in json_data:
        score.score_value = json_data["score_value"]

    db.session.commit()  # Commit changes to the database

    return score_schema.jsonify(score), 200  # Return the updated score as JSON

@score_bp.route("/<int:score_id>", methods=["DELETE"])
@jwt_required()  # Protect this route with JWT authentication
def delete_score(score_id):
    """
    Delete a score by its ID.

    Args:
    - score_id: The ID of the score to delete.

    Returns:
    A success message or a 404 error if the score does not exist.
    """
    # Attempt to retrieve the score from the database using the provided score_id
    score = Score.query.get(score_id)

    # Check if the score exists
    if not score:
        return {"message": "Score not found."}, 404  # Return a 404 error if the score does not exist
    
    # Delete the score from the database
    db.session.delete(score)  # Mark the score for deletion
    db.session.commit()  # Commit the transaction to remove the score

    # Return a success message indicating the deletion was successful
    return {"message": "Score deleted successfully."}, 200  # Return a success message with a 200 status code