import mongoengine as me
from src.resources.utils import points_to_base64_image

MAX_CERAMIC_SIZE = 50


class Cast(me.Document):
    meta = {"allow_inheritance": True}
    name = me.StringField(required=True)
    points = me.ListField(me.StringField())
    defaults = me.MapField(me.FloatField())
    segments = me.MapField(me.ListField(me.StringField(), 2))

    def __init__(self, name, points, defaults, segments, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.points = points
        self.defaults = defaults
        self.segments = segments

    def get_default_points(self, proportion=1):
        points = []

        for point in self.points:
            a, b = point.split(";")

            value_a = self.defaults.get(a, None) or float(a)
            value_b = self.defaults.get(b, None) or float(b)

            points.append((value_a * proportion, value_b * proportion))

        return points

    def to_json(self):
        return {
            "_id": str(self.pk),
            "name": self.name,
            "points": self.points,
            "defaults": self.defaults,
            "segments": self.segments,
            "base64": points_to_base64_image(
                self.get_default_points(),
                {"width": MAX_CERAMIC_SIZE, "height": MAX_CERAMIC_SIZE},
            ),
        }
