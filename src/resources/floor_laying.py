import json
from flask import request, jsonify
from flask_restful import Resource
from shapely.affinity import rotate
from shapely.geometry import Point, Polygon, box
from shapely.geometry.collection import GeometryCollection
from src.resources.utils import axis_ajust, normalize, get_corner_from_index, two_points_slope, get_unique_cuts
import numpy as np
import requests

class FloorLaying(Resource):
    def get(self):
        points = request.args.get('points')

        if not points:
            return jsonify(
                error="Bad Request: Missing argument 'points'",
                status=400
            )

        points = json.loads(points)

        corner = request.args.get('corner')

        if not corner:
            return jsonify(
                error="Bad Request: Missing argument 'corner'",
                status=400
            )

        corner = int(corner)

        
        ceramic_data = request.args.get('ceramic_data')

        if not ceramic_data:
            return jsonify(
                error="Bad Request: Missing argument 'ceramic_data'",
                status=400
            )

        ceramic_data = json.loads(ceramic_data)

        if ['height', 'spacing', 'width'] != sorted(ceramic_data.keys()):
            return jsonify(
                error="Bad Request: Argument 'ceramic_data' invalid",
                status=400
            )

        fig = Polygon(points)

        if not fig.is_valid:
            return jsonify(
                error="Bad Request: Polygon invalid",
                status=400
            )

        a,b,c = get_corner_from_index(corner, points)
        slope = two_points_slope(a,b) % 90

        if slope != 0:
        	fig = rotate(fig, slope)
            # Update config after rotation
        	points = list(fig.exterior.coords)
        	a,b,c = get_corner_from_index(corner, points)

        xmin, ymin, xmax, ymax = fig.bounds
        total_width = ceramic_data["width"] + ceramic_data["spacing"]
        total_height = ceramic_data["height"] + ceramic_data["spacing"]

        # Shift xmin/ymin to match corner 
        refx, refy = points[corner]
        xmin = np.around(xmin - (total_width - (refx - xmin)  % total_width), 5)
        ymin = np.around(ymin - (total_height - (refy - ymin) % total_height), 5)

        # Prevent ending up with spacing touching the wall
        x,y = axis_ajust(a,b,c)
        fix_x = ceramic_data["spacing"] if x else 0
        fix_y = ceramic_data["spacing"] if y else 0

        result = {"cuts": [], "full": 0}
        for x1 in np.arange(xmin + fix_x, xmax + ceramic_data["width"], total_width):
            for y1 in np.arange(ymin + fix_y, ymax + ceramic_data["height"], total_height):
                x2 = x1 + ceramic_data["width"]
                y2 = y1 + ceramic_data["height"]
                ceramic = box(
                    np.around(x1, 5),
                    np.around(y1, 5),
                    np.around(x2, 5),
                    np.around(y2, 5))

                x,y = ceramic.exterior.coords.xy

                if fig.intersects(ceramic) and not ceramic.touches(fig):

                    a,b,c,d = ceramic.bounds
                    c += ceramic_data["spacing"]
                    d += ceramic_data["spacing"]

                    new_ceramic = box(a,b,c,d)

                    # if new_ceramic.intersects(Point((refx,refy))):
                    #     start = ceramic

                    x,y = ceramic.exterior.coords.xy

                    if not fig.covers(ceramic):
                        intersection = fig.intersection(ceramic)
                        if type(intersection) is not Polygon:
                            if type(intersection) is GeometryCollection:
                                for polyg in intersection.geoms:
                                    if type(polyg) is Polygon:
                                        x,y = polyg.exterior.coords.xy
                        else:
                            x,y = intersection.exterior.xy

                        result["cuts"].append(normalize(x,y))

                    else:
                        result["full"] += 1

        result["cuts"] = get_unique_cuts(result["cuts"])

        return jsonify(
            floor_laying=result,
            status=200
        )
