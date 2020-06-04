"""
RTSP Stream
==========

Module storing an rtsp-based implementation of a video stream reader to a network camera.

More information about the protocol can be found at: https://tools.ietf.org/html/rfc4566#page-14
"""

import socket as _socket
from src.comms.utils import STREAM_THREAD_DELAY as _DELAY
from .buffered_socket import BufferedSocket as _BufferedSocket
from .video_stream_reader import VideoStreamReader as _VideoStreamReader
from ..utils import ConnectionStatus as _ConnectionStatus
from src.common import Log as _Log
import threading as _threading

from src.common import utils
from . import utils as _http_utils


def _parse_options(response: str):
    tokens = response.split("\r\n")

    for line in tokens:
        if line.lstrip().lower().startswith("public"):
            collon_index = line.index(":")

            if collon_index > 0:
                return [opt.lstrip().rstrip() for opt in line[(collon_index + 1):].split(",")]
            else:
                return []

    return []

class RTSPStreamReader(_VideoStreamReader):
    """
    RTSP video stream reader.
    """

    def __init__(self, host_properties):
        """
        Standard constructor.

        Parses the video stream URL and initializes stream variables.

        :param host_properties: The components of the url to connect to (as returned by the 'parse_url' method)
        """
        super().__init__(host_properties)

        self.__host_url = f"{ self.host['protocol'] }://{ self.host['host_address'] }"
        if not self.host['host_port'] == 80:
            self.__host_url += ":" + str(self.host['host_port'])
        self.__host_url += self.host['path']

        self.__running = False
        self.__socket = None

        self.__thread = None

        self.__sequence_index = 1
        self.__status = _ConnectionStatus.DISCONNECTED

    def open_stream(self):
        _Log.info(f"Connecting to {self.host['host_address']}:{self.host['host_port']}.")

        # Connect socket to server
        self.__socket = _BufferedSocket(_socket.AF_INET, _socket.SOCK_STREAM)
        self.__socket.connect((self.host["host_address"], self.host["host_port"]))

        self.__running = True

        self.__status = _ConnectionStatus.CONNECTING

        # Start streaming thread
        self.__process()
        # self.__thread = _threading.Thread(target=self.__process, daemon=True)
        # self.__thread.start()

    def __check_header_cseq(self, header_lines):
        cseq_value = _http_utils.http_find_option(header_lines, "CSeq")

        if len(cseq_value) <= 0:
            return

        if int(cseq_value) != self.__sequence_index:
            raise ValueError(f"Invalid CSeq value ({ self.__sequence_index } != { int(cseq_value) }).")

    def __check_header_code(self, header_lines):
        error_code = int(header_lines[0].split(" ")[1])

        if error_code // 100 != 2:
            raise RuntimeError(f"RTSP header error code: { error_code } { ' '.join(header_lines[0].split(' ')[2:]) }")

    def __check_http_response_content(self, header_lines):
        content_length = _http_utils.http_find_option(header_lines, "ContentLength")

        if len(content_length) < 1:
            return

        content_length = int(content_length)
        self.__socket.read_amount(content_length)

    def __request_options(self):
        request = f"OPTIONS { self.__host_url } RTSP/1.0\r\n"
        request += f"CSeq: { self.__sequence_index }\r\n"
        request += "Proxy-Require: gzipped-messages\r\n\r\n"

        # Send request
        self.__socket.send(request.encode())

        # Wait for response
        response_header = self.__socket.read_until(b'\r\n\r\n').decode()
        header_lines = response_header.split("\r\n")

        self.__check_header_code(header_lines)
        self.__check_http_response_content()

        # HTTP CSeq check
        self.__check_header_cseq(header_lines)
        self.__sequence_index += 1

        # Return option list
        return _http_utils.http_find_option(header_lines, "Public").replace(" ", "").split(",")

    def __request_description(self):
        request = f"DESCRIBE { self.__host_url } RTSP/1.0\r\n"
        request += f"CSeq: { self.__sequence_index }\r\n\r\n"

        # Send request
        self.__socket.send(request.encode())

        # Wait for response
        response_header = self.__socket.read_until(b'\r\n\r\n').decode()
        header_lines = response_header.split("\r\n")

        self.__check_header_code(header_lines)
        self.__check_http_response_content()

        # HTTP CSeq check
        self.__check_header_cseq(header_lines)
        self.__sequence_index += 1

        # Read content
        content_length = int(_http_utils.http_find_option(header_lines, "Content-Length"))
        response_body = self.__socket.read_amount(content_length).decode()

        # Parse content
        content_type = _http_utils.http_find_option(header_lines, "Content-Type").lstrip()

        if not content_type.startswith("application/sdp"):
            raise NotImplementedError(f"RTSP content type '{ content_type }' is not currently supported!")

        # Content provided will be in the SDP (Session Description Protocol) format
        return _http_utils.parse_sdp_content(response_body)

    def __request_setup(self, media_url):
        request = f"SETUP { media_url } RTSP/1.0\r\n"
        request += f"CSeq: { self.__sequence_index }\r\n"
        request += "Transport: RTP/AVP;unicast;client_port=8000-8001\r\n\r\n"

        self.__socket.send(request.encode())

        # Read header
        response_header = self.__socket.read_until(b'\r\n\r\n').decode()
        header_lines = response_header.split("\r\n")

        self.__check_header_code(header_lines)
        self.__check_http_response_content()

        # HTTP CSeq check
        self.__check_header_cseq(header_lines)
        self.__sequence_index += 1

        transport = _http_utils.http_find_option(header_lines, "Transport")
        _Log.info(response_header)

        for token in transport.split(";"):
            if token.lower().startswith("server_port"):
                _Log.info(token[12:])

        # Transport: RTP/AVP/UDP;unicast;client_port=8000-8001;server_port=64782-64783;ssrc=75DF6CFB;mode=play

    def __request_play(self, media_url):
        request = f"PLAY { media_url } RTSP/1.0\r\n"
        request += f"CSeq: { self.__sequence_index }\r\n\r\n"

        self.__socket.send(request.encode())

        # Read header
        response_header = self.__socket.read_until(b'\r\n\r\n').decode()
        header_lines = response_header.split("\r\n")

        self.__check_header_code(header_lines)
        self.__check_http_response_content()

        # HTTP CSeq check
        self.__check_header_cseq(header_lines)
        self.__sequence_index += 1

        # _Log.info("\n")
        _Log.info(response_header)

    def __find_video_media_info(self, stream_desc):
        for media_desc in stream_desc["media_descriptions"]:
            if not media_desc["media"]["type"].lower() == "video":
                continue

            # Check if the cerent video stream is an H265 stream
            temp_attribs = []
            temp_attribs.extend(media_desc["attributes"])
            temp_attribs.extend(stream_desc["attributes"])

            h265_supported = False
            for attrib in temp_attribs:
                if attrib[0] == "rtpmap":
                    h265_supported = attrib[1].split(" ")[1].split("/")[0].upper() == "H265"
                    break

            if not h265_supported:
                continue

            # Find URL of current video media
            for attrib in temp_attribs:
                if attrib[0] == "control":
                    return attrib[1]

        return None

    def __process(self):
        """
        Process the video stream.
        """
        options = self.__request_options()

        if utils.index_of_safe(options, "DESCRIBE") == -1 and utils.index_of_safe(options, "describe") == -1:
            raise RuntimeError("Option DESCRIBE not supported by server")

        stream_desc = self.__request_description()
        video_url = self.__find_video_media_info(stream_desc)

        if video_url is None:
            raise RuntimeError("Valid video media not provided by stream")

        self.__request_setup(video_url)
        self.__request_play(video_url)

        self.__socket.close()

    @property
    def frame_raw(self):
        pass

    @property
    def frame(self):
        pass

    @property
    def raw_type(self) -> str:
        return "h265"

    @property
    def status(self) -> _ConnectionStatus:
        return self.__status

    def close(self):
        """
        Close the stream.
        """
        self.__running = False
