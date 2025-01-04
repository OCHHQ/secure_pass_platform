from dotenv import load_dotenv  # Import dotenv
import os

# Load environment variables from .env
load_dotenv()

from app import create_app  # Import create_app after loading environment variables

app = create_app()  # Create the Flask app instance

if __name__ == '__main__':
    app.run(debug=True)  # Run the app in debug mode
