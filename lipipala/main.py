#!/usr/bin/env python
"""
LipiPala AI - Main Application Entry Point

This module serves as the entry point for the LipiPala AI application,
initializing components and starting the web service for language preservation.
"""

import os
import logging
import argparse
from pathlib import Path
from flask import Flask, render_template, jsonify

from lipipala.config import get_config
from lipipala.api.routes import register_api_routes
from lipipala.core.data_collection import DataCollectionService
from lipipala.core.speech_recognition import SpeechRecognitionService
from lipipala.core.translation import TranslationService
from lipipala.core.language_learning import LanguageLearningService
from lipipala.db.operations import initialize_database

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("lipipala.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create Flask application
app = Flask(__name__,
            static_folder='static',
            template_folder='templates')


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='LipiPala AI Server')
    parser.add_argument('--debug', action='store_true',
                        help='Run in debug mode')
    parser.add_argument('--port', type=int, default=5000,
                        help='Port to run the server on')
    parser.add_argument('--host', type=str, default='0.0.0.0',
                        help='Host to run the server on')
    parser.add_argument('--config', type=str,
                        default='config.yaml', help='Path to config file')
    return parser.parse_args()


def initialize_app():
    """Initialize application components."""
    logger.info("Initializing LipiPala AI...")

    # Load configuration
    config = get_config()
    app.config.update(config)

    # Initialize database
    initialize_database(app)

    # Initialize core services
    app.data_collection = DataCollectionService(config['data_collection'])
    app.speech_recognition = SpeechRecognitionService(
        config['speech_recognition'])
    app.translation = TranslationService(config['translation'])
    app.language_learning = LanguageLearningService(
        config['language_learning'])

    # Register API routes
    register_api_routes(app)

    # Register main routes
    register_main_routes(app)

    logger.info("LipiPala AI initialization complete")
    return app


def register_main_routes(app):
    """Register main application routes."""

    @app.route('/')
    def index():
        """Render the main page."""
        supported_languages = app.speech_recognition.get_supported_languages()
        return render_template('index.html',
                               languages=supported_languages,
                               version=app.config['version'])

    @app.route('/dashboard')
    def dashboard():
        """Render the dashboard page."""
        stats = {
            'languages': app.speech_recognition.get_supported_languages(),
            'recordings': app.data_collection.get_stats(),
            'translations': app.translation.get_stats(),
            'users': app.language_learning.get_user_stats()
        }
        return render_template('dashboard.html', stats=stats)

    @app.route('/health')
    def health_check():
        """Health check endpoint."""
        services_status = {
            'data_collection': app.data_collection.is_healthy(),
            'speech_recognition': app.speech_recognition.is_healthy(),
            'translation': app.translation.is_healthy(),
            'language_learning': app.language_learning.is_healthy(),
            'database': app.db.is_healthy() if hasattr(app, 'db') else False
        }

        all_healthy = all(services_status.values())

        return jsonify({
            'status': 'healthy' if all_healthy else 'unhealthy',
            'services': services_status,
            'version': app.config['version']
        }), 200 if all_healthy else 503


def main():
    """Main entry point for the application."""
    args = parse_arguments()

    # Set configuration path
    os.environ['LIPIPALA_CONFIG'] = args.config

    # Initialize the application
    app = initialize_app()

    # Run the application
    logger.info(f"Starting LipiPala AI server on {args.host}:{args.port}")
    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == '__main__':
    main()
