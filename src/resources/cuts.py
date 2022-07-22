from flask_restful import Resource
from src.model.cut import Cut


class Cuts(Resource):
    def get(self):
        return [cut.to_json() for cut in Cut.objects]
