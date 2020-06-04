"""
Main
====

Main execution module.

To run the code, call::
    python surface

where `python` is Python3.8.1 version and `surface` is relative or absolute path to the directory in which this file is.
"""
from src import gui
from src.comms import streams

if __name__ == "__main__":
    reader = streams.stream_from_url("rtsp://127.0.0.1:8554/video.stream")
    reader.open_stream()

    reader.close()

    # Fetch and exit with the return code of the application execution
    # exit(gui.start())