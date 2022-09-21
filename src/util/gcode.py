from pygcode import (
    GCodeRapidMove,
    GCodeLinearMove,
    GCodeFeedRate,
    GCodeAbsoluteDistanceMode,
    GCodeUseMillimeters,
)
from src.util.constants import START_POSITION
from src.config import (
    X_Y_FEED_RATE,
    Z_FEED_RATE,
    Z_BASE_DISTANCE,
    TO_CUT_OFFSET,
    X_OFFSET,
    Y_OFFSET,
)


def parse_gcode(scribe_lines, ceramic_depth):
    """
    Parse the cut coordinates and return a list of GCode objects.
    """
    g_codes = setup_machine()

    z_offset = _calc_z_offset(ceramic_depth)

    g_codes.append(GCodeRapidMove(Z=START_POSITION["Z"]))

    g_codes.append(GCodeRapidMove(x=START_POSITION["X"], y=START_POSITION["Y"]))

    for coordinates in scribe_lines:
        x_move, y_move = _coordinates_to_millimeters(coordinates[0])

        g_codes.append(GCodeRapidMove(X=x_move + X_OFFSET, Y=y_move + Y_OFFSET))

        g_codes.append(GCodeFeedRate(Z_FEED_RATE))

        g_codes.append(GCodeLinearMove(Z=z_offset))

        g_codes.append(GCodeFeedRate(X_Y_FEED_RATE))

        for cut_coordinate in coordinates[1:]:
            x_cut, y_cut = _coordinates_to_millimeters(cut_coordinate)
            g_codes.append(GCodeLinearMove(X=x_cut, Y=y_cut))

        g_codes.append(GCodeRapidMove(Z=START_POSITION["Z"]))

    g_codes.append(GCodeRapidMove(x=START_POSITION["X"], y=START_POSITION["Y"]))

    return _g_codes_to_string(g_codes)


def setup_machine():
    """
    Setup the machine to start at the given position.
    """
    g_codes = [
        GCodeAbsoluteDistanceMode(),
        GCodeUseMillimeters(),
    ]

    return g_codes


def _coordinates_to_millimeters(coordinates):
    return list(map(_meters_to_millimeters, coordinates))


def _meters_to_millimeters(meters):
    return meters * 1_000


def _calc_z_offset(ceramic_depth):
    return Z_BASE_DISTANCE + _meters_to_millimeters(ceramic_depth) - TO_CUT_OFFSET


def _g_codes_to_string(gcode):
    return "\n".join(str(g) for g in gcode)
