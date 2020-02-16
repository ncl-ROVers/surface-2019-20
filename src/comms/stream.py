"""
TODO: Document, log things
"""
from .utils import DEFAULT_STREAM_WIDTH as _DEFAULT_WIDTH, DEFAULT_STREAM_HEIGHT as _DEFAULT_HEIGHT
from ..common import Log as _Log
from PySide2.QtGui import QImage as _QImage, QPixmap as _QPixmap
import typing as _typing
import cv2 as _cv2
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
        self._width = _DEFAULT_WIDTH
        self._height = _DEFAULT_HEIGHT

        # Configure OpenCV video capture - set correct resolution and source url
        self._video_capture = _cv2.VideoCapture(self._url)
        self._video_capture.set(3, self._width)
        self._video_capture.set(4, self._height)

    @property
    def frame(self) -> _np.ndarray:
        """
        TODO: Document
        """
        ret, frame = self._video_capture.read()
        return frame if ret else _np.empty((self._height, self._width, 3))

    @property
    def shape(self) -> _typing.Tuple[int, int]:
        """
        TODO: Docs
        :return:
        """
        return self._width, self._height

    @shape.setter
    def shape(self, shape: _typing.Tuple[int, int]):
        """
        TODO: Docs
        :param shape:
        :return:
        """
        self._width = shape[0]
        self._height = shape[1]

    @property
    def frame_qt(self) -> _QPixmap:
        """
        TODO: Docs
        :return:
        """
        frame = self.frame
        height, width, _ = frame.shape
        bytes_per_line = 3 * width
        frame = _cv2.cvtColor(frame, _cv2.COLOR_BGR2RGB)
        frame = _QImage(frame.data, width, height, bytes_per_line, _QImage.Format_RGB888)
        frame = _QPixmap.fromImage(frame)
        # TODO: FInished here broken code
        from PySide2.QtWidgets import QLabel
        x = QLabel()
        x.setPixmap(frame)
        x.show()
        return frame
