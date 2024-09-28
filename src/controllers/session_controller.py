from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db  # Import the database instance
from models.session import Session, session_schema, sessions_schema  # Import Session model and schemas

# Create a Blueprint for session-related routes
session_controller = Blueprint("session_controller", __name__)

@session_controller.route("/sessions", methods=["POST"])
@jwt_required()  # Ensure the user is authenticated to create a session
def create_session():
    """
    Create a new gaming session.

    Expects:
    - JSON payload with 'start_time', 'game_id', and optionally 'end_time'.

    Returns:
    - JSON representation of the newly created session.
    """
    body = request.json  # Get JSON payload from the request

    # Get the current user's ID from the JWT
    user_id = get_jwt_identity()

    # Create a new session instance with the provided data
    new_session = Session(
        start_time=body.get("start_time", None),
        user_id=user_id,
        game_id=body.get("game_id", None),
        end_time=body.get("end_time", None)  # end_time can be optional while creating the session
    )

    # Add the new session to the database session and commit
    db.session.add(new_session)
    db.session.commit()

    return session_schema.jsonify(new_session), 201  # Return the created session with a 201 status


@session_controller.route("/sessions", methods=["GET"])
@jwt_required()  # Ensure the user is authenticated to retrieve sessions
def get_sessions():
    """
    Retrieve all gaming sessions for the authenticated user.

    Returns:
    - JSON list of sessions tied to the current user.
    """
    user_id = get_jwt_identity()  # Get the current user's ID from the JWT

    # Query all sessions associated with the current user
    sessions = Session.query.filter_by(user_id=user_id).all()

    return sessions_schema.jsonify(sessions)  # Return the list of sessions


@session_controller.route("/sessions/<int:id>", methods=["GET"])
@jwt_required()  # Ensure the user is authenticated to access this route
def get_session(id):
    """
    Retrieve a specific gaming session by ID.

    Arguments:
    - id: The ID of the session to retrieve.

    Returns:
    - JSON representation of the session if found.
    - Error message if the session is not found or unauthorised.
    """
    session = Session.query.get(id)  # Retrieve session by ID

    if not session:
        return {"message": "Session not found"}, 404  # Return error if not found

    # Ensure that the authenticated user owns the session
    if session.user_id != get_jwt_identity():
        return {"message": "Unauthorised"}, 401

    return session_schema.jsonify(session)  # Return the found session


@session_controller.route("/sessions/<int:id>", methods=["DELETE"])
@jwt_required()  # Ensure the user is authenticated to delete a session
def delete_session(id):
    """
    Delete a gaming session by its ID.

    Arguments:
    - id: The ID of the session to delete.

    Returns:
    - Success message if deleted, or error message if not found/unauthorized.
    """
    session = Session.query.get(id)  # Retrieve the session by ID

    if not session:
        return {"message": "Session not found"}, 404  # Return error if not found

    # Ensure that the authenticated user owns the session before deletion
    if session.user_id != get_jwt_identity():
        return {"message": "Unauthorised"}, 401

    # Delete the session from the database
    db.session.delete(session)
    db.session.commit()

    return {"message": "Session deleted successfully"}, 200  # Return success message