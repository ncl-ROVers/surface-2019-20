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
from src import *


if __name__ == "__main__":
    #gui.start()
    controller = control.Controller()
    manager = control.ControlManager()

    if not controller:
        common.Log.error("Failed to initialise the controller")
        exit(1)

    controller_pid = controller.start()
    manager_pid = manager.start()

    # TODO: Remove later
    import time
    while True:
        for k in common.CONTROL_DICT:
            print(k, common.dm.control[k], end=" | ")
            pass
        print()
        time.sleep(0.5)