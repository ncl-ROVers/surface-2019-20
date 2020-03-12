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
import warnings as _warnings

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


def _parse_sdp_content(content: str):
    content_data = {}

    body_lines = content.split("\r\n")
    i = 0

    while i < len(body_lines):
        try:
            if len(body_lines[i]) < 1:
                continue

            if body_lines[i][0] == 'v':  # Parse version number
                version = int(body_lines[i][2:])
                if version != 0:
                    raise SyntaxError(f"Invalid protocol version number {version}.")
            elif body_lines[i][0] == 'o':  # Parse originator field
                tokens = body_lines[i][2:].split(' ')

                if not len(tokens) == 6:
                    raise SyntaxError(f"SDP originator field 'o' must have six fields. {len(tokens)} were provided!")

                content_data["originator"] = {}
                content_data["originator"]["name"] = tokens[0]
                content_data["originator"]["session"] = tokens[1]
                content_data["originator"]["username"] = tokens[2]
                content_data["originator"]["id"] = tokens[3]
                content_data["originator"]["version"] = tokens[4]
                content_data["originator"]["net_address"] = tokens[5]
            elif body_lines[i][0] == 's':  # Parse session name
                session_name = body_lines[i][2:]

                if len(session_name) < 1:
                    raise SyntaxError("Session name must be at least one character long!")

                content_data["name"] = session_name
            elif body_lines[i][0] == 'i':  # Parse session title/information
                session_info = body_lines[i][2:]

                if len(session_info) <= 0:
                    _warnings.warn(f"Session information field 'i' used but no information provided! " +
                                   "This field will be skipped.", SyntaxWarning)
                    continue

                content_data["info"] = session_info
            elif body_lines[i][0] == 'u':  # Parse URI of description
                uri_desc = body_lines[i][2:]

                if len(uri_desc) <= 0:
                    _warnings.warn(f"Description URI field 'u' used but no URI provided! " +
                                   "This field will be skipped.", SyntaxWarning)
                    continue

                content_data["uri_desc"] = uri_desc
            elif body_lines[i][0] == 'e':  # Parse contact emails
                emails = body_lines[i][2:]

                if len(emails) > 0:
                    content_data["emails"] = emails.split(" ")
                else:
                    content_data["emails"] = []
            elif body_lines[i][0] == 'p':  # Parse contact phone numbers
                phones = body_lines[i][2:]

                if len(phones) > 0:
                    content_data["phones"] = phones.split(" ")
                else:
                    content_data["phones"] = []
            elif body_lines[i][0] == 'c':  # Parse connection information
                connection = body_lines[i][2:].split(" ")

                if len(connection) < 3:
                    _warnings.warn(
                        f"At least three values must be provided for the connection information field 'c', " +
                        f"but only {len(connection)} were found. This field will be skipped.", SyntaxWarning)
                    continue

                content_data["connection_info"] = {}
                content_data["connection_info"]["net_type"] = connection[0]
                content_data["connection_info"]["addr_type"] = connection[1]
                content_data["connection_info"]["address"] = connection[2]
            elif body_lines[i][0] == 'b':  # Parse bandwidth information
                bandwidth_info = body_lines[i][2:]
                tokens = bandwidth_info.split(":")

                if not len(tokens) == 2:
                    _warnings.warn(f"Bandwidth field 'b' must have two values, not {len(tokens)}. " +
                                   "This field will be skipped.", SyntaxWarning)
                    continue

                if len(tokens) > 0:
                    bw_list = content_data.get("bandwidths", [])

                    bw_list.append({"type": tokens[0], "value": tokens[1]})
                    content_data["bandwidths"] = bw_list
            elif body_lines[i][0] == 't':  # Parse timing description
                time_tokens = body_lines[i][2:].split(" ")

                if not len(time_tokens) == 2:
                    _warnings.warn(f"Timing field 't' must have two values, not {len(time_tokens)}. " +
                                   "This field will be skipped.", SyntaxWarning)
                    continue

                time_desc = {
                    "start_time": time_tokens[0],
                    "end_time": time_tokens[1],
                    "repeat_times": []
                }

                while (len(body_lines) > (i + 1)) and (body_lines[i + 1][0] == 'r'):
                    repeat_tokens = body_lines[i + 1][2:].split(" ")

                    if not len(repeat_tokens) == 3:
                        _warnings.warn(f"Repeat timing field 'r' must have three values, not {len(repeat_tokens)}. " +
                                       "This field will be skipped.", SyntaxWarning)
                        continue

                    time_desc["repeat_times"].append({
                        "interval": repeat_tokens[0],
                        "duration": repeat_tokens[1],
                        "offset": repeat_tokens[2]
                    })

                    i += 1

                times = content_data.get("time_descriptions", [])
                times.append(time_desc)

                content_data["time_descriptions"] = times
            elif body_lines[i][0] == 'r':  # Parse repeat timing line
                _warnings.warn(f"Repeat time field 'r' detected outside of time description. " +
                               "This field will be skipped.", SyntaxWarning)
            elif body_lines[i][0] == 'z':  # Parse time zone info
                zone_tokens = body_lines[i][2:].split(" ")

                if (len(zone_tokens) < 2) or (len(zone_tokens) % 2 == 1):
                    _warnings.warn(f"Time zone field 'r' must have an even, positive number of values. " +
                                   "This field will be skipped.", SyntaxWarning)
                    continue

                content_data["zones"] = [(zone_tokens[i], zone_tokens[i + 1]) for i in range(0, len(zone_tokens, 2))]
            elif body_lines[i][0] == 'k':
                enc_tokens = body_lines[i][2:].split(":")

                if len(enc_tokens) == 1:
                    content_data["encryption"]["method"] = enc_tokens[0]
                elif len(enc_tokens) == 2:
                    content_data["encryption"]["method"] = enc_tokens[0]
                    content_data["encryption"]["key"] = enc_tokens[1]
                else:
                    _warnings.warn(f"Encryption key field 'k' must have either one or two values. " +
                                   "This field will be skipped.", SyntaxWarning)
                    continue
            elif body_lines[i][0] == "m":
                media_tokens = body_lines[i][2:]
        finally:
            i += 1

    return content_data


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
            self.__host_url += str(self.host['host_port'])
        self.__host_url += self.host['path']

        self.__running = False
        self.__socket = None

        self.__thread = None

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

    def __request_options(self):
        request = f"OPTIONS { self.__host_url } RTSP/1.0\r\n"
        request += "Require: implicit-play\r\n"
        request += "Proxy-Require: gzipped-messages\r\n\r\n"

        self.__socket.send(request.encode())

        return self.__socket.read_until(b'\r\n\r\n').decode()

    def __request_description(self):
        request = f"DESCRIBE { self.__host_url } RTSP/1.0\r\n\r\n"

        self.__socket.send(request.encode())

        # Read header
        response_header = self.__socket.read_until(b'\r\n\r\n').decode()
        header_lines = response_header.split("\r\n")

        # Read content
        content_length = int(_http_utils.http_find_option(header_lines, "Content-Length"))
        response_body = self.__socket.read_amount(content_length).decode()

        # Parse content
        content_type = _http_utils.http_find_option(header_lines, "Content-Type").lstrip()

        if not content_type.startswith("application/sdp"):
            raise NotImplementedError(f"RTSP content type '{ content_type }' is not currently supported!")

        # Content provided will be in the SDP (Session Description Protocol) format
        sdp_content = _parse_sdp_content(response_body)
        _Log.info(str(sdp_content))

        return response_body

    def __process(self):
        """
        Process the video stream.
        """
        test_body = "v=0\r\n" + \
            "o=- 774661722 774661722 IN IP4 127.0.0.1\r\n" + \
            "s=hessdalen03.stream\r\n" + \
            "i=Test stream description\r\n" + \
            "u=http://example.org\r\n" + \
            "c=IN IP4 0.0.0.0\r\n" + \
            "b=CT:12860\r\n" + \
            "b=RT:1806\r\n" + \
            "t=0 0\r\n" + \
            "r=0 0 0\r\n" + \
            "a=sdplang:en\r\n" + \
            "a=range:npt=now-\r\n" + \
            "a=control:*\r\n" + \
            "m=audio 0 RTP/AVP 96\r\n" + \
            "a=rtpmap:96 mpeg4-generic/48000/2\r\n" + \
            "a=fmtp:96 profile-level-id=1;mode=AAC-hbr;sizelength=13;indexlength=3;indexdeltalength=3;config=1190\r\n" + \
            "a=control:trackID=1\r\n" + \
            "m=video 0 RTP/AVP 97\r\n" + \
            "a=rtpmap:97 H264/90000\r\n" + \
            "a=fmtp:97 packetization-mode=1;profile-level-id=42001E;sprop-parameter-sets=Z2QAKK2wpDBSAgFxQWKQPQRWFIYKQEAuKCxSB6CKwpDBSAgFxQWKQPQRTDoUKQNC4oJHMGIemHQoUgaFxQSOYMQ9MOhQpA0LigkcwYh6xEQmIVilsQRWUURJsogxOU4QITKUIEVlCCTYQVhBMJQhMIjGggWQJFaIGBJZBAaEnaMIDwsSWQQKCwsrRBQYOWQweO0YEBZASNAogszlAUAW7ARAAAH0gADqYBgAAAMDk4cAAA7msr//4wAAAwBycOAAAdzWV//8aA==,aP48sA==\r\n" + \
            "a=cliprect:0,0,720,1280\r\n" + \
            "a=framesize:97 1280-720\r\n" + \
            "a=framerate:59.94\r\n" + \
            "a=control:trackID=2\r\n"

        _Log.info("Prasing message...")
        stuff = _parse_sdp_content(test_body)
        _Log.info(str(stuff))
        #_Log.info(self.__request_description())

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
