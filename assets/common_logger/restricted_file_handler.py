"""
Restricted File Handler
=======================

Helper module storing the class to load in the `config.json` file.
"""
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