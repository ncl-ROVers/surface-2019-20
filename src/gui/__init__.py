"""
Graphical User Interface
========================

Visual tools handling the interaction between the users of the application and the ROV's backend.

Interaction with this module should only happen via the :func:`start` function.

.. moduleauthor::
    Kacper Florianski <k.florianski@ncl.ac.uk>
"""

from PySide2.QtWidgets import QApplication as _QApplication
from .loading import Loading as _Loading
from .home import Home as _Home
from .utils import ScreenManager as _ScreenManager, Screen as _Screen
from ..common import Log


def start() -> int:
    """
    Start the graphical user interface.

    Creates an instance of :class:`PySide2.QtWidgets.QApplication` as well as the `manager` object to handle screen
    selections and rendering.

    :return: Return code of the application
    """
    app = _QApplication()

    # Create and configure the screen manager, load all assets and switch to the home screen
    manager = _ScreenManager(_Loading(), _Home())
    manager.post_init()
    manager.show()
    manager.screen.load()
    manager.screen = _Screen.Home

    # Start the application and later exit with its return code
    Log.info("Application started")
    rc = app.exec_()
    Log.info("Application stopped")
    return rc
