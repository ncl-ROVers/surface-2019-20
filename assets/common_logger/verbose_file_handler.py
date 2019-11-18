import logging as _logging
import inspect as _inspect
import os
# Rough version

class _VerboseFileHandler(_logging.FileHandler):

    def __init__(self, filename, *args, **kwargs):
        _logging.FileHandler.__init__(self, filename, *args, **kwargs)

    def emit(self, record):
        # [7] as: (0)here <- (1)`Handler.handle' in logging/__init.py__ <- (2)`Logger.callHandlers' in
        # logging/__init.py__ <- (3)`Logger.handle' in logging/__init.py__ <- (4)`Logger._log' in logging/__init.py__
        # <- (5) `Logger.$SEVERITY' in logging/__init.py__ <- (6) `Log.$SEVERITY' in surface/.../logger.py <- (7) call
        # TODO: change this to be done programmatically, as just using an array access is dependent on Python's
        #  internal details. Maybe loop down from (len(_inspect.stack()) -1) until we find "logger.py",
        #  the stack entry after that one being the one we want.
        caller = _inspect.getframeinfo(_inspect.stack()[7][0])

        # `fileName' needs to give more of the path; treat `surface' directory as root?
        record.fileName = os.path.basename(caller.filename)
        # should have the parent function/class
        record.function = caller.function
        record.lineNum = str(caller.lineno)

        _logging.FileHandler.emit(self, record)
