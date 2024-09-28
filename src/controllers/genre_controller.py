from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from init import db  # Import the database instance
from models.genre import Genre, genre_schema, genres_schema  # Import Genre model and schemas

# Create a Blueprint for genre-related routes
genre_controller = Blueprint("genre_controller", __name__)

@genre_controller.route("/genres", methods=["POST"])
@jwt_required()  # Ensure the user is authenticated to create a genre
def create_genre():
    """
    Create a new genre.

    Expects:
    - JSON payload with 'name'.
    
    Returns:
    - JSON representation of the newly created genre.
    """
    body = request.json  # Get JSON payload from the request

    # Create a new genre instance
    new_genre = Genre(
        name=body.get("name")  # The name of the genre
    )

    # Add the new genre to the database and commit the changes
    db.session.add(new_genre)
    db.session.commit()

    return genre_schema.jsonify(new_genre), 201  # Return the created genre with a 201 status


@genre_controller.route("/genres", methods=["GET"])
def get_genres():
    """
    Retrieve all genres.

    Returns:
    - JSON list of all genres in the database.
    """
    genres = Genre.query.all()  # Retrieve all genres
    return genres_schema.jsonify(genres)  # Return the list of genres


@genre_controller.route("/genres/<int:id>", methods=["GET"])
def get_genre(id):
    """
    Retrieve a specific genre by ID.

    Arguments:
    - id: The ID of the genre to retrieve.

    Returns:
    - JSON representation of the genre if found.
    - Error message if the genre is not found.
    """
    genre = Genre.query.get(id)  # Retrieve genre by ID
    
    if not genre:
        return {"message": "Genre not found"}, 404  # Return error if not found

    return genre_schema.jsonify(genre)  # Return the found genre


@genre_controller.route("/genres/<int:id>", methods=["PUT", "PATCH"])
@jwt_required()  # Ensure the user is authenticated to update a genre
def update_genre(id):
    """
    Update an existing genre by ID.

    Arguments:
    - id: The ID of the genre to update.

    Expects:
    - JSON payload with 'name' to update.

    Returns:
    - JSON representation of the updated genre if successful.
    - Error message if genre not found.
    """
    genre = Genre.query.get(id)  # Retrieve the genre by ID

    if not genre:
        return {"message": "Genre not found"}, 404  # Return error if not found

    body = request.json  # Get JSON payload for updates

    # Update the name of the genre if provided
    if "name" in body:
        genre.name = body["name"]

    # Commit changes to the database
    db.session.commit()

    return genre_schema.jsonify(genre)  # Return updated genre


@genre_controller.route("/genres/<int:id>", methods=["DELETE"])
@jwt_required()  # Ensure the user is authenticated to delete a genre
def delete_genre(id):
    """
    Delete a genre by its ID.

    Arguments:
    - id: The ID of the genre to delete.

    Returns:
    - Success message if deleted, or error message if not found.
    """
    genre = Genre.query.get(id)  # Retrieve the genre by ID

    if not genre:
        return {"message": "Genre not found"}, 404  # Return error if not found

    # Delete the genre from the database
    db.session.delete(genre)
    db.session.commit()

    return {"message": "Genre deleted successfully"}, 200  # Return success message