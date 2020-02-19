"""
Verbose File Handler
====================

Helper module storing the class to load in the config files.

Additionally amends the following logging record fields to give more relevant information:

    * `filename' - file from where the message was logged
    * `function' - function within which the message was logged
    * `lineno' - line number of the log statement
"""
import logging as _logging
import inspect as _inspect
import os as _os

_ROOT_DIR = _os.path.normpath(_os.path.join(_os.path.dirname(__file__), "..", ".."))


def _get_frame():
    """
    Return the frame that called the logging function.

    :return: Frame (see the `inspect' module for details)
    """
    stack = _inspect.stack()[::-1]

    # Traverse backwards through the stack to find the first frame that has the filename "logger.py". The frame
    # following that is the calling frame.
    while stack:
        frame = stack.pop()
        if _os.path.basename(frame.filename) == "logger.py":

            # If logged within logger.py or failed to find it, return the last caller frame.
            try:
                return stack.pop()[0]
            except IndexError:
                return frame


class _VerboseFileHandler(_logging.FileHandler):
    """
    Helper file handler class used for logging configuration.
    
    Any emit to a RestrictedFileHandler is also passed to this, so it is all the levels combined.
    """

    def __init__(self, filename, *args, **kwargs):
        _logging.FileHandler.__init__(self, filename, *args, **kwargs)

    def emit(self, record):
        """
        Overridden function modified so any logging call is put into the verbose file.
        
        :param record: Record used in the emit function
        :return: Result of the emit function
        """
        caller = _inspect.getframeinfo(_get_frame())
        record.filename = _os.path.relpath(caller.filename, _ROOT_DIR)
        record.function = caller.function
        record.lineno = caller.lineno

        return _logging.FileHandler.emit(self, record)
