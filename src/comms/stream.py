"""
TODO: Document
"""
from .utils import STREAM_CLOCK_INTERVAL as _INTERVAL, STREAM_WIDTH as _WIDTH, STREAM_HEIGHT as _HEIGHT
from ..common import Log as _Log
import cv2 as _cv2
from PySide2.QtCore import QTimer as _QTimer
import numpy as _np


class VideoStream:
    """
    TODO: Document
    """

    def __init__(self, url: str):
        """
        TODO: Document

        :param url:
        """
        self._url = url

        # Frames will have constant shape - therefore initialising it to an empty array of preset shape is fine
        self._frame = _np.empty((_HEIGHT, _WIDTH, 3))

        # Sometimes the interval might have to be adjusted to offload resources
        self._interval = _INTERVAL

        # Declare clock-related values to update the frames with a constant rate
        self._clock = _QTimer()
        self._clock.setInterval(self._interval)
        self._clock.timeout.connect(self._read)

        # Configure OpenCV video capture - set correct resolution and source url
        self._video_capture = _cv2.VideoCapture(self._url)
        self._video_capture.set(3, _WIDTH)
        self._video_capture.set(4, _HEIGHT)

    @property
    def frame(self) -> _np.ndarray:
        """
        TODO: Document
        """
        if not self._clock.isActive():
            _Log.warning(f"Clock isn't active for {self._url} stream, frames will not be updated")

        return self._frame

    @property
    def clock(self) -> _QTimer:
        """
        TODO: Document
        """
        return self._clock

    def set_interval(self, interval: int):
        """
        TODO: Document

        :param interval:
        """
        self._interval = interval
        self._clock.setInterval(interval)

    def _read(self):
        """
        TODO: Document
        """
        data = self._video_capture.read()
        self._frame = data[1] if data[0] else _np.empty((_HEIGHT, _WIDTH, 3))
