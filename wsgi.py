"""WSGI entry point for PythonAnywhere deployment."""
import os
from pathlib import Path
from app import create_app

# Load environment variables from appropriate .env file
try:
    from dotenv import load_dotenv

    # Determine which environment file to load
    # Priority: FLASK_CONFIG env var > FLASK_ENV env var > default to production
    config_name = os.environ.get('FLASK_CONFIG') or os.environ.get('FLASK_ENV', 'production')

    # Load the appropriate .env file
    if config_name == 'production':
        env_file = Path(__file__).parent / '.env.production'
        if env_file.exists():
            load_dotenv(env_file)
        else:
            # Fallback to .env if .env.production doesn't exist
            load_dotenv()
    else:
        # For development/testing, use .env
        load_dotenv()

except ImportError:
    pass

# Create application instance
config_name = os.environ.get('FLASK_CONFIG') or os.environ.get('FLASK_ENV', 'production')
application = create_app(config_name)

if __name__ == '__main__':
    application.run(host='127.0.0.1', port=5001, debug=True)
