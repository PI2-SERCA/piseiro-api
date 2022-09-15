from flask import request, jsonify
from flask_restful import Resource
from shapely.geometry import box
from src.resources.utils import (
    get_optimized_cut,
    get_scribe_lines,
    points_to_base64_image,
    simple_error_response,
)
import requests

from src.util.broker import send_cuts
from src.util.gcode import parse_gcode


class Scribe(Resource):
    def post(self):
        data = request.get_json(force=True)

        for arg in ["cuts", "repetitions", "ceramic_data"]:
            if arg not in data.keys():
                return simple_error_response(
                    f"Bad Request: Missing argument '{arg}'", requests.codes.bad_request
                )

        cuts = data["cuts"]
        repetitions = data["repetitions"]
        ceramic_data = data["ceramic_data"]

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

        ceramic = box(0, 0, ceramic_data["width"], ceramic_data["height"])

        result = []
        for cut in cuts:
            optimized_cut = get_optimized_cut(cut["points"], ceramic)
            scribe_lines = get_scribe_lines(optimized_cut, ceramic)

            gcode = parse_gcode(scribe_lines)
            new_cut = {
                "gcode": gcode,
                "repetitions": repetitions * cut["quantity"],
                "width": ceramic_data["width"],
                "height": ceramic_data["height"],
                "depth": ceramic_data["depth"],
            }

            if cut.get("base64", None) is not None:
                new_cut["base64"] = cut["base64"]
            else:
                new_cut["base64"] = points_to_base64_image(cut["points"], ceramic_data)

            result.append(new_cut)

        send_cuts(result)

        return jsonify(cuts=result, status=requests.codes.ok)
