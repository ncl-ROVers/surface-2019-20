"""
Common Statics
==============

Standard statics module storing all constants, classes and other objects which do not change throughout the execution
of the program.
"""

import os as _os
import logging as _logging


class _RestrictedFileHandler(_logging.FileHandler):
    """
    Helper file handler class used by the logging configuration.

    Extends a classic file handler be restricting the logging messages to contain only the specified level.

    .. note::

        Due to circular imports, it is impossible to place this class in the :py:mod:`log` package.
    """

    def __init__(self, filename, *args, **kwargs):
        _logging.FileHandler.__init__(self, filename, *args, **kwargs)

    def emit(self, record):
        """
        Overridden function modified to only log records of a matching level.

        :param record: Record used in the emit function
        :return: None if the level's don't match, result of the emit function otherwise
        """

        return _logging.FileHandler.emit(self, record) if record.levelno == self.level else None


# Declare path to the root folder (surface)
ROOT_DIR = _os.path.normpath(_os.path.join(_os.path.dirname(__file__), "..", ".."))

# Declare paths to the main folders
ASSETS_DIR = _os.path.join(ROOT_DIR, "assets")
SRC_DIR = _os.path.join(ROOT_DIR, "src")
LOG_DIR = _os.path.join(ROOT_DIR, "log")

# Declare the paths to the source paths
SRC_COMMON_DIR = _os.path.join(SRC_DIR, "common")
SRC_GUI_DIR = _os.path.join(SRC_DIR, "gui")
SRC_LOG_DIR = _os.path.join(SRC_DIR, "log")

# Declare the paths to the assets folders
GUI_LOADING = _os.path.join(ASSETS_DIR, "gui_loading")
