from src.common import LOG_DIR, Log
import os

def main():
    """
    Main function for testing the logging system
    Gets the values from a dictionary which are a number of functions. These functions are tests
    These functions are then ran. 
    These functions can return AssertionError exceptions
    
    :return: No return
    """

    for test_func in get_tests(__name__).values():
        test_func()


def get_log_files():
    """
    Getter that returns a set of logging files found in the logging directory
    
    :return: any files with the .log extension found
    """


    files = set()
    for file in os.listdir(LOG_DIR):
        if file.endswith(".log"):
            files.add(os.path.join(LOG_DIR, file))
    return files

def test_create_logs():
    """
    Test that checks if 5 logging files are created. 1 for each level (Debug, Info, Warning, Error) and the 'verbose' file
    
    :return: Nothing if test passes, AssertionError exception if the test fails
    """

    Log.debug("Test debug message")
    Log.info("Test info message")
    Log.warning("Test warning message")
    Log.error("Test error message")

    # There should be 5 files created - each for the log level and a verbose for all levels combined
    assert(len(get_log_files()) == 5)


def test_level_filtering():
    """
    Test that checks each logging file has the correct length.
    The "verbose" logging file should be 4 lines since its composed of the 4 levels / the 4 other logging files
    The other logging files should be 1 line since all other messages are appended on the end
    
    :return: Nothing if test passes, AssertionError exception if the test fails
    """

    for file in get_log_files():
        with open(file) as f:
            if "verbose" in file:
                assert(len(f.readlines()) == 4)
            else:
                assert(len(f.readlines()) == 1)
