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
