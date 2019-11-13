import enum as _enum


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

    return intended_min + (value - current_min) * (intended_max - intended_min) / (current_max - current_min)


class DrivingMode(_enum.Enum):
    """
    TODO: Document
    """
    MANUAL = 0
    BALANCING = 1
    AUTONOMOUS = 2