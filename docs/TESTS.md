# Creating tests for Python using Pytest

## Using Pytest

-Test files and test functions must contain:
  ```test_*``` or ```_*test```
so that Pytest can automatically detect the tests

-You can then run pytest from PyCharm IDE using: 

**Run 'pytest ...' on a test method, file, or directory**

and the results will be displayed in the 'Run' terminal

## Example Tests

Here are some examples of test methods (test_create_logs() & test_level_filtering()) that use assert:
```
from src.common import LOG_DIR, Log
import os


def get_log_files():
    """
    TODO: Documentation
    
    :return
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

    # There should be 5 files created - each for the log level and a verbose for all levels combined
    assert (len(get_log_files()) == 5)


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