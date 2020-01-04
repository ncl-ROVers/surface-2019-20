"""
TODO: Document
"""
import socket as _socket
from json import loads as _loads, dumps as _dumps, JSONDecodeError as _JSONDecodeError
from ..common import data_manager as _dm
from ..common import Log as _Log
from time import sleep as _sleep


class Connection:
    """
    TODO: Document
    """

    def __init__(self, ip: str = "localhost", *, port: int = 50000):
        """
        TODO: Document
        :param ip:
        :param port:
        """
        pass

    @property
    def status(self):
        """
        TODO: Document
        :return:
        """
        pass

    def connect(self):
        """
        TODO: Document
        :return:
        """
        pass

    def disconnect(self):
        """
        TODO: Document
        :return:
        """
        pass

    def reconnect(self):
        """
        TODO: Document
        :return:
        """
        pass
