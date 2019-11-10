from .utils import get_tests
from src.common import LOG_DIR, Log
import os


def main():
    """
    TODO: Document

    :return:
    """

    for test_func in get_tests(__name__).values():
        test_func()


def get_log_files():
    """
    TODO: Document

    :return:
    """

    files = set()
    for file in os.listdir(LOG_DIR):
        if file.endswith(".log"):
            files.add(os.path.join(LOG_DIR, file))
    return files


def test_create_logs():
    """
    TODO: Document

    :return:
    """

    Log.debug("Test debug message")
    Log.info("Test info message")
    Log.warning("Test warning message")
    Log.error("Test error message")

    # There should be 5 files created - each for the log level and a verbose for all levels combined
    assert(len(get_log_files()) == 5)


def test_level_filtering():
    """
    TODO: Document

    :return:
    """

    for file in get_log_files():
        with open(file) as f:
            if "verbose" in file:
                assert(len(f.readlines()) == 4)
            else:
                assert(len(f.readlines()) == 1)