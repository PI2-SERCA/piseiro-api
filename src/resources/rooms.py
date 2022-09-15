from flask_restful import Resource
from src.model.room import Room
from flask import request
from src.resources.utils import simple_error_response
import mongoengine as me
import requests


class Rooms(Resource):
    def get(self, room_id=None):
        if room_id is None:
            return [room.to_json() for room in Room.objects]

        return self.show(room_id)

    def get_room(self, room_id):
        try:
            room = Room.objects.with_id(room_id)

            if room is None:
                return None, f"There is no room with ID {room_id}"

            return room, None
        except me.errors.ValidationError:
            return None, f"There is no room with ID {room_id}"

    def show(self, room_id):
        room, json_msg = self.get_room(room_id)

        if room is None:
            return simple_error_response(json_msg, requests.codes.not_found)

        return room.to_json(), requests.codes.ok

    def delete(self, room_id):
        room, json_msg = self.get_room(room_id)

        if room is None:
            return simple_error_response(json_msg, requests.codes.not_found)

        room.delete()

        return requests.codes.ok

    def post(self):
        data = request.get_json(force=True)

        room = Room(
            points=data.get("points"),
            defaults=data.get("defaults"),
            segments=data.get("segments"),
            name=data.get("name"),
        )

        room.save()

        return room.to_json()

    def patch(self, room_id):
        room, error_msg = self.get_room(room_id)

        if room is None:
            return simple_error_response(error_msg, requests.codes.not_found)

        data = request.get_json(force=True)

        try:
            room.update(**data)
            room.reload()

            return room.to_json(), requests.codes.ok
        except me.errors.ValidationError as error:
            return simple_error_response(
                str(error), requests.codes.unprocessable_entity
            )
