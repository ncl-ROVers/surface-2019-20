"""
TODO: Document
"""
from .utils import Screen
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *


class Streams(Screen):
    """
    TODO: Document
    """

    def __init__(self):
        """
        Default inherited.
        """
        super(Streams, self).__init__()

        # Each camera should take exactly half width and half height of available space (25% of the space)
        self._layout = QGridLayout()
        self._main_camera = QLabel()
        self._top_camera = QLabel()
        self._bottom_camera = QLabel()
        self._micro_camera = QLabel()

        self._config()
        self.setLayout(self._layout)

    def _config(self):
        """
        Default inherited.
        """
        super()._config()

        # Each camera should take max space available - to evenly distribute the space
        self._main_camera.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._top_camera.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._bottom_camera.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._micro_camera.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # TODO: FInished here
        # self._layout.add

    def _set_style(self):
        """
        Default inherited.
        """
        super()._set_style()

    def post_init(self):
        """
        Default inherited.
        """
        super().post_init()

    def on_switch(self):
        """
        Start frame fetching clocks.
        """
        super().on_switch()
        self.manager.references.main_camera.clock.start()
        self.manager.references.top_camera.clock.start()
        self.manager.references.bottom_camera.clock.start()
        self.manager.references.micro_camera.clock.start()

    def on_exit(self):
        """
        Stop frame fetching clocks.
        """
        self.manager.references.main_camera.clock.stop()
        self.manager.references.top_camera.clock.stop()
        self.manager.references.bottom_camera.clock.stop()
        self.manager.references.micro_camera.clock.stop()
