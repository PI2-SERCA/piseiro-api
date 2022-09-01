from src.model.cast import Cast

CUT_PROPORTION = 100


class Cut(Cast):
    def get_default_points(self):
        return super().get_default_points(CUT_PROPORTION)
