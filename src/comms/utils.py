"""
Communication Utils
===================

Standard utils module storing common to the package classes, functions, constants, and other objects.
"""
import enum as _enum


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
