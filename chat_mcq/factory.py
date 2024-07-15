import logging

from flask import Flask
from flask.logging import default_handler

from .extensions import db


def create_app():
    """
    Create and configure the Flask application.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object("chat_mcq.config")

    configure_logging(app)
    configure_extensions(app)
    register_blueprints(app)

    return app


def configure_logging(app: Flask):
    """
    Configure logging for the Flask application.

    Args:
        app (Flask): The Flask application instance.
    """
    # Add default handler.
    app.logger.addHandler(default_handler)

    # Set logging level for the Flask app.
    logging_level = app.config.get("FLASK_LOGLEVEL", "INFO")
    app.logger.setLevel(getattr(logging, logging_level.upper()))

    # Log messages to a file if the config is provided.
    log_file = app.config.get("FLASK_LOGFILE")
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        app.logger.addHandler(file_handler)


def configure_extensions(app: Flask):
    """
    Initialize Flask extensions.

    Args:
        app (Flask): The Flask application instance.
    """
    from .models import MCQ

    db.init_app(app)

    with app.app_context():
        db.create_all()


def register_blueprints(app: Flask):
    """
    Register Blueprints with the Flask application.

    Args:
        app (Flask): The Flask application instance.
    """
    from .routes.entry import entry_page
    from .routes.mcq_generator import mcq_generator
    from .routes.question_answer import question_answer

    app.register_blueprint(entry_page)
    app.register_blueprint(mcq_generator)
    app.register_blueprint(question_answer)
