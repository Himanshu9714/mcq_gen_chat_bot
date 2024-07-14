import logging

from flask import Flask
from flask.logging import default_handler

from .extensions import db


def create_app():
    app = Flask(__name__)
    app.config.from_object("chat_mcq.config")

    configure_logging(app)
    configure_extensions(app)
    register_blueprints(app)

    return app


def configure_logging(app: Flask):
    # default handler.
    app.logger.addHandler(default_handler)

    # Logging level for the flask app, by default set to INFO
    logging_level = app.config.get("FLASK_LOGLEVEL", "INFO")
    app.logger.setLevel(getattr(logging, logging_level.upper()))

    # Log the messages in the file if the config is provided
    log_file = app.config.get("FLASK_LOGFILE")
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        app.logger.addHandler(file_handler)


def configure_extensions(app: Flask):
    from .models import MCQ

    db.init_app(app)

    with app.app_context():
        db.create_all()


def register_blueprints(app: Flask):
    from .routes.entry import entry_page
    from .routes.mcq_generator import mcq_generator

    app.register_blueprint(entry_page)
    app.register_blueprint(mcq_generator)
