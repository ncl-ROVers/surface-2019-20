import enum as _enum


class DrivingMode(_enum.Enum):
    """
    Enumeration for allowed driving modes.
    """
    MANUAL = 0
    BALANCING = 1
    AUTONOMOUS = 2