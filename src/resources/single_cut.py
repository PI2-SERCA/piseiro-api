from flask import request, jsonify
from flask_restful import Resource
from shapely.geometry import box, Polygon
from src.resources.utils import get_scribe_lines
import requests


class SingleCut(Resource):
    def post(self):
        data = request.get_json(force=True)

        for arg in ['points', 'repetitions', 'ceramic_data']:
            if arg not in data.keys():
                return jsonify(
                    error=f"Bad Request: Missing argument '{arg}'",
                    status=requests.codes.bad_request
                )

        points = data['points']
        repetitions = data['repetitions']
        ceramic_data = data['ceramic_data']

        must = {'height', 'width'}
        if must.intersection(set(ceramic_data.keys())) != must:
            return jsonify(
                error="Bad Request: Argument 'ceramic_data' invalid",
                status=requests.codes.bad_request
            )

        if type(repetitions) is not int:
            return jsonify(
                error="Bad Request: Argument 'repetitions' is not integer",
                status=requests.codes.bad_request
            )

        fig = Polygon(points)
        if not fig.is_valid:
            return jsonify(
                error="Bad Request: Polygon invalid",
                status=requests.codes.bad_request
            )

        ceramic = box(0, 0, ceramic_data['width'], ceramic_data['height'])

        cut = Polygon(points)
        scribe_lines = get_scribe_lines(cut, ceramic)

        result = {"points": scribe_lines}

        return jsonify(
            single_cut=result,
            status=requests.codes.ok
        )
