import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.logging_config import setup_logging
from config import config

db = SQLAlchemy()


def create_app() -> Flask:
    """Application factory for creating Flask app instances."""
    app = Flask(__name__)
    setup_logging()
    app.logger.info('App initialized.')

    config_name = os.getenv('FLASK_ENV', 'development')
    app.config.from_object(config[config_name])

    db.init_app(app)

    from app.projects import project_bp
    from app.tasks import task_bp
    from app.users import user_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(task_bp)

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
        db.session.rollback()
        return {'error': 'Internal server error'}, 500

    return app
