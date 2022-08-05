import json
from flask import request, jsonify
from flask_restful import Resource
from shapely.affinity import rotate
from shapely.geometry import Point, Polygon, box
from shapely.geometry.collection import GeometryCollection
from src.resources.utils import axis_ajust, get_corner_from_index, two_points_slope, get_unique_cuts, points_to_base64_image
import numpy as np
import requests

class FloorLaying(Resource):
    def get(self):

        for arg in ['points', 'corner', 'ceramic_data']:
            if arg not in request.args.keys():
                return jsonify(
                    error=f"Bad Request: Missing argument '{arg}'",
                    status=requests.codes.bad_request
                )

        points = request.args.get('points')
        corner = request.args.get('corner')
        ceramic_data = request.args.get('ceramic_data')

        try:
            corner = int(corner)
        except:
            return jsonify(
                error="Bad Request: Wrong format in 'corner'",
                status=requests.codes.bad_request
            )

        try:
            ceramic_data = json.loads(ceramic_data)
        except:
            return jsonify(
                error="Bad Request: Wronge JSON format in 'ceramic_data'",
                status=requests.codes.bad_request
            )

        must = {'height', 'spacing', 'width'}
        if must.intersection(set(ceramic_data.keys())) != must:
            return jsonify(
                error="Bad Request: Argument 'ceramic_data' invalid",
                status=requests.codes.bad_request
            )

        try:
            points = json.loads(points)
        except:
            return jsonify(
                error="Bad Request: Wrong JSON format in 'points'",
                status=requests.codes.bad_request
            )

        fig = Polygon(points)
        if not fig.is_valid:
            return jsonify(
                error="Bad Request: Polygon invalid",
                status=requests.codes.bad_request
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

                    coords = ceramic.exterior.coords

                    if not fig.covers(ceramic):
                        intersection = fig.intersection(ceramic)
                        if type(intersection) is not Polygon:
                            if type(intersection) is GeometryCollection:
                                for polyg in intersection.geoms:
                                    if type(polyg) is Polygon:
                                        coords = polyg.exterior.coords
                        else:
                            coords = intersection.exterior.coords

                        result["cuts"].append(list(coords))

                    else:
                        result["full"] += 1

        result["cuts"] = get_unique_cuts(result["cuts"])

        for cut in result["cuts"]:
            base64 = points_to_base64_image(cut["points"])
            cut["base64"] = base64

        return jsonify(
            floor_laying=result,
            status=requests.codes.ok
        )
