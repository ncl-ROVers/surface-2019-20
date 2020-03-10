"""
Stream
======

Module storing an implementation of a stream-based connection to a network camera.
"""
from PySide2.QtGui import QImage as _QImage, QPixmap as _QPixmap
from PySide2.QtCore import QObject as _QObject, Signal as _Signal, QByteArray as _QByteArray
import numpy as _np
from . import streams as _streams


class VideoStream(_QObject):
    """
    Video stream class used to capture a video stream.

    Handles fetching frames from a remote address and their conversion to raw pixel format.

    Usage
    -----

    A stream object can be created as follows:

        capture = VideoStream(URL)

    where `URL` is a valid URL in string format.

    The latest frame can be received using the `frame` property which will
    return a numpy array containing all the pixel values.
    """
    # Create a QT signal to connect it to frame displaying slots in the GUI
    frame_received = _Signal(_QPixmap)

    def __init__(self, stream_url: str):
        """
        Standard constructor.

        Parses the video stream URL and initializes stream variables.

        :param stream_url: The url of the video stream to be captured.
        """
        super().__init__()

        self.__reader = _streams.stream_from_url(stream_url)
        self.__reader.frame_callback = lambda: self.frame_received.emit(self.frame_qt)
        self.__reader.open_stream()

    @property
    def frame_raw(self) -> bytearray:
        """
        Get the last frame received by the stream.

        :return: A bytearray that contains the raw JPEG image data.
        """
        return self.__reader.frame_raw

    @property
    def frame(self) -> _np.ndarray:
        """
        Get the last frame received by the stream.

        :return: An array of the pixels of the frame.
        """
        return self.__reader.frame

    @property
    def frame_qt(self) -> _QPixmap:
        """
        Getter for the frame (QT format).

        Transforms the frame into a QPixelmap.
        """
        if self.__reader.raw_type == "jpeg":
            image = _QImage()
            image.loadFromData(_QByteArray(self.frame_raw), aformat="jpeg")
            pixel_map = _QPixmap.fromImage(image)
            return pixel_map

        return _QPixmap()

    def close(self):
        """
        Close the stream.
        """
        self.__reader.close()
