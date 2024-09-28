from flask import Blueprint  # Import Blueprint for grouping related functions
from init import db, bcrypt  # Import the database instance for SQLAlchemy and Bcrypt for password hashing

from models.user import User  # Import User model for creating demo users
from models.game import Game  # Import Game model for demo data
from models.genre import Genre  # Import Genre model for demo data
from models.developer import Developer  # Import Developer model for demo data

# Create a Blueprint for the database commands
db_commands = Blueprint("db_commands", __name__)

@db_commands.cli.command("create")
def create_db():
    """
    Create a new database. This involves creating all the tables that are
    defined in the models. This is a one-time operation and should be run
    only once, ideally when the application is first set up.
    """
    db.create_all()  # This creates all tables defined by your SQLAlchemy models
    print("Database created")

@db_commands.cli.command("drop")
def drop_db():
    """
    Drop all tables in the database.

    This command is used to delete all of the tables in the database.
    This is the opposite of the 'create' command, which creates the tables
    in the first place.
    
    This command is useful for starting over from scratch or for clearing
    out old data that is no longer needed.
    """
    db.drop_all()  # Call the `drop_all` method on the database
    print("Database dropped")  # Print a message letting the user know what happened

@db_commands.cli.command("seed")
def seed_db():
    """
    Populate the database with initial data. This is useful for setting up the database
    for the first time or for filling it with some sample data for testing purposes.
    """
    
    # Create initial genres for the game database
    genres = [
        Genre(name="Action"),
        Genre(name="Adventure"),
        Genre(name="RPG"),
        Genre(name="Strategy")
    ]
    
    # Add genres to the session and commit
    db.session.add_all(genres)
    db.session.commit()  # Commit to save the genres
    print("Genres added to the database")

    # Create initial developers
    developers = [
        Developer(name="Epic Games"),
        Developer(name="Blizzard Entertainment"),
        Developer(name="Ubisoft")
    ]
    
    # Add developers to the session and commit
    db.session.add_all(developers)
    db.session.commit()  # Commit to save the developers
    print("Developers added to the database")

    # Create some demo games associated with the created developers and genres
    games = [
        Game(
            title="Fortnite",
            genre_id=genres[0].id,  # Associate with Action genre
            developer_id=developers[0].id  # Associate with Epic Games
        ),
        Game(
            title="Overwatch",
            genre_id=genres[1].id,  # Associate with Adventure genre
            developer_id=developers[1].id  # Associate with Blizzard Entertainment
        ),
        Game(
            title="Assassin's Creed",
            genre_id=genres[2].id,  # Associate with RPG genre
            developer_id=developers[2].id  # Associate with Ubisoft
        )
    ]

    # Add games to the session and commit
    db.session.add_all(games)
    db.session.commit()  # Commit to save the games
    print("Games added to the database")

    # Create initial users, demonstrating the use of hashing
    users = [
        User(
            name="Admin User",
            email="admin@example.com",
            password=bcrypt.generate_password_hash("admin123").decode("utf-8")  # Hash the password
        ),
        User(
            name="Player One",
            email="player1@example.com",
            password=bcrypt.generate_password_hash("player123").decode("utf-8")  # Hash the password
        )
    ]

    # Add users to the session and commit
    db.session.add_all(users)
    db.session.commit()  # Commit to save the users
    print("Users added to the database")

    print("Database seeding completed")  # Print a message indicating seeding was successful