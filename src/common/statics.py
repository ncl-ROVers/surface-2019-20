import os as _os
import logging as _logging


class _RestrictedFileHandler(_logging.FileHandler):
    """
    Unfortunately has to be here due to circular imports

    TODO: Document
    """

    def __init__(self, filename, *args, **kwargs):
        _logging.FileHandler.__init__(self, filename, *args, **kwargs)

    def emit(self, record):
        """
        TODO: Document
        """

        if not record.levelno == self.level:
            return
        else:
            return _logging.FileHandler.emit(self, record)


# Declare path to the root folder (surface)
ROOT_DIR = _os.path.normpath(_os.path.join(_os.path.dirname(__file__), "..", ".."))

# Declare paths to the main folders
ASSETS_DIR = _os.path.join(ROOT_DIR, "assets")
SRC_DIR = _os.path.join(ROOT_DIR, "src")

# Declare the paths to the source paths
COMMON_DIR = _os.path.join(SRC_DIR, "common")
GUI_DIR = _os.path.join(SRC_DIR, "gui")
LOG_DIR = _os.path.join(SRC_DIR, "log")
