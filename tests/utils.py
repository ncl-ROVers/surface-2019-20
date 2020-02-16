"""
Test utils
==========

Standard utils module storing common to the package classes, functions, constants, and other objects.
"""
import os as _os

# Declare some root-level directories
ROOT_DIR = _os.path.normpath(_os.path.join(_os.path.dirname(__file__), ".."))
TESTS_DIR = _os.path.join(ROOT_DIR, "tests")

# Declare assets-related directories
TESTS_ASSETS_DIR = _os.path.join(TESTS_DIR, "assets")
TESTS_ASSETS_LOG_DIR = _os.path.join(TESTS_ASSETS_DIR, "log")
TESTS_ASSETS_VISION_DIR = _os.path.join(TESTS_ASSETS_DIR, "vision")


def get_log_files(directory: str) -> set:
    """
    Helper function used to retrieve a set of absolute paths to the log files.

    :param directory: Path to the directory with the log files
    :return: A set of paths
    """
    files = set()
    for file in _os.listdir(directory):
        if file.endswith(".log"):
            files.add(_os.path.join(directory, file))
    return files
