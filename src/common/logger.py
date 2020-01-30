"""
Logger
======
Module storing an implementation of a static log class and all values associated with it.
The config.json files stored within the assets folder are used to configure most of the logging functionality.
"""
from .utils import LOG_DIR as _LOG_DIR, COMMON_LOGGER_DIR as _COMMON_LOGGER
import logging as _logging
import logging.config as _config
import json as _json
import subprocess as _subprocess
import os as _os
import enum as _enum

_DEFAULT_LOG_DIR = _LOG_DIR
_MAIN_CONFIG_FILE_PATH = _os.path.join(_COMMON_LOGGER, "config_main.json")
# TODO change to "config_hardware.json" once the hardware logging is implemented (#57)
_HARDWARE_CONFIG_FILE_PATH = _os.path.join(_COMMON_LOGGER, "config_main.json")
_FILE_HANDLERS = {"logging.FileHandler", "assets.common_logger.restricted_file_handler._RestrictedFileHandler",
                  "assets.common_logger.verbose_file_handler._VerboseFileHandler"}

# Disable filelock's module logging
_logging.getLogger("filelock").disabled = True


class LogError(Exception):
    """
    A standard exception to handle log-related errors.
    """
    pass


class Logger(_enum.Enum):
    """
    Logger enum used to easily select loggers to reconfigure.
    """
    MAIN = "_main_logger"
    HARDWARE = "_hardware_logger"


def _get_logger(config_file_path: str, *, log_directory: str = "") -> _logging.Logger:
    """
    Helper function to configure the built-in logging module and retrieve a logger object.
    Uses (and modifies when needed) the a JSON configuration file.
    :param config_file_path: Path to the JSON configuration file
    :param log_directory: Path to where the logs should be stored
    :raises: LogError
    :return: Python's built-in logger object
    """

    # Use the default log directory if it's not set
    if not log_directory:
        log_directory = _DEFAULT_LOG_DIR

    # Verify both paths are correct or throw an error
    if not _os.path.exists(config_file_path):
        raise LogError(f"Failed to find the log config file at {config_file_path}")
    if not _os.path.exists(log_directory):
        raise LogError(f"The log directory does not exist - {log_directory}")

    try:
        with open(config_file_path, "r") as f:
            config = _json.load(f)

            # Extract the handlers and update the paths within them to use the correct folder
            handlers = config["handlers"]
            for handler in handlers:
                if handlers[handler]["class"] in _FILE_HANDLERS:
                    handlers[handler]["filename"] = _os.path.join(log_directory, handlers[handler]["filename"])

    except OSError as e:
        raise LogError(f"An error occurred while setting up the logging module - {e}")

    # Load the configuration and return the logger object
    _config.dictConfig(config)
    return _logging.getLogger()


class Log:
    """
    Static logging class which uses a Python's built-in logger object for the actual logging tasks.
    Uses the :class:`LogError` class to handle errors and let the calling function handle them.
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

    # Initialise the loggers
    _main_logger = _get_logger(_MAIN_CONFIG_FILE_PATH)
    _hardware_logger = _get_logger(_HARDWARE_CONFIG_FILE_PATH)

    @classmethod
    def reconfigure(cls, logger: Logger, config_file_path: str, *, log_directory: str = ""):
        """
        Helper function to reconfigure a logger

        :param logger: Name of the logger to reconfigure
        :param config_file_path: Path to the JSON configuration file
        :param log_directory:  Path to where the log files should be stored
        """
        if not isinstance(logger, Logger):
            raise LogError(f"Attempted to reconfigure an invalid logger {logger} - isn't of type \"Logger\"")

        # Update the logger with both new values (or use the empty strings as default to use the default paths)
        setattr(cls, logger.value, _get_logger(config_file_path, log_directory=log_directory))

    @classmethod
    def debug(cls, message: str, *args, **kwargs):
        """
        Standard debug logging.
        :param message: Message to log
        :param args: Args passed to the internal logger
        :param kwargs: Kwargs passed to the internal logger
        """
        cls._main_logger.debug(message, *args, **kwargs)

    @classmethod
    def info(cls, message: str, *args, **kwargs):
        """
        Standard info logging.
        :param message: Message to log
        :param args: Args passed to the internal logger
        :param kwargs: Kwargs passed to the internal logger
        """
        cls._main_logger.info(message, *args, **kwargs)

    @classmethod
    def warning(cls, message: str, *args, **kwargs):
        """
        Standard warning logging.
        :param message: Message to log
        :param args: Args passed to the internal logger
        :param kwargs: Kwargs passed to the internal logger
        """
        cls._main_logger.warning(message, *args, **kwargs)

    @classmethod
    def error(cls, message: str, *args, **kwargs):
        """
        Standard error logging.
        :param message: Message to log
        :param args: Args passed to the internal logger
        :param kwargs: Kwargs passed to the internal logger
        """
        cls._main_logger.error(message, *args, **kwargs)

    @classmethod
    def command_result(cls, command_result: _subprocess.CompletedProcess):
        """
        Method used to log return code as info, stdout as debug and stderr as error.
        :param command_result: Result from subprocess.run or similar
        """

        cls._main_logger.info("The command returned {}, logging stdout and stderr...".format(command_result.returncode))

        # Log stdout as info
        if command_result.stdout:
            cls._main_logger.debug(command_result.stdout.decode("ascii"))

        # Log stderr as error
        if command_result.stderr:
            cls._main_logger.error(command_result.stderr.decode("ascii"))
