import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()


def create_app() -> Flask:
    """Application factory for creating Flask app instances."""
    app = Flask(__name__)
    config_name = os.getenv('FLASK_ENV', 'development')
    app.config.from_object(config[config_name])

    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route('/')
    def index() -> dict[str, object]:
        """Root endpoint providing API information."""
        return {
            'message': 'Project Management API',
            'endpoints': {
                'users': '/users',
                'projects': '/projects',
                'tasks': '/projects/<id>/tasks',
            },
        }

    @app.errorhandler(404)
    def not_found(_error: Exception) -> tuple[dict[str, str], int]:
        """Handle 404 errors."""
        return {'error': 'Resource not found'}, 404

    @app.errorhandler(500)
    def internal_error(_error: Exception) -> tuple[dict[str, str], int]:
        """Handle 500 errors."""
        return {'error': 'Internal server error'}, 500

    return app
