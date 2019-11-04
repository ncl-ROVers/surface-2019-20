from PySide2.QtWidgets import QApplication as _QApplication
from .loading import Loading as _Loading
from .home import Home as _Home
from .sample import Sample as _Sample
from .utils import ScreenManager as _ScreenManager, Screen as _Screen


def start():
    """
    TODO: Document

    :return:
    """

    app = _QApplication()
    manager = _ScreenManager(_Loading(), _Sample())
    manager.post_init()
    manager.show()
    manager.screen.load()
    manager.screen = _Screen.Sample
    app.exec_()
