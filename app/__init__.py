import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(db_uri):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    # sqlalchemy event system is not used, so it is safely turned off
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.logger.setLevel(logging.INFO)
    db.init_app(app)
    app.app_context().push()
    with app.app_context():
        from app.routes import routes
        from app.models import user
    return app
