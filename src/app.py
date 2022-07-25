from flask import Flask
from flask_restful import Api
from flask_mongoengine import MongoEngine

from src.resources.cuts import Cuts
from src.resources.rooms import Rooms

from .config import MONGO_SETTINGS
from src.resources.floor_laying import FloorLaying
from src.resources.corners import Corners


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

    api.add_resource(Corners, "/corners")
    api.add_resource(FloorLaying, "/floor-laying")

    db = MongoEngine(app)

    api.add_resource(Rooms, "/rooms")

    api.add_resource(Cuts, "/cuts")

    return app, api, db
