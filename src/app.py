from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_mongoengine import MongoEngine

from src.resources.cuts import Cuts
from src.resources.rooms import Rooms
from src.util.broker import declare_queue

from .config import MONGO_SETTINGS
from src.resources.floor_laying import FloorLaying
from src.resources.corners import Corners
from src.resources.scribe import Scribe
from src.resources.single_cut import SingleCut


def create_app(is_testing=False):
    """
    Create the Flask app
    """
    app = Flask(__name__)

    app.config["CORS_ORIGINS"] = [
        "http://localhost:3000",
        "https://pisadinha.netlify.app",
        "http://pisadinha.s3-website.us-east-2.amazonaws.com",
    ]

    CORS(app)

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

    declare_queue()

    api.add_resource(Corners, "/corners")
    api.add_resource(FloorLaying, "/floor-laying")
    api.add_resource(Scribe, "/scribe")
    api.add_resource(SingleCut, "/single-cut")
    api.add_resource(Rooms, "/rooms", "/rooms/<string:room_id>")
    api.add_resource(Cuts, "/cuts", "/cuts/<string:cut_id>")

    return app, api, db
