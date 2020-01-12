"""
Log-related tests.

The tests are first reconfiguring the loggers to use the local assets folder instead of the production environment.
"""
import pytest

from src.common import COMMON_LOGGER_DIR, TESTS_ASSETS_DIR, Log, Logger
import os


def get_log_files() -> set:
    """
    Helper function used to retrieve a set of absolute paths to the log files.
    
    :return: A set of paths
    """
    files = set()
    for file in os.listdir(TESTS_ASSETS_DIR):
        if file.endswith(".log"):
            files.add(os.path.join(TESTS_ASSETS_DIR, file))
    return files


def test_create_logs():
    """
    Test that log files are correctly created.

    After clearing the existing log files and logging some messages, there should be 5 files created - each for the log
    level and a verbose file for all levels combined
    """
    Log.debug("Test debug message")
    Log.info("Test info message")
    Log.warning("Test warning message")
    Log.error("Test error message")

    assert len(get_log_files()) == 5


def test_level_filtering():
    """
    Test that log levels are filtered into the correct files.

    Each file should have only the respective, single level logged, except for verbose which should have all of them.
    """
    for file in get_log_files():
        with open(file) as f:
            if "verbose" in file:
                assert (len(f.readlines()) == 4)
            else:
                assert (len(f.readlines()) == 1)


@pytest.fixture(scope="module", autouse=True)
def config():

    """
    Pytest fixture for config function - used to execute config before any test is ran
    scope parameter used to share fixture instance across full session
    autouse parameter ensures all tests in session use the fixture automatically
    """

    # Remove all log files from the assets folder.
    for log_file in get_log_files():
        os.remove(log_file)

    # Reconfigure the logger to use a separate folder (instead of the real logs)
    Log.reconfigure(Logger.MAIN, os.path.join(COMMON_LOGGER_DIR, "config_main.json"),
                    log_directory=TESTS_ASSETS_DIR)
