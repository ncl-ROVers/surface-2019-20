"""
Control Statics
===============

Standard statics module storing all constants, classes and other objects which do not change throughout the execution
of the program.
"""
import enum as _enum


class DrivingMode(_enum.Enum):
    """
    Enumeration for allowed driving modes.
    """
    MANUAL = 0
    BALANCING = 1
    AUTONOMOUS = 2
