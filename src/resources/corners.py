from shapely.geometry import Polygon
from flask import request, jsonify
from flask_restful import Resource
from src.resources.utils import (
    get_corner_from_index,
    three_points_angle,
    is_valid_corner,
    simple_error_response,
)
import json
import requests


class Corners(Resource):
    def get(self):
        points = request.args.get("points")

        if not points:
            return simple_error_response(
                "Bad Request: Missing argument 'points'", requests.codes.bad_request
            )

        try:
            points = json.loads(points)
        except Exception:
            return simple_error_response(
                "Bad Request: Wrong JSON format in 'points'", requests.codes.bad_request
            )

        if not Polygon(points).is_valid:
            return simple_error_response(
                "Bad Request: Polygon invalid", requests.codes.bad_request
            )

        corners = []
        for i in range(0, len(points) - 1):
            a, b, c = get_corner_from_index(i, points)

            angle = three_points_angle(a, b, c)

            if abs(angle) == 90:
                if is_valid_corner(points, a, b, c):
                    corners.append(i)

        return jsonify(corners=corners, status=requests.codes.ok)
