from pygcode import (GCode, GCodeRapidMove, GCodeLinearMove, GCodeFeedRate, GCodeAbsoluteDistanceMode,
                     GCodeUseMillimeters, Word)
from constants import START_POSITION, FEED_RATE, Z_AXIS_CUT_POSITION

# Scribe lines are in the format:
# [[[Xstart0, Ystart0], [Xdest0, Ydest0]], [[Xstart1, Ystart1], [Xdest1, Ydest1]]...]


def parse_gcode(scribe_lines):
    """
    Parse the cut coordinates and return a list of GCode objects.
    """
    g_codes = []

    for line in scribe_lines:
        start_coordinates = list(map(_meters_to_millimeters, line[0]))
        dest_coordinates = list(map(_meters_to_millimeters, line[1]))

        g_codes.append(GCodeRapidMove(X=start_coordinates[0], Y=start_coordinates[1]))
        g_codes.append(GCodeFeedRate(FEED_RATE))
        g_codes.append(GCodeLinearMove(Z=Z_AXIS_CUT_POSITION))
        g_codes.append(GCodeLinearMove(X=dest_coordinates[0], Y=dest_coordinates[1]))
        g_codes.append(GCodeRapidMove(Z=START_POSITION.get('Z')))

    g_codes.append(GCode(Word('G', '28.1')))
    return g_codes


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


def _meters_to_millimeters(meters):
    return meters * 1000
