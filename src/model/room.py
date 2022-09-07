from src.model.cast import Cast

ROOM_PROPORTION = 10


class Room(Cast):
    def get_default_points(self):
        return super().get_default_points(ROOM_PROPORTION)
