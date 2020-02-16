"""
Graphical User Interface
========================

Visual tools handling the interaction between the users of the application and the ROV's backend.

Interaction with this module should only happen via the :func:`start` function.

.. moduleauthor::
    Kacper Florianski <k.florianski@ncl.ac.uk>
    Adanna Obibuaku <A.Obibuaku@newcastle.ac.uk>
    Zhanqiu Wang <Z.Wang111@newcastle.ac.uk>
    Riley Heeley <m.h.heeley1@newcastle.ac.uk>
"""
import os
import signal
from PySide2.QtWidgets import QApplication as _QApplication
from .loading import Loading as _Loading
from .home import Home as _Home
from .controller import Controller as _Controller
from .streams import Streams as _Streams
from .utils import ScreenManager as _ScreenManager, Screen as _Screen
from ..common import Log


def _kill_processes(*args):
    """
    Helper function used to kill all child processes spawned by the application.

    :param args: List of pid-s
    """
    for pid in args:
        os.kill(pid, signal.SIGTERM)


def start() -> int:
    """
    Start the graphical user interface.

    Creates an instance of :class:`PySide2.QtWidgets.QApplication` as well as the `manager` object to handle screen
    selections and rendering.

    :return: Return code of the application
    """
    app = _QApplication()

    # Declare a list of processes to terminate - each PID added to it will later be sent SIGTERM signal
    processes_to_terminate = list()

    # Create and configure the screen manager, load all assets and switch to the home screen
    manager = _ScreenManager(_Loading(), _Home(), _Streams(), _Controller())
    manager.post_init()
    manager.show()
    manager.screen.load()

    # Start the controller readings if it's connected
    if manager.references.controller:
        controller_pid = manager.references.controller.start()
        processes_to_terminate.append(controller_pid)

    # Start the control manager to update the transmission shared memory
    control_manager_pid = manager.references.control_manager.start()
    processes_to_terminate.append(control_manager_pid)

    # Once loaded and started all components, switch to the Home screen
    manager.screen = _Screen.Home

    # Start the application and later exit with its return code
    Log.info("Application started")
    rc = app.exec_()
    Log.info("Application stopped")

    # Cleanup the sockets and terminate the connection process
    manager.references.connection.disconnect()

    # Kill all child processes and exit the application
    _kill_processes(*processes_to_terminate)
    return rc
