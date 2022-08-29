from flask import Flask
from flask_restful import Api
from flask_mongoengine import MongoEngine

from src.resources.cuts import Cuts
from src.resources.rooms import Rooms

from .config import MONGO_SETTINGS


def create_app(is_testing=False):
    """
    Create the Flask app
    """
    app = Flask(__name__)

    if is_testing:
        app.config["TESTING"] = True
        app.config["MONGODB_SETTINGS"] = {
            "host": "mongomock://localhost",
            "db": "piseiro",
        }
    else:
        app.config["MONGODB_SETTINGS"] = MONGO_SETTINGS

    api = Api(app)

    db = MongoEngine(app)

    api.add_resource(Rooms, "/rooms")

    api.add_resource(Cuts, "/cuts")

    return app, api, db
