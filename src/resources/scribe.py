from flask import request, jsonify
from flask_restful import Resource
from shapely.geometry import box, Polygon
from src.resources.utils import get_optimized_cut, get_scribe_lines
import json
import requests


class Scribe(Resource):
    def post(self):
        data = request.get_json(force=True)

        for arg in ['cuts', 'repetitions', 'ceramic_data']:
        	if arg not in data.keys():
        		return jsonify(
        			error=f"Bad Request: Missing argument '{arg}'",
        			status=requests.codes.bad_request
        		)
        cuts = data['cuts']
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

        ceramic = box(0, 0, ceramic_data['width'], ceramic_data['height']) 

        result = []
        for cut in cuts:
            optimized_cut = get_optimized_cut(cut["points"], ceramic) 
            scribe_lines = get_scribe_lines(optimized_cut, ceramic)

            #gcode = get_gcode(scribe_lines)
            cut["points"] = list(scribe_lines)
            result.append(cut)


        return jsonify(
            cuts=result,
            status=requests.codes.ok
        )
