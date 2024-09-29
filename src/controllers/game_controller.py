from flask import Blueprint, request
from flask_jwt_extended import jwt_required  # To enforce user authentication
from init import db  # Import the database instance
from models.game import Game, game_schema, games_schema  # Import Game model and schemas
from models.genre import Genre  # Import Genre model to validate genre ID
from models.developer import Developer  # Import Developer model to validate developer ID

# Create a Blueprint for game-related routes
game_controller = Blueprint("game_controller", __name__)

@game_controller.route("/games", methods=["POST"])
@jwt_required()  # Ensure the user is authenticated to create a game
def create_game():
    
    # Create a new game.

    # Expects:
    #     - JSON payload with 'title', 'genre_id', and 'developer_id'.
    
    # Returns:
    #     - JSON representation of the newly created game.
    #     - Error message if genre or developer does not exist.
   
    body = request.json  # Get JSON payload from the request

    # Validate existence of genre and developer
    genre_id = body.get("genre_id")
    developer_id = body.get("developer_id")

    # Check if the provided genre_id exists
    genre = Genre.query.get(genre_id)
    if not genre:
        return {"message": "Genre not found"}, 404

    # Check if the provided developer_id exists
    developer = Developer.query.get(developer_id)
    if not developer:
        return {"message": "Developer not found"}, 404

    # Create a new game instance
    new_game = Game(
        title=body.get("title"),  # The title of the game
        genre_id=genre_id,  # Associate with the verified genre
        developer_id=developer_id  # Associate with the verified developer
    )

    # Add the new game to the database and commit the changes
    db.session.add(new_game)
    db.session.commit()

    return game_schema.jsonify(new_game), 201  # Return the created game with a 201 status


@game_controller.route("/games", methods=["GET"])
def get_games():
    
    # Retrieve all games.

    # Returns:
    #     - JSON list of all games in the database.
    
    games = Game.query.all()  # Retrieve all games from the database
    return games_schema.jsonify(games)  # Return the list of games


@game_controller.route("/games/<int:id>", methods=["GET"])
def get_game(id):
    
    # Retrieve a specific game by ID.

    # Arguments:
    #     - id: The ID of the game to retrieve.

    # Returns:
    #     - JSON representation of the game if found.
    #     - Error message if the game is not found.
    
    game = Game.query.get(id)  # Retrieve game by ID

    if not game:
        return {"message": "Game not found"}, 404  # Return error if not found

    return game_schema.jsonify(game)  # Return the found game


@game_controller.route("/games/<int:id>", methods=["PUT", "PATCH"])
@jwt_required()  # Ensure the user is authenticated to update a game
def update_game(id):
    
    # Update an existing game's information.

    # Arguments:
    #     - id: The ID of the game to update.

    # Expects:
    #     - JSON payload with fields to update such as 'title', 'genre_id', or 'developer_id'.

    # Returns:
    #     - JSON representation of the updated game if successful.
    #     - Error message if game is not found.
    
    game = Game.query.get(id)  # Retrieve the game by ID

    if not game:
        return {"message": "Game not found"}, 404  # Return error if the game does not exist

    body = request.json  # Get JSON payload for updates

    # Update fields based on the provided data in the request body
    if "title" in body:
        game.title = body["title"]  # Update the title of the game
    if "genre_id" in body:
        game.genre_id = body["genre_id"]  # Update the genre ID
    if "developer_id" in body:
        game.developer_id = body["developer_id"]  # Update the developer ID

    # Commit changes to the database
    db.session.commit()

    return game_schema.jsonify(game)  # Return the updated game


@game_controller.route("/games/<int:id>", methods=["DELETE"])
@jwt_required()  # Ensure the user is authenticated to delete a game
def delete_game(id):
    
    # Delete a game by its ID.

    # Arguments:
    #     - id: The ID of the game to delete.

    # Returns:
    #     - Success message if deleted, or error message if not found.
    
    game = Game.query.get(id)  # Retrieve the game by ID

    if not game:
        return {"message": "Game not found"}, 404  # Return error if the game does not exist

    # Delete the game from the database
    db.session.delete(game)
    db.session.commit()

    return {"message": "Game deleted successfully"}, 200  # Return success message