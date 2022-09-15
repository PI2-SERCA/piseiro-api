from flask_restful import Resource
from src.model.cut import Cut
from flask import request
from src.resources.utils import simple_error_response
import mongoengine as me
import requests


class Cuts(Resource):
    def get(self, cut_id=None):
        if cut_id is None:
            return [cut.to_json() for cut in Cut.objects]

        return self.show(cut_id)

    def get_cut(self, cut_id):
        try:
            cut = Cut.objects.with_id(cut_id)

            if cut is None:
                return None, f"There is no cut with ID {cut_id}"

            return cut, None
        except me.errors.ValidationError:
            return None, f"There is no cut with ID {cut_id}"

    def show(self, cut_id):
        cut, json_msg = self.get_cut(cut_id)

        if cut is None:
            return simple_error_response(json_msg, requests.codes.not_found)

        return cut.to_json(), requests.codes.ok

    def delete(self, cut_id):
        cut, json_msg = self.get_cut(cut_id)

        if cut is None:
            return simple_error_response(json_msg, requests.codes.not_found)

        cut.delete()

        return requests.codes.ok

    def post(self):
        data = request.get_json(force=True)

        cut = Cut(
            points=data.get("points"),
            defaults=data.get("defaults"),
            segments=data.get("segments"),
            name=data.get("name"),
        )

        cut.save()

        return cut.to_json()

    def patch(self, cut_id):
        cut, error_msg = self.get_cut(cut_id)

        if cut is None:
            return simple_error_response(error_msg, requests.codes.not_found)

        data = request.get_json(force=True)

        try:
            cut.update(**data)
            cut.reload()

            return cut.to_json(), requests.codes.ok
        except me.errors.ValidationError as error:
            return simple_error_response(
                str(error), requests.codes.unprocessable_entity
            )
