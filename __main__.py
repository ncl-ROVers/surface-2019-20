"""
Main
====

Main execution module.

To run the code, call::
    python surface

where `python` is Python3.8 version and `surface` is relative or absolute path to the directory in which this file is.

.. warning::

    Currently you can only run the code with Python3.7, because PySide2 has not yet been released for 3.8. Disable all
    Python 3.8 related code before running this module with Python3.7.
"""
from src import *
import os
import signal


def _kill_processes(*args):
    """
    Helper function used to kill all child processes spawned by the application.

    :param args: List of pid-s
    """
    for pid in args:
        os.kill(pid, signal.SIGTERM)


if __name__ == "__main__":
    # controller = control.Controller()
    # manager = control.ControlManager()
    #
    # if not controller:
    #     common.Log.error("Failed to initialise the controller")
    #     exit(1)
    #
    # controller_pid = controller.start()
    # manager_pid = manager.start()
    #
    # # Fetch and remember the return code of the application execution
    # rc = gui.start()
    #
    # # Kill all child processes and exit the application
    # _kill_processes(controller_pid, manager_pid)
    # exit(rc)
    import socket
    import time
    s = socket.create_server(("localhost", 50000))
    s.listen(1)
    con = comms.Connection()
    print(con.status)
    con.connect()
    time.sleep(1)
    print(con.status)
    con.reconnect()
    time.sleep(1)
    print(con.status)
    con.disconnect()
    time.sleep(1)
    print(con.status)
