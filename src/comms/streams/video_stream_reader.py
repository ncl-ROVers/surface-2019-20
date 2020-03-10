"""
Video Stream Reader
==================

Module storing an abstract class that all video stream implementations are based on
"""

from abc import ABC as _ABC, abstractmethod
from ..utils import ConnectionStatus as _ConnectionStatus


class VideoStreamReader(_ABC):
    """
    Base class for all video stream readers.

    Used to create a common interface for all video stream reader implementations.
    """

    @abstractmethod
    def __init__(self, host_properties):
        """
        Standard constructor.

        Initializes stream variables.

        :param host_properties: The components of the url to connect to (as returned by the 'parse_url' method)
        """
        super(VideoStreamReader, self).__init__()

        self.__frame_callback = None
        self.host = host_properties

    @abstractmethod
    def open_stream(self):
        pass

    @property
    @abstractmethod
    def frame_raw(self):
        pass

    @property
    @abstractmethod
    def frame(self):
        pass

    @property
    @abstractmethod
    def raw_type(self) -> str:
        pass

    @property
    def frame_callback(self):
        return self.__frame_callback

    @frame_callback.setter
    def frame_callback(self, frame_received_callback: lambda: ()):
        self.__frame_callback = frame_received_callback

    def invoke_frame_callback(self):
        if self.__frame_callback is not None:
            self.__frame_callback()

    @property
    @abstractmethod
    def status(self) -> _ConnectionStatus:
        return _ConnectionStatus.DISCONNECTED

    @abstractmethod
    def close(self):
        pass
