from flask import request, jsonify
from flask_restful import Resource
from shapely.geometry import box, Polygon
from src.resources.utils import (
    get_scribe_lines,
    points_to_base64_image,
    simple_error_response,
)
import requests

from src.util.broker import send_cuts
from src.util.gcode import parse_gcode


class SingleCut(Resource):
    def post(self):
        data = request.get_json(force=True)

        for arg in ["points", "repetitions", "ceramic_data"]:
            if arg not in data.keys():
                return simple_error_response(
                    f"Bad Request: Missing argument '{arg}'", requests.codes.bad_request
                )

        points = data["points"]
        repetitions = data["repetitions"]
        ceramic_data = data["ceramic_data"]
        img_base64 = data.get("base64", None)

        must = {"height", "width", "depth"}
        if must.intersection(set(ceramic_data.keys())) != must:
            return simple_error_response(
                "Bad Request: Argument 'ceramic_data' invalid",
                requests.codes.bad_request,
            )

        if type(repetitions) is not int:
            return simple_error_response(
                "Bad Request: Argument 'repetitions' is not integer",
                requests.codes.bad_request,
            )

        fig = Polygon(points)
        if not fig.is_valid:
            return simple_error_response(
                "Bad Request: Polygon invalid",
                requests.codes.bad_request,
            )

        ceramic = box(0, 0, ceramic_data["width"], ceramic_data["height"])

        cut = Polygon(points)
        scribe_lines = get_scribe_lines(cut, ceramic)

        gcode = parse_gcode(scribe_lines, ceramic_data["depth"])

        result = {
            "gcode": gcode,
            "repetitions": repetitions,
            "width": ceramic_data["width"],
            "height": ceramic_data["height"],
            "depth": ceramic_data["depth"],
        }

        if img_base64 is not None:
            result["base64"] = img_base64
        else:
            result["base64"] = points_to_base64_image(points, ceramic_data)

        # Sending to broker
        send_cuts([result])

        return jsonify(single_cut=result, status=requests.codes.ok)
