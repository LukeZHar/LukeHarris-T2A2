from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db  # Import the database instance
from models.score import Score, score_schema, scores_schema  # Import Score model and schemas

# Create a Blueprint for score-related routes
score_controller = Blueprint("score_controller", __name__)

@score_controller.route("/scores", methods=["POST"])
@jwt_required()  # Ensure the user is authenticated to create a score
def create_score():
    
    # Create a new score for a specific game.

    # Expects:
    # - JSON payload with 'value' and 'game_id'.
    
    # Returns:
    # - JSON representation of the newly created score on success.
    
    body = request.json  # Get JSON payload from the request

    # Get the current user's ID from the JWT
    user_id = get_jwt_identity()

    # Create a new score instance
    new_score = Score(
        value=body.get("value"),  # The score value
        user_id=user_id,
        game_id=body.get("game_id")  # The game with which this score is associated
    )

    # Add the new score to the database session and commit
    db.session.add(new_score)
    db.session.commit()

    return score_schema.jsonify(new_score), 201  # Return the created score with a 201 status


@score_controller.route("/scores", methods=["GET"])
@jwt_required()  # Ensure the user is authenticated to retrieve scores
def get_scores():
    
    # Retrieve all scores for the authenticated user.

    # Returns:
    # - JSON list of scores tied to the current user.
    
    user_id = get_jwt_identity()  # Get the current user's ID from the JWT

    # Query all scores associated with the current user
    scores = Score.query.filter_by(user_id=user_id).all()

    return scores_schema.jsonify(scores)  # Return the list of user scores


@score_controller.route("/scores/<int:id>", methods=["GET"])
@jwt_required()  # Ensure the user is authenticated to access this route
def get_score(id):
    
    # Retrieve a specific score by ID.

    # Arguments:
    # - id: The ID of the score to retrieve.

    # Returns:
    # - JSON representation of the score if found.
    # - Error message if the score is not found or unauthorized.
    
    score = Score.query.get(id)  # Retrieve score by ID

    if not score:
        return {"message": "Score not found"}, 404  # Return error if not found

    # Ensure that the authenticated user owns the score
    if score.user_id != get_jwt_identity():
        return {"message": "Unauthorized"}, 401

    return score_schema.jsonify(score)  # Return the found score


@score_controller.route("/scores/<int:id>", methods=["DELETE"])
@jwt_required()  # Ensure the user is authenticated to delete a score
def delete_score(id):
    
    # Delete a score by its ID.

    # Arguments:
    # - id: The ID of the score to delete.

    # Returns:
    # - Success message if deleted, or error message if not found/unauthorized.
    
    score = Score.query.get(id)  # Retrieve the score by ID

    if not score:
        return {"message": "Score not found"}, 404  # Return error if not found

    # Ensure that the authenticated user owns the score before deletion
    if score.user_id != get_jwt_identity():
        return {"message": "Unauthorized"}, 401

    # Delete the score from the database
    db.session.delete(score)
    db.session.commit()

    return {"message": "Score deleted successfully"}, 200  # Return success message