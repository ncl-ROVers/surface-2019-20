"""
TODO: Document
"""
from .utils import Screen
from PySide2.QtCore import *
from PySide2.QtWidgets import *


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

        # Declare clocks to update the frames with a constant rate
        self._main_camera_clock = QTimer()
        self._main_camera_clock.setInterval(50)
        self._top_camera_clock = QTimer()
        self._top_camera_clock.setInterval(50)
        self._bottom_camera_clock = QTimer()
        self._bottom_camera_clock.setInterval(50)
        self._micro_camera_clock = QTimer()
        self._micro_camera_clock.setInterval(50)

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

        # Update clock timeouts
        #self._main_camera_clock.timeout.connect(self._update_main_camera)


        # Each camera takes a different corner of the available space
        self._layout.addWidget(self._main_camera, 0, 0)
        self._layout.addWidget(self._top_camera, 0, 1)
        self._layout.addWidget(self._bottom_camera, 1, 0)
        self._layout.addWidget(self._micro_camera, 1, 1)

    def _update_main_camera(self):
        self._main_camera.setPixmap(self.manager.references.main_camera.frame_qt)

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
        self.manager.references.main_camera.frame_qt
        # self._main_camera_clock.start()
        # self._top_camera_clock.start()
        # self._bottom_camera_clock.start()
        # self._micro_camera_clock.start()

    def on_exit(self):
        """
        Stop frame fetching clocks.
        """
        # self._main_camera_clock.stop()
        # self._top_camera_clock.stop()
        # self._bottom_camera_clock.stop()
        # self._micro_camera_clock.stop()
