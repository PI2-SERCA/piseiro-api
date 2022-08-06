from flask import request, jsonify
from flask_restful import Resource
from shapely.geometry import Polygon
import io
import json
import matplotlib.pyplot as plt
import requests
from src.resources.utils import binary_to_base64


class SingleCut(Resource):
    def get(self):

        for arg in ['points', 'ceramic_data']:
            if arg not in request.args.keys():
                return jsonify(
                    error=f"Bad Request: Missing argument '{arg}'",
                    status=requests.codes.bad_request
                )

        points = request.args.get('points')
        ceramic_data = request.args.get('ceramic_data')

        try:
            ceramic_data = json.loads(ceramic_data)
        except:
            return jsonify(
                error="Bad Request: Wronge JSON format in 'ceramic_data'",
                status=requests.codes.bad_request
            )

        must = {'height', 'width'}
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

        image_bytes = io.BytesIO()
        figure = plt.figure()

        x, y = fig.exterior.coords.xy
        plt.fill(x, y, "white")
        plt.xlim([0, ceramic_data["width"]])
        plt.ylim([0, ceramic_data["height"]])
        plt.axis("off")

        figure.savefig(
            image_bytes, format="png", dpi=figure.dpi, facecolor="tab:blue", edgecolor="none"
        )
        image_bytes.seek(0)

        result = {}
        result["base64"] = binary_to_base64(image_bytes.read())
        result["points"] = points

        return jsonify(
            single_cut=result,
            status=requests.codes.ok
        )
