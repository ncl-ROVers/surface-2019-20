"""
Log-related tests.

The tests are first reconfiguring the loggers to use the local assets folder instead of the production environment.
"""
import pytest
import os
from tests.utils import TESTS_ASSETS_LOG_DIR, get_log_files
from src.common import COMMON_LOGGER_DIR, Log, Logger


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

    assert len(get_log_files(TESTS_ASSETS_LOG_DIR)) == 5


def test_level_filtering():
    """
    Test that log levels are filtered into the correct files.

    Each file should have only the respective, single level logged, except for verbose which should have all of them.
    """
    for file in get_log_files(TESTS_ASSETS_LOG_DIR):
        with open(file) as f:
            if "verbose" in file:
                assert (len(f.readlines()) == 4)
            else:
                assert (len(f.readlines()) == 1)


@pytest.fixture(scope="module", autouse=True)
def config():
    """
    PyTest fixture for the configuration function - used to execute config before any test is ran.

    `scope` parameter is used to share fixture instance across the module session, whereas `autouse` ensures all tests
    in session use the fixture automatically.
    """

    # Remove all log files from the assets folder.
    for log_file in get_log_files(TESTS_ASSETS_LOG_DIR):
        os.remove(log_file)

    # Reconfigure the logger to use a separate folder (instead of the real logs)
    Log.reconfigure(Logger.MAIN, os.path.join(COMMON_LOGGER_DIR, "config_main.json"),
                    log_directory=TESTS_ASSETS_LOG_DIR)
