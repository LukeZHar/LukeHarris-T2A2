from init import db  # Import the database instance for SQLAlchemy
from models.game import Game, game_schema, games_schema  # Import the Game model and schema
from flask import Blueprint, request, jsonify  # Import necessary components from Flask
from flask_jwt_extended import jwt_required  # JWT authentication helper

# Create a Blueprint for game-related routes
game_bp = Blueprint('games', __name__, url_prefix='/api/games')

@game_bp.route("/", methods=["POST"])
@jwt_required()  # Protect this route with JWT authentication
def create_game():
    """
    Create a new game in the database.

    Expects a JSON payload with 'name', 'description', 'release_date', 'genre_id', and 'developer_id'.

    If successful, returns the created game with a 201 status code.
    Returns a 400 status code if there are validation errors.
    """
    # Load the incoming JSON data
    json_data = request.get_json()
    
    # Extract data from JSON request
    name = json_data.get("name")
    description = json_data.get("description")
    release_date = json_data.get("release_date")
    genre_id = json_data.get("genre_id")
    developer_id = json_data.get("developer_id")

    # Validate that all required fields are provided
    if not name or not genre_id or not developer_id:
        return {"message": "Missing required fields: name, genre_id, and developer_id."}, 400

    # Create a new Game instance
    new_game = Game(
        name=name,
        description=description,
        release_date=release_date,
        genre_id=genre_id,
        developer_id=developer_id
    )

    # Add the new game to the session and commit the transaction
    db.session.add(new_game)
    db.session.commit()

    return game_schema.jsonify(new_game), 201  # Return the created game as JSON


@game_bp.route("/", methods=["GET"])
@jwt_required()  # Protect this route with JWT authentication
def get_all_games():
    """
    Retrieve a list of all games in the database.

    Returns a JSON list of all games.
    """
    games = Game.query.all()  # Query all games from the database
    return games_schema.jsonify(games), 200  # Return the games as a JSON response


@game_bp.route("/<int:game_id>", methods=["GET"])
@jwt_required()  # Protect this route with JWT authentication
def get_game(game_id):
    """
    Retrieve a single game by its ID.

    Args:
    - game_id: The ID of the game to retrieve.

    Returns:
    A JSON representation of the game or a 404 error if not found.
    """
    game = Game.query.get(game_id)  # Attempt to retrieve the game by ID
    if game:
        return game_schema.jsonify(game), 200  # Return the game as JSON if found
    else:
        return {"message": "Game not found."}, 404  # Return 404 if the game does not exist


@game_bp.route("/<int:game_id>", methods=["PUT", "PATCH"])
@jwt_required()  # Protect this route with JWT authentication
def update_game(game_id):
    """
    Update an existing game by ID.

    Args:
    - game_id: The ID of the game to update.

    Expects a JSON payload with fields to update (optional).

    Returns:
    The updated game as JSON or a 404 error if the game is not found.
    """
    game = Game.query.get(game_id)  # Retrieve the game by ID
    if not game:
        return {"message": "Game not found."}, 404  # Return 404 if the game does not exist

    # Load the incoming data for updates, allowing for partial updates
    json_data = request.get_json()

    # Update the game attributes based on the provided data
    if "name" in json_data:
        game.name = json_data["name"]
    if "description" in json_data:
        game.description = json_data["description"]
    if "release_date" in json_data:
        game.release_date = json_data["release_date"]
    if "genre_id" in json_data:
        game.genre_id = json_data["genre_id"]
    if "developer_id" in json_data:
        game.developer_id = json_data["developer_id"]

    db.session.commit()  # Commit changes to the database

    return game_schema.jsonify(game), 200  # Return the updated game as JSON

@game_bp.route("/<int:game_id>", methods=["DELETE"])
@jwt_required()  # Protect this route with JWT authentication
def delete_game(game_id):
    """
    Delete a game by its ID.

    Args:
    - game_id: The ID of the game to delete.

    Returns:
    A success message or a 404 error if the game does not exist.
    """
    # Attempt to retrieve the game from the database using the provided game_id
    game = Game.query.get(game_id)
    
    # Check if the game exists
    if not game:
        return {"message": "Game not found."}, 404  # Return a 404 error if the game does not exist
    
    # Delete the game from the database
    db.session.delete(game)  # Mark the game for deletion
    db.session.commit()  # Commit the transaction to remove the game

    # Return a success message confirming the deletion
    return {"message": "Game deleted successfully"}, 200  # Return a success message with a 200 status