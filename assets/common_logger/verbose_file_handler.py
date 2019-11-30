"""
TODO: Document
"""
import logging as _logging
import inspect as _inspect
import os as _os


def _get_frame():
    """
    Return the frame that called the logging function.
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
    TODO: Document
    """

    def __init__(self, filename, *args, **kwargs):
        _logging.FileHandler.__init__(self, filename, *args, **kwargs)

    def emit(self, record):
        """
        TODO: Document

        :param record:
        :return:
        """
        caller = _inspect.getframeinfo(_get_frame())

        # TODO: `filename' needs to give more of the path; treat `surface' directory as root?
        record.v_filename = _os.path.basename(caller.filename)
        # TODO should have the parent function/class
        record.v_function = caller.function
        record.v_lineno = caller.lineno

        _logging.FileHandler.emit(self, record)
