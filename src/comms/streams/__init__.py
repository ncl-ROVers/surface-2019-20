"""
Streams
=======

Streaming tools handling different types of video streams

.. moduleauthor::
    Jason Philippou <i.philippou1@newcastle.ac.uk>
"""
from .http_stream import HTTPStreamReader
from .rtsp_stream import RTSPStreamReader

from .video_stream_reader import VideoStreamReader as _VideoStreamReader


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


def stream_from_url(url: str) -> _VideoStreamReader:
    """
    Create a video stream reader compatible with the url provided

    :param url: The url of the stream
    :return: The reader for the particular type of stream
    """
    url_tokens = parse_url(url)

    if url_tokens["protocol"] == "http":
        return HTTPStreamReader(url_tokens)
    elif url_tokens["protocol"] == "rtsp":
        return RTSPStreamReader(url_tokens)

    return
