"""
TODO: Document
"""

from ..common import LOG_DIR, SRC_LOG_DIR
import logging as _logging
import logging.config as _config
import json as _json
import subprocess as _subprocess
import os as _os

_DEFAULT_LOG_DIR = LOG_DIR
_DEFAULT_CONFIG_FILE_PATH = _os.path.join(SRC_LOG_DIR, "config.json")
_FILE_HANDLERS = {"logging.FileHandler", "src.common.statics._RestrictedFileHandler"}


class _LogConfig:
    """
    TODO: Document
    """

    @staticmethod
    def get_logger(config_file_path: str = "", log_directory: str = "") -> _logging.Logger:
        """
        TODO: Document
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
                for handler in (handlers):
                    if handlers[handler]["class"] in _FILE_HANDLERS:
                        handlers[handler]["filename"] = _os.path.join(log_directory, handlers[handler]["filename"])

        except OSError as e:
            raise Log.LogError(f"An error occurred while setting up the logging module - {e}")

        # Load the configuration and return the logger object
        _config.dictConfig(config)
        return _logging.getLogger()


class Log:
    """
    TODO: Document
    """

    # Initialise the logger
    _logger = _LogConfig.get_logger()

    class LogError(Exception):
        """
        TODO: Document
        """

        pass

    @classmethod
    def reconfigure(cls, *, config_file_path: str = "", log_directory: str = ""):
        """
        TODO: Document
        """

        # Update the logger with both new values (or use the empty strings as default to use the default paths)
        cls._logger = _LogConfig.get_logger(config_file_path, log_directory)

    @classmethod
    def debug(cls, message: str, *args, **kwargs):
        """
        TODO: Document
        """

        cls._logger.debug(message, *args, **kwargs)

    @classmethod
    def info(cls, message: str, *args, **kwargs):
        """
        TODO: Document
        """

        cls._logger.info(message, *args, **kwargs)

    @classmethod
    def warning(cls, message: str, *args, **kwargs):
        """
        TODO: Document
        """

        cls._logger.warning(message, *args, **kwargs)

    @classmethod
    def error(cls, message: str, *args, **kwargs):
        """
        TODO: Document
        """

        cls._logger.error(message, *args, **kwargs)

    @classmethod
    def command_result(cls, command_result: _subprocess.CompletedProcess):
        """
        TODO: Document
        """

        Log.debug("The command returned {}, logging stdout and stderr...".format(command_result.returncode))

        # Log stdout as info
        if command_result.stdout:
            cls._logger.info(command_result.stdout.decode("ascii"))

        # Log stderr as error
        if command_result.stderr:
            cls._logger.error(command_result.stderr.decode("ascii"))
