"""
Logger
======

Module storing an implementation of a static log class and all values associated with it.
"""

from ..common import LOG_DIR as _LOG_DIR, SRC_LOG_DIR as _SRC_LOG_DIR
import logging as _logging
import logging.config as _config
import json as _json
import subprocess as _subprocess
import os as _os

_DEFAULT_LOG_DIR = _LOG_DIR
_DEFAULT_CONFIG_FILE_PATH = _os.path.join(_SRC_LOG_DIR, "config.json")
_FILE_HANDLERS = {"logging.FileHandler", "src.common.statics._RestrictedFileHandler"}


def _get_logger(config_file_path: str = "", log_directory: str = "") -> _logging.Logger:
    """
    Helper function to configure the built-in logging module and retrieve a logger object.

    Uses (and modifies when needed) the a JSON configuration file, which by default is `config.json`.

    :param config_file_path: Path to the JSON configuration file
    :param log_directory: Path to where the logs should be stored
    :raises: Log.LogError
    :return: Python's built-in logger object
    """

    # Use the default config file path if it's not set
    if not config_file_path:
        config_file_path = _DEFAULT_CONFIG_FILE_PATH

    # Use the default log directory if it's not set
    if not log_directory:
        log_directory = _DEFAULT_LOG_DIR

    # Verify both paths are correct or throw an error
    if not _os.path.exists(config_file_path):
        raise Log.LogError(f"Failed to find the log config file at {config_file_path}")
    if not _os.path.exists(log_directory):
        raise Log.LogError(f"The log directory does not exist - {log_directory}")

    try:
        with open(config_file_path, "r") as f:
            config = _json.load(f)

            # Extract the handlers and update the paths within them to use the correct folder
            handlers = config["handlers"]
            for handler in handlers:
                if handlers[handler]["class"] in _FILE_HANDLERS:
                    handlers[handler]["filename"] = _os.path.join(log_directory, handlers[handler]["filename"])

    except OSError as e:
        raise Log.LogError(f"An error occurred while setting up the logging module - {e}")

    # Load the configuration and return the logger object
    _config.dictConfig(config)
    return _logging.getLogger()


class Log:
    """
    Static logging class which uses a Python's built-in logger object for the actual logging tasks.

    Defines a :class:`LogError` class to handle errors and let the calling function handle them.

    Functions
    ---------

    The following list shortly summarises each function:

        * reconfigure - a method to change the files' location
        * debug - a method to log a debug message
        * info - a method to log an info message
        * warning - a method to log a warning message
        * error - a method to log an error message
        * command result - a method to log a result of a command

    Usage
    -----

    This screen should only be switched to once, and its func:`load` method called.
    """

    # Initialise the logger
    _logger = _get_logger()

    class LogError(Exception):
        """
        A standard exception to handle log-related errors.
        """
        pass

    @classmethod
    def reconfigure(cls, *, config_file_path: str = "", log_directory: str = ""):
        """

        :param config_file_path: Path to the JSON configuration file
        :param log_directory:  Path to where the log files should be stored
        """
        # Update the logger with both new values (or use the empty strings as default to use the default paths)
        cls._logger = _get_logger(config_file_path, log_directory)

    @classmethod
    def debug(cls, message: str, *args, **kwargs):
        """
        Standard debug logging.

        :param message: Message to log
        :param args: Args passed to the internal logger
        :param kwargs: Kwargs passed to the internal logger
        """
        cls._logger.debug(message, *args, **kwargs)

    @classmethod
    def info(cls, message: str, *args, **kwargs):
        """
        Standard info logging.

        :param message: Message to log
        :param args: Args passed to the internal logger
        :param kwargs: Kwargs passed to the internal logger
        """
        cls._logger.info(message, *args, **kwargs)

    @classmethod
    def warning(cls, message: str, *args, **kwargs):
        """
        Standard warning logging.

        :param message: Message to log
        :param args: Args passed to the internal logger
        :param kwargs: Kwargs passed to the internal logger
        """
        cls._logger.warning(message, *args, **kwargs)

    @classmethod
    def error(cls, message: str, *args, **kwargs):
        """
        Standard error logging.

        :param message: Message to log
        :param args: Args passed to the internal logger
        :param kwargs: Kwargs passed to the internal logger
        """
        cls._logger.error(message, *args, **kwargs)

    @classmethod
    def command_result(cls, command_result: _subprocess.CompletedProcess):
        """
        Method used to log return code as info, stdout as debug and stderr as error.

        :param command_result: Result from subprocess.run or similar
        """

        Log.info("The command returned {}, logging stdout and stderr...".format(command_result.returncode))

        # Log stdout as info
        if command_result.stdout:
            cls._logger.debug(command_result.stdout.decode("ascii"))

        # Log stderr as error
        if command_result.stderr:
            cls._logger.error(command_result.stderr.decode("ascii"))
