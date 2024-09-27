from init import db  # Import the database instance for SQLAlchemy
from models.session import Session, SessionSchema, session_schema, sessions_schema  # Import the Session model and schemas
from models.game import Game  # Import the Game model for validation
from flask import Blueprint, request, jsonify  # Import necessary components from Flask
from flask_jwt_extended import jwt_required  # JWT helper for authentication

# Create a Blueprint for session-related routes
session_bp = Blueprint('sessions', __name__, url_prefix='/api/sessions')

@session_bp.route("/", methods=["POST"])
@jwt_required()  # Protect this route with JWT authentication
def create_session():
    """
    Create a new game session in the database.

    Expects a JSON payload with 'game_id', 'max_players', and 'start_time'.
    
    If successful, returns the created session with a 201 status code.
    Returns a 400 status code if required fields are missing or validation fails.
    """
    json_data = request.get_json()  # Load the incoming JSON data

    # Extract the necessary fields from the JSON request
    game_id = json_data.get("game_id")
    max_players = json_data.get("max_players")

    # Check if required fields are provided
    if not game_id or not max_players:
        return {"message": "Missing game_id or max_players."}, 400  # Return error if fields are missing

    # Check if the associated game exists
    game = Game.query.get(game_id)
    if not game:
        return {"message": "Game not found."}, 404  # Return 404 if the game does not exist

    # Create a new Session instance
    new_session = Session(
        game_id=game_id,
        start_time=datetime.utcnow(),  # Set the start time to now
        max_players=max_players
    )

    # Add the new session to the database and commit changes
    db.session.add(new_session)
    db.session.commit()

    return session_schema.jsonify(new_session), 201  # Return the created session as JSON


@session_bp.route("/", methods=["GET"])
@jwt_required()  # Protect this route with JWT authentication
def get_sessions():
    """
    Retrieve a list of all game sessions in the database.

    Returns a JSON list of all sessions.
    """
    sessions = Session.query.all()  # Query all session records
    return sessions_schema.jsonify(sessions), 200  # Return the sessions as a JSON response


@session_bp.route("/<int:session_id>", methods=["GET"])
@jwt_required()  # Protect this route with JWT authentication
def get_session(session_id):
    """
    Retrieve a single session by its ID.

    Args:
    - session_id: The ID of the session to retrieve.

    Returns:
    A JSON representation of the session or a 404 error if not found.
    """
    session = Session.query.get(session_id)  # Attempt to retrieve the session by ID
    if session:
        return session_schema.jsonify(session), 200  # Return the session as JSON if found
    else:
        return {"message": "Session not found."}, 404  # Return 404 if the session does not exist


@session_bp.route("/<int:session_id>", methods=["PUT", "PATCH"])
@jwt_required()  # Protect this route with JWT authentication
def update_session(session_id):
    """
    Update an existing session by ID.

    Args:
    - session_id: The ID of the session to update.

    Expects a JSON payload with fields to update (optional).

    Returns:
    The updated session as JSON or a 404 error if the session is not found.
    """
    session = Session.query.get(session_id)  # Retrieve the session by ID
    if not session:
        return {"message": "Session not found."}, 404  # Return 404 if the session does not exist

    # Load the incoming data for updates, allowing for partial updates
    json_data = request.get_json()

    # Update the session's attributes based on the provided data
    if "max_players" in json_data:
        session.max_players = json_data["max_players"]
    if "end_time" in json_data:
        session.end_time = json_data["end_time"]  # Update end time if provided

    db.session.commit()  # Commit changes to the database

    return session_schema.jsonify(session), 200  # Return the updated session as JSON


@session_bp.route("/<int:session_id>", methods=["DELETE"])
@jwt_required()  # Protect this route with JWT authentication
def delete_session(session_id):
    """
    Delete a session by its ID.

    Args:
    - session_id: The ID of the session to delete.

    Returns:
    A success message or a 404 error if the session does not exist.
    """
    # Attempt to retrieve the session from the database using the provided session_id
    session = Session.query.get(session_id)

    # Check if the session exists
    if not session:
        return {"message": "Session not found."}, 404  # Return a 404 error if the session does not exist
    
    # Delete the session from the database
    db.session.delete(session)  # Mark the session for deletion
    db.session.commit()  # Commit the transaction to remove the session

    # Return a success message indicating the deletion was successful
    return {"message": "Session deleted successfully"}, 200  # Return a success message with a 200 status code