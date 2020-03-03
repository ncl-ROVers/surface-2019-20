"""
Stream
======

Module storing an implementation of a stream-based connection to a network camera.
"""
import socket as _socket
from .utils import DEFAULT_STREAM_WIDTH as _DEFAULT_WIDTH, DEFAULT_STREAM_HEIGHT as _DEFAULT_HEIGHT, \
    STREAM_THREAD_DELAY as _DELAY
from ..common import Log as _Log
from PySide2.QtGui import QImage as _QImage, QPixmap as _QPixmap
from PySide2.QtCore import QObject as _QObject, Signal as _Signal, QByteArray as _QByteArray
import threading as _threading
import simplejpeg as _simplejpeg
import numpy as _np
import time as _time


def parse_url(stream_url: str):
    """
    Parse a URL and extracts its components (protocol, host address, host port, file)

    :param stream_url: The URL to be parsed

    :return: Returns a dictionary containing the parsed valued
    """
    parse_index = 0

    url_data = {}

    # Parse url protocol
    protocol = "http"
    protocol_length = stream_url.find('://')

    if protocol_length > 1:
        protocol = stream_url[:protocol_length]

    parse_index += protocol_length + 3

    # Parse url host
    host_name_size = stream_url[parse_index:].find('/')
    if host_name_size <= 0:
        host_name_size = len(stream_url) - parse_index

    host = stream_url[parse_index:(host_name_size + parse_index)]

    parse_index += host_name_size

    # Parse url file
    path = stream_url[parse_index:]

    # Extract address and port
    colon_index = host.find(':')

    port = 80
    if colon_index > 0:
        port = int(host[(colon_index + 1):])
    else:
        colon_index = len(host)

    address = host[:colon_index]

    url_data["protocol"] = protocol
    url_data["host_address"] = address
    url_data["host_port"] = port
    url_data["path"] = path

    return url_data


class VideoStream(_QObject):
    """
    Video stream class used to capture an MJPEG stream.

    Handles fetching frames from a remote address and their conversion to raw pixel format.

    Usage
    -----

    A stream object can be created as follows:

        capture = VideoStream(URL)

    where `URL` is a valid URL in string format.

    The capture will not begin until the `connect` function is called, which will
    spawn a new thread that handles stream processing.

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

        self.__host = parse_url(stream_url)

        protocol = self.__host["protocol"]
        if not protocol == "http":
            _Log.error(f"Protocol '{protocol}' not supported!")
            exit()

        self.__stream_buffer = bytearray()
        self.__running = False
        self.__socket = None

        # Image buffer
        self.__image_buffer = None
        self.__image_lock = _threading.Lock()

        self.__thread = None

        self.__open_stream()

    def __open_stream(self):
        """
        Connect to the host and start the stream thread.
        """
        _Log.info(f"Connecting to {self.__host['host_address']}:{self.__host['host_port']}.")

        # Connect socket to server
        self.__socket = _socket.socket(_socket.AF_INET, _socket.SOCK_STREAM)
        self.__socket.connect((self.__host["host_address"], self.__host["host_port"]))

        self.__running = True

        # Start streaming thread
        self.__thread = _threading.Thread(target=self.__process, daemon=True)
        self.__thread.start()

    def __read_ahead(self):
        """
        Read bytes from the socket into the stream buffer.
        """
        data = self.__socket.recv(4096)
        self.__stream_buffer.extend(data)

    def __collapse_head(self, head_size):
        """
        Remove the section [0, head_size) from the start of the buffer.
        The remaining data will be moved to the beginning of the buffer.

        :param head_size: The amount of bytes to remove from the start of the buffer.
        """
        self.__stream_buffer = self.__stream_buffer[head_size:]

    def __read_until(self, delim):
        """
        Read from the strean until 'delim' is encountered.

        :param delim: The sequence of bytes that terminates reading.
        """
        delim_index = 0

        while True:
            if delim_index >= len(self.__stream_buffer):
                self.__read_ahead()

            if self.__stream_buffer[delim_index:(delim_index + len(delim))] == bytearray(delim):
                break

            delim_index += 1

        data = self.__stream_buffer[:delim_index]
        self.__collapse_head(delim_index + len(delim))

        return data

    def __read_amount(self, count):
        """
        Read a number of bytes from the stream.

        :param count: The number of byets to be read.
        """
        while len(self.__stream_buffer) < count:
            self.__read_ahead()

        data = self.__stream_buffer[:count]
        self.__collapse_head(count)

        return data

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
        http_request = f"GET {self.__host['path']} HTTP/1.1\r\n"
        http_request += "User-Agent: Lavf/58.29.100\r\n"
        http_request += "Accept: */*\r\n"
        http_request += "Range: bytes=0-\r\n"
        http_request += "Connection: close\r\n"
        http_request += f"Host: {self.__host['host_address']}:{self.__host['host_port']}\r\n"
        http_request += "Icy-MetaData: 1\r\n\r\n"

        self.__socket.send(http_request.encode())

        # Read response header
        stream_header = self.__read_until(b'\r\n\r\n').decode()
        header_lines = stream_header.split("\r\n")

        if not header_lines[0].split(" ")[1] == "200":
            _Log.error(f"HTTP error encountered: '{header_lines[0]}'")
            return

        # Find content type tag
        content_type = self.__find_option(header_lines, "Content-Type").split(";")

        boundary = list(filter(lambda token: token.lower().startswith("boundary="), [t.lstrip() for t in content_type]))[-1]
        boundary = str(boundary[len("boundary="):])

        if not boundary.startswith("--"):
            boundary = "--" + boundary

        last_emit_time = _time.time()
        while self.__running:
            # Read header
            frame_header = self.__read_until(b'\r\n\r\n').decode()

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
            frame_data = self.__read_amount(frame_length)

            self.__image_lock.acquire()
            self.__image_buffer = bytearray(len(frame_data))
            self.__image_buffer[:] = frame_data
            self.__image_lock.release()

            # Emit signal
            current_time = _time.time()
            if current_time - last_emit_time >= _DELAY:
                self.frame_received.emit(self.frame_qt)
                last_emit_time = current_time

        return

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
    def frame(self) -> _np.ndarray:
        """
        Get the last frame received by the stream.

        :return: An array of the pixels of the frame.
        """
        frame_data = self.latest_frame_raw()

        if frame_data is not None:
            return _simplejpeg.decode_jpeg(frame_data)

        return _np.ndarray(shape=[1, 1])

    @property
    def frame_qt(self) -> _QPixmap:
        """
        Getter for the frame (QT format).

        Transforms the frame into a QPixelmap.
        """
        image = _QImage()
        image.loadFromData(_QByteArray(self.frame_raw), aformat="jpeg")
        pixel_map = _QPixmap.fromImage(image)
        return pixel_map

    def close(self):
        """
        Close the stream.
        """
        self.__running = False
