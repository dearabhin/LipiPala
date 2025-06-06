import logging
from flask import Flask
from lipipala.config import settings
from lipipala.api.v1.routes import api_v1_bp


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config.from_object(settings)

    # Configure logging
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Register blueprints
    app.register_blueprint(api_v1_bp)

    logging.info(f"{settings.app_name} v{settings.version} initialized.")
    return app
