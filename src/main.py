# Import the create_app function from the application package
from init import create_app

# Create an instance of the Flask application by calling the create_app function
# This function sets up the app, initializes extensions, and registers blueprints
app = create_app()

if __name__ == "__main__":
    """
    The main entry point of the application.
    
    This block checks if this file is being run as a standalone script.
    If true, it will start the Flask development server.
    
    The `host='0.0.0.0'` makes the server publicly available, which is useful
    for testing from other devices on the network. The `port=5000` is the default 
    port for Flask applications. Setting `debug=True` enables debug mode, providing
    a more verbose output when errors occur and automatically reloading the server
    when code changes.
    """
    app.run(host='0.0.0.0', port=5000, debug=True)  # Start the app in debug mode