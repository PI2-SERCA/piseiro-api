from shapely.geometry import Polygon
from flask import request, jsonify
from flask_restful import Resource
from src.resources.utils import get_corner_from_index, three_points_angle, is_valid_corner
import json


class Corners(Resource):
    def get(self):
        points = request.args.get('points')

        if not points:
            return jsonify(
                error="Bad Request: Missing argument 'points'",
                status=400
            )
        
        points = json.loads(points)

        if not Polygon(points).is_valid:
            return jsonify(
                error="Bad Request: Polygon invalid",
                status=400
            )

        corners = []
        for i in range(0, len(points) - 1):
            a,b,c = get_corner_from_index(i, points)

            angle = three_points_angle(a,b,c)

            if abs(angle) == 90:
                if is_valid_corner(points,a,b,c):
                    corners.append(i)
        
        return jsonify(
            corners=corners,
            status=200
        )
