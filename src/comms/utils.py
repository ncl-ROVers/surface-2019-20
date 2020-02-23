"""
Communication Utils
===================

Standard utils module storing common to the package classes, functions, constants, and other objects.
"""
import enum as _enum

# Declare STREAM-related constructs - resolution and read delay
DEFAULT_STREAM_WIDTH = 640
DEFAULT_STREAM_HEIGHT = 480
STREAM_THREAD_DELAY = 0.03

# TODO: Replace with real urls
MAIN_STREAM_URL = "http://localhost:11026/"
TOP_STREAM_URL = "http://localhost:11025/"
BOTTOM_STREAM_URL = "http://localhost:11024/"
MICRO_STREAM_URL = "http://217.45.174.115:81/mjpg/video.mjpg"


class ConnectionStatus(_enum.Enum):
    """
    Enumeration for different connection statuses.

    The order of communicating with a remote server should always be:

        1. Connecting
        2. Connected
        3. Disconnected
    """
    CONNECTING = 0
    CONNECTED = 1
    DISCONNECTED = 2
