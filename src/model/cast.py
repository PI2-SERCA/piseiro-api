import mongoengine as me


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

    def to_json(self):
        return {
            "name": self.name,
            "points": self.points,
            "defaults": self.defaults,
            "segments": self.segments,
        }
