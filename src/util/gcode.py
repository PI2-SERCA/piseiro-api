from pygcode import (GCode, GCodeRapidMove, GCodeLinearMove, GCodeFeedRate, GCodeAbsoluteDistanceMode,
                     GCodeUseMillimeters, Word)
from constants import START_POSITION, FEED_RATE, Z_AXIS_CUT_POSITION


def parse_gcode(scribe_lines):
    """
    Parse the cut coordinates and return a list of GCode objects.
    """
    g_codes = []

    for coordinates in scribe_lines:
        x_move, y_move = _coordinates_to_millimeters(coordinates[0])

        g_codes.append(GCodeRapidMove(X=x_move, Y=y_move))
        g_codes.append(GCodeFeedRate(FEED_RATE))
        g_codes.append(GCodeLinearMove(Z=Z_AXIS_CUT_POSITION))

        for cut_coordinate in coordinates[1:]:
            x_cut, y_cut = _coordinates_to_millimeters(cut_coordinate)
            g_codes.append(GCodeLinearMove(X=x_cut, Y=y_cut))

        g_codes.append(GCodeRapidMove(Z=START_POSITION.get('Z')))

    g_codes.append(GCode(Word('G', '28.1')))

    return _g_codes_to_string(g_codes)


def setup_machine():
    """
    Setup the machine to start at the given position.
    """
    g_codes = [
        GCode(Word('G', '28.1')),  # Return to home position
        GCodeAbsoluteDistanceMode(),
        GCodeUseMillimeters()
    ]

    return g_codes


def _coordinates_to_millimeters(coordinates):
    return list(map(_meters_to_millimeters, coordinates))


def _meters_to_millimeters(meters):
    return meters * 1000


def _g_codes_to_string(gcode):
    return '\n'.join(str(g) for g in gcode)
