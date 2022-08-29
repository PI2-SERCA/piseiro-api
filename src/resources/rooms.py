from flask_restful import Resource
from src.model.room import Room


class Rooms(Resource):
    def get(self):
        return [room.to_json() for room in Room.objects]
