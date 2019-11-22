"""
Main
====

Main execution module.

To run the code, call::
    python surface

where `python` is Python3.8 version and `surface` is relative or absolute path to the directory in which this file is.

.. warning::

    Currently you can only run the code with Python3.7, because PySide2 has not yet been released for 3.8.

    To run the code, change::

        `for handler in (handlers := config["handlers"]):`
            #(...)

    to::

        handler = config["handlers"]
        for handler in handlers:
            #(...)
"""

from src import gui


if __name__ == "__main__":
    gui.start()
