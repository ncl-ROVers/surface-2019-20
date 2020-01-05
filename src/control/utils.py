"""
Control Utils
=============

Standard utils module storing common to the package classes, functions, constants, and other objects.
"""
import enum as _enum

# Declare the expected normalised values
NORM_MAX = 1
NORM_IDLE = 0
NORM_MIN = -NORM_MAX


class DrivingMode(_enum.Enum):
    """
    Enumeration for allowed driving modes.
    """
    MANUAL = 0
    BALANCING = 1
    AUTONOMOUS = 2


def normalise(value: float, current_min: float, current_max: float, intended_min: float, intended_max: float) -> float:
    """
    Function used to normalise a value to fit within a given range, knowing its actual range.

    Uses standard MinMax normalisation.

    :param value: Value to be normalised
    :param current_min: The actual minimum of the value
    :param current_max: The actual maximum of the value
    :param intended_min: The expected minimum of the value
    :param intended_max: The expected maximum of the value
    :raises: ValueError
    :return: Normalised value
    """
    if current_min == current_max or intended_min == intended_max:
        raise ValueError("Current or intended minimum and maximum can not be equal")
    elif not (current_max >= value >= current_min):
        raise ValueError(f"Value {value} is not be between {current_min} and {current_max}")

    return intended_min + (value - current_min) * (intended_max - intended_min) / (current_max - current_min)
