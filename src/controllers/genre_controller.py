from init import db  # Import the database instance for SQLAlchemy
from models.genre import Genre, genre_schema, genres_schema  # Import the Genre model and schemas
from flask import Blueprint, request, jsonify  # Import necessary components from Flask
from flask_jwt_extended import jwt_required  # JWT helper for authentication

# Create a Blueprint for genre-related routes
genre_bp = Blueprint('genres', __name__, url_prefix='/api/genres')

@genre_bp.route("/", methods=["POST"])
@jwt_required()  # Protect this route with JWT authentication
def create_genre():
    """
    Create a new genre in the database.

    Expects a JSON payload with 'name'.
    
    If successful, returns the created genre with a 201 status code.
    Returns a 400 status code if there are validation errors.
    """
    # Load the incoming JSON data from the request
    json_data = request.get_json()
    
    # Extract the genre name from the JSON request
    name = json_data.get("name")

    # Validate that the name is provided
    if not name:
        return {"message": "Missing genre name."}, 400  # Return 400 if no name is provided

    # Check for the existence of an existing genre with the same name
    if Genre.query.filter_by(name=name).first():
        return {"message": "Genre already exists."}, 400  # Conflict if genre already exists

    # Create a new Genre instance
    new_genre = Genre(name=name)

    # Add the new genre to the database session
    db.session.add(new_genre)
    db.session.commit()  # Commit the transaction to save the new genre

    return genre_schema.jsonify(new_genre), 201  # Return the created genre as JSON


@genre_bp.route("/", methods=["GET"])
def get_all_genres():
    """
    Retrieve a list of all genres in the database.

    Returns a JSON list of all genres.
    """
    genres = Genre.query.all()  # Query all genres from the database
    return genres_schema.jsonify(genres), 200  # Return the genres as a JSON response


@genre_bp.route("/<int:genre_id>", methods=["GET"])
def get_genre(genre_id):
    """
    Retrieve a single genre by its ID.

    Args:
    - genre_id: The ID of the genre to retrieve.

    Returns:
    A JSON representation of the genre or a 404 error if not found.
    """
    genre = Genre.query.get(genre_id)  # Attempt to retrieve the genre by ID
    if genre:
        return genre_schema.jsonify(genre), 200  # Return the genre as JSON if found
    else:
        return {"message": "Genre not found."}, 404  # Return 404 if the genre does not exist


@genre_bp.route("/<int:genre_id>", methods=["PUT", "PATCH"])
@jwt_required()  # Protect this route with JWT authentication
def update_genre(genre_id):
    """
    Update an existing genre by ID.

    Args:
    - genre_id: The ID of the genre to update.

    Expects a JSON payload with fields to update.

    Returns:
    The updated genre as JSON or a 404 error if the genre is not found.
    """
    genre = Genre.query.get(genre_id)  # Retrieve the genre by ID
    if not genre:
        return {"message": "Genre not found."}, 404  # Return 404 if the genre does not exist

    # Load the incoming data for updates, allowing for partial updates
    body = request.get_json()

    if "name" in body:
        genre.name = body["name"]  # Update the genre name

    db.session.commit()  # Commit changes to the database

    return genre_schema.jsonify(genre), 200  # Return the updated genre as JSON


@genre_bp.route("/<int:genre_id>", methods=["DELETE"])
@jwt_required()  # Protect this route with JWT authentication
def delete_genre(genre_id):
    """
    Delete a genre by its ID.

    Args:
    - genre_id: The ID of the genre to delete.

    Returns:
    A success message or a 404 error if the genre does not exist.
    """
    genre = Genre.query.get(genre_id)  # Attempt to retrieve the genre by ID
    if not genre:
        return {"message": "Genre not found."}, 404  # Return a 404 error if genre not found
    
    # Delete the genre from the database
    db.session.delete(genre)
    db.session.commit()  # Commit the transaction

    return {"message": "Genre deleted successfully"}, 200