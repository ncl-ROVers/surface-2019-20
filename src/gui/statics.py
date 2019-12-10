"""
GUI Statics
===========

Standard statics module storing all constants, classes and other objects which do not change throughout the execution
of the program.
"""

import enum

SCREEN_HEIGHT = 1080
SCREEN_WIDTH = 1920
WINDOW_INDICATOR = 'borders'


class Colour(enum.Enum):
    """
    Colour enumeration storing different colour values for the GUI style.

    Each colour is in the RGBA format.
    """

    MAJOR = 34, 51, 54, 255
