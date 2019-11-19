import logging as _logging
import inspect as _inspect
import os
# Rough version

class _VerboseFileHandler(_logging.FileHandler):

    def __init__(self, filename, *args, **kwargs):
        _logging.FileHandler.__init__(self, filename, *args, **kwargs)

    def emit(self, record):

        def get_frame():
            """Return the frame that called the logging function."""
            stack = _inspect.stack()
            # Traverse backwards through the stack to find the first frame that has the filename "logger.py". The frame
            # following that is the calling frame.
            i = len(stack) - 1
            while i >= 0:
                if os.path.basename(stack[i].filename) == "logger.py":
                    return stack[i + 1][0]
                i -= 1

        caller = _inspect.getframeinfo(get_frame())

        # `filename' needs to give more of the path; treat `surface' directory as root?
        record.v_filename = os.path.basename(caller.filename)
        # TODO should have the parent function/class
        record.v_function = caller.function
        record.v_lineno = caller.lineno

        _logging.FileHandler.emit(self, record)
