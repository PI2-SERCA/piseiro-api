from src.model.cast import Cast


class Cut(Cast):
    def to_json(self):
        return {
            "name": self.name,
            "points": self.points,
            "defaults": self.defaults,
            "segments": self.segments,
        }
