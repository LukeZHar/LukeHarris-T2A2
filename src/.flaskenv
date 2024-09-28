# .flaskenv configuration file
# This file is used by Flask commands to set various environment settings for the application

# Specifies the entry point for the Flask application
# This should be the module or package containing your Flask application instance
FLASK_APP=main

# Enables or disables debug mode.
# In development, it's useful to have this enabled (1) for better error messages and reloader functionality
# In production, set this to 0 to ensure the application runs in production mode
FLASK_DEBUG=1

# Specifies the port on which the Flask development server will run
# The default port is 5000 if not specified, but you can set it to any open port
FLASK_RUN_PORT=8080
