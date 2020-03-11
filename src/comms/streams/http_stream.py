"""
HTTP Stream
==========

Module storing an http-based implementation of a video stream reader to a network camera.
"""

import socket as _socket
from src.comms.utils import STREAM_THREAD_DELAY as _DELAY
from .buffered_socket import BufferedSocket as _BufferedSocket
from .video_stream_reader import VideoStreamReader as _VideoStreamReader
from ..utils import ConnectionStatus as _ConnectionStatus
from src.common import Log as _Log
import threading as _threading
import simplejpeg as _simplejpeg
import numpy as _np
import time as _time


class HTTPStreamReader(_VideoStreamReader):
    """
    HTTP video stream reader.

    Currently, only MJPEG streams are supported.
    """

    def __init__(self, host_properties):
        """
        Standard constructor.

        Parses the video stream URL and initializes stream variables.

        :param host_properties: The components of the url to connect to (as returned by the 'parse_url' method)
        """
        super().__init__(host_properties)

        self.__stream_buffer = bytearray()
        self.__running = False
        self.__socket = None

        # Image buffer
        self.__image_buffer = None
        self.__image_lock = _threading.Lock()

        self.__thread = None

        self.__status = _ConnectionStatus.DISCONNECTED

    def open_stream(self):
        """
        Connect to the host and start the stream thread.
        """
        _Log.info(f"Connecting to {self.host['host_address']}:{self.host['host_port']}.")

        # Connect socket to server
        self.__socket = _BufferedSocket(_socket.AF_INET, _socket.SOCK_STREAM)
        self.__socket.connect((self.host["host_address"], self.host["host_port"]))

        # Initialize status variables
        self.__running = True
        self.__status = _ConnectionStatus.CONNECTING

        # Start streaming thread
        self.__thread = _threading.Thread(target=self.__process, daemon=True)
        self.__thread.start()

    def __find_option(self, lines, option_name):
        """
        Find the value of an option inside an HTTP header.

        :param lines: A list of all the lines of the HTTP header.
        :param option_name: The name of the option to search for.
        :return: The value of the option.
        """
        option = list(filter(lambda line: line.lower().startswith(option_name.lower()), lines))[-1]
        return option[(option.find(":") + 1):]

    def __process(self):
        """
        Process the video stream.
        """
        # Send header
        http_request = f"GET {self.host['path']} HTTP/1.1\r\n"
        http_request += "User-Agent: Lavf/58.29.100\r\n"
        http_request += "Accept: */*\r\n"
        http_request += "Range: bytes=0-\r\n"
        http_request += "Connection: close\r\n"
        http_request += f"Host: {self.host['host_address']}:{self.host['host_port']}\r\n"
        http_request += "Icy-MetaData: 1\r\n\r\n"

        self.__socket.send(http_request.encode())

        # Read response header
        stream_header = self.__socket.read_until(b'\r\n\r\n').decode()
        header_lines = stream_header.split("\r\n")

        if not header_lines[0].split(" ")[1] == "200":
            _Log.error(f"HTTP error encountered: '{header_lines[0]}'")
            return

        self.__status = _ConnectionStatus.CONNECTED

        # Find content type tag
        content_type = self.__find_option(header_lines, "Content-Type").split(";")

        boundary = list(filter(lambda token: token.lower().startswith("boundary="),
                               [t.lstrip() for t in content_type]))[-1]
        boundary = str(boundary[len("boundary="):])

        if not boundary.startswith("--"):
            boundary = "--" + boundary

        last_emit_time = _time.time()
        while self.__running:
            # Read header
            frame_header = self.__socket.read_until(b'\r\n\r\n')

            try:
                frame_header = frame_header.decode()
            except UnicodeDecodeError:
                print(f"Unicode decode error: ({ len(frame_header) }) - { frame_header }")
                break

            header_index = frame_header.find(boundary)

            if header_index < 0:
                _Log.error("Header not found in stream frame")
                continue

            frame_header = frame_header[header_index:]
            frame_header_lines = frame_header.split("\r\n")

            if frame_header_lines[0] != boundary:
                _Log.error("Expected frame boundary at line 0. Not found!")
                continue

            frame_type = self.__find_option(frame_header_lines, "Content-Type").lstrip()
            frame_length = int(self.__find_option(frame_header_lines, "Content-Length").lstrip())

            # Read frame
            frame_data = self.__socket.read_amount(frame_length)

            self.__image_lock.acquire()
            self.__image_buffer = bytearray(len(frame_data))
            self.__image_buffer[:] = frame_data
            self.__image_lock.release()

            # Emit signal
            current_time = _time.time()
            if current_time - last_emit_time >= _DELAY:
                self.invoke_frame_callback()
                last_emit_time = current_time

        self.__status = _ConnectionStatus.DISCONNECTED

    @property
    def frame_raw(self) -> bytearray:
        """
        Get the last frame received by the stream.

        :return: A bytearray that contains the raw JPEG image data.
        """
        self.__image_lock.acquire()
        frame_data = self.__image_buffer
        self.__image_lock.release()

        return frame_data

    @property
    def raw_type(self):
        return "jpeg"

    @property
    def frame(self) -> _np.ndarray:
        """
        Get the last frame received by the stream.

        :return: An array of the pixels of the frame.
        """
        frame_data = self.frame_raw

        if frame_data is not None:
            return _simplejpeg.decode_jpeg(frame_data)

        return _np.ndarray(shape=[1, 1])

    @property
    def status(self):
        return self.__status

    def close(self):
        """
        Close the stream.
        """
        self.__running = False
