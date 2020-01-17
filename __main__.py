"""
Main
====

Main execution module.

To run the code, call::
    python surface

where `python` is Python3.8.1 version and `surface` is relative or absolute path to the directory in which this file is.
"""
from src import gui


if __name__ == "__main__":

    # Fetch and exit with the return code of the application execution
    exit(gui.start())
