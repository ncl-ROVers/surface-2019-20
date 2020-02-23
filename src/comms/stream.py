"""
Stream
======

Module storing an implementation of a stream-based connection to a network camera.
"""
from .utils import DEFAULT_STREAM_WIDTH as _DEFAULT_WIDTH, DEFAULT_STREAM_HEIGHT as _DEFAULT_HEIGHT, \
    STREAM_THREAD_DELAY as _DELAY
from ..common import Log as _Log
from PySide2.QtGui import QImage as _QImage, QPixmap as _QPixmap
from PySide2.QtCore import QObject as _QObject, Signal as _Signal
import typing as _typing
import cv2 as _cv2
import numpy as _np
import threading as _threading
import time as _time


class VideoStream(_QObject):
    """
    Video stream class used as a stream receiver.

    Handles fetching frames from a remote address in OpenCV format and their conversion to QT format.

    Functions
    ---------

    The following list shortly summarises each function:

        * __init__ - a constructor to create and initialise video capture and thread related constructs
        * frame - a getter used to retrieve the frame in OpenCV format
        * frame_qt - a getter used to retrieve the frame in QT format
        * shape - a property used to get or set the resolution of the frame
        * _read - helper method to read the frames in a thread (and emit signals)

    Usage
    -----

    The stream object should be created as follows::

        stream = VideoStream(URL)

    where `URL` is a valid url in string format.

    ..warning::

        The frame reading process will start immediately, and it's up to the calling code to decide when to use them.
    """
    # Create a QT signal to connect it to frame displaying slots in the GUI
    frame_received = _Signal(_QPixmap)

    def __init__(self, url: str):
        """
        Standard constructor.

        Builds a video capture object and starts receiving the frames in a separate thread.

        :param url: URL of the stream
        """
        super().__init__()

        # Set up basic parameters
        self._url = url
        self._width = _DEFAULT_WIDTH
        self._height = _DEFAULT_HEIGHT
        self._frame = _np.empty((self._height, self._width, 3))

        # Configure OpenCV video capture - set correct resolution and source url
        self._video_capture = _cv2.VideoCapture(self._url)
        self._video_capture.set(3, self._width)
        self._video_capture.set(4, self._height)

        # Start frame reading code
        self._thread = _threading.Thread(target=self._read, daemon=True)
        self._thread.start()

    @property
    def frame(self) -> _np.ndarray:
        """
        Getter for the frame (OpenCV format).
        """
        return self._frame

    @property
    def frame_qt(self) -> _QPixmap:
        """
        Getter for the frame (QT format).

        Transforms the frame into a QPixelmap.
        """
        frame = self.frame

        # Empty array will fail to get converted
        try:
            frame = _cv2.cvtColor(frame, _cv2.COLOR_BGR2RGB)
        except _cv2.error as e:
            _Log.error(f"Failed to convert a frame from BGR to RGB - {e}")

        # Extract information from the frame
        height, width, _ = frame.shape
        bytes_per_line = 3 * width

        # Create QT-related objects and return the pixel map
        image = _QImage(frame.data, width, height, bytes_per_line, _QImage.Format_RGB888)
        pixel_map = _QPixmap.fromImage(image)
        return pixel_map

    @property
    def shape(self) -> _typing.Tuple[int, int]:
        """
        Getter for the frame's resolution.
        """
        return self._width, self._height

    @shape.setter
    def shape(self, shape: _typing.Tuple[int, int]):
        """
        Setter for the frame's resolution.

        :param shape: Width and height
        """
        self._width = shape[0]
        self._height = shape[1]
        self._video_capture.set(3, self._width)
        self._video_capture.set(4, self._height)

    def _read(self):
        """
        Helper method used to read the frames in a background thread.

        Emits a signal with the QPixmap frame on each frame read.
        """
        while True:
            ret, frame = self._video_capture.read()
            self._frame = frame if ret else _np.empty((self._height, self._width, 3))
            if ret:
                self.frame_received.emit(self.frame_qt)
            _time.sleep(_DELAY)
