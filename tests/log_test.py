from src.common import COMMON_LOGGER_DIR, Log
import os

# Reconfigure the logger to use a separate folder (instead of the real logs)
#Log.reconfigure(os.path.join(COMMON_LOGGER_DIR, "config.json"))


def get_log_files() -> set:
    """
    Helper function used to retrieve a set of absolute paths to the log files
    
    :return: A set of paths
    """

    files = set()
    for file in os.listdir(LOG_DIR):
        if file.endswith(".log"):
            files.add(os.path.join(LOG_DIR, file))
    return files


def test_create_logs():
    """
    TODO: Documentation
    
    :return
    """

    Log.debug("Test debug message")
    Log.info("Test info message")
    Log.warning("Test warning message")
    Log.error("Test error message")

    # There should be 5 files created - each for the log level and a verbose file for all levels combined
    assert len(get_log_files()) == 5


def test_level_filtering():
    """
    TODO: Documentation
    
    :return
    """

    for file in get_log_files():
        with open(file) as f:
            if "verbose" in file:
                assert (len(f.readlines()) == 4)
            else:
                assert (len(f.readlines()) == 1)
