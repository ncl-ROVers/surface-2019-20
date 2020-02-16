"""
Streams screen
==============

Module storing an implementation of a streams display screen and all values associated with it.
"""
from ..common import Log
from .utils import Screen
from PySide2.QtCore import *
from PySide2.QtWidgets import *


# Declare FPS - 1 FPS is equivalent to the value being set to 1000.
STREAM_UPDATE_INTERVAL = 1000//20


class Streams(Screen):
    """
    Loading screen used to load all assets while displaying a visually-pleasing representation of the mentioned task.

    Functions
    ---------

    The following list shortly summarises each function:

        * __init__ - a constructor to create all QT objects and class-specific fields
        * _config - a method to place all items created in __init__
        * _set_style - default implementation of the inherited method
        * post_init - default implementation of the inherited method
        * on_switch - a method which start the clocks
        * on_exit - a method which stops the clocks
        * _update_main_camera - helper function to display main camera's frame
        * _update_top_camera - helper function to display top camera's frame
        * _update_bottom_camera - helper function to display bottom camera's frame
        * _update_micro_camera - helper function to display micro-ROV camera's frame

    Usage
    -----

    This screen can be switched to as many times as needed.
    """

    def __init__(self):
        """
        Standard constructor.
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
        self._top_camera_clock = QTimer()
        self._bottom_camera_clock = QTimer()
        self._micro_camera_clock = QTimer()

        self._config()
        self.setLayout(self._layout)

    def _config(self):
        """
        Standard configuration method.
        """
        super()._config()

        # Set and connect clock timeouts
        self._main_camera_clock.timeout.connect(self._update_main_camera)
        self._main_camera_clock.setInterval(STREAM_UPDATE_INTERVAL)

        self._top_camera_clock.timeout.connect(self._update_top_camera)
        self._top_camera_clock.setInterval(STREAM_UPDATE_INTERVAL)

        self._bottom_camera_clock.timeout.connect(self._update_bottom_camera)
        self._bottom_camera_clock.setInterval(STREAM_UPDATE_INTERVAL)

        self._micro_camera_clock.timeout.connect(self._update_micro_camera)
        self._micro_camera_clock.setInterval(STREAM_UPDATE_INTERVAL)

        # Each camera takes a different corner of the available space
        self._layout.addWidget(self._main_camera, 0, 0)
        self._layout.addWidget(self._top_camera, 0, 1)
        self._layout.addWidget(self._bottom_camera, 1, 0)
        self._layout.addWidget(self._micro_camera, 1, 1)

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
        Start frame displaying clocks.
        """
        super().on_switch()
        self._main_camera_clock.start()
        self._top_camera_clock.start()
        self._bottom_camera_clock.start()
        self._micro_camera_clock.start()

    def on_exit(self):
        """
        Stop frame displaying clocks.
        """
        self._main_camera_clock.stop()
        self._top_camera_clock.stop()
        self._bottom_camera_clock.stop()
        self._micro_camera_clock.stop()

    def _update_main_camera(self):
        """
        Update main camera's frame.
        """
        Log.debug("Updating main, forward-facing camera")
        frame = self.manager.references.main_camera.frame_qt
        frame = frame.scaled(min(self._main_camera.width(), frame.width()),
                             min(self._main_camera.height(), frame.height()),
                             aspectMode=Qt.KeepAspectRatio, mode=Qt.SmoothTransformation)
        self._main_camera.setPixmap(frame)

    def _update_top_camera(self):
        """
        Update top camera's frame.
        """
        Log.debug("Updating top-facing camera")
        frame = self.manager.references.top_camera.frame_qt
        frame = frame.scaled(min(self._top_camera.width(), frame.width()),
                             min(self._top_camera.height(), frame.height()),
                             aspectMode=Qt.KeepAspectRatio, mode=Qt.SmoothTransformation)
        self._top_camera.setPixmap(frame)

    def _update_bottom_camera(self):
        """
        Update bottom camera's frame.
        """
        Log.debug("Updating bottom-facing camera")
        frame = self.manager.references.bottom_camera.frame_qt
        frame = frame.scaled(min(self._bottom_camera.width(), frame.width()),
                             min(self._bottom_camera.height(), frame.height()),
                             aspectMode=Qt.KeepAspectRatio, mode=Qt.SmoothTransformation)
        self._bottom_camera.setPixmap(frame)

    def _update_micro_camera(self):
        """
        Update micro-ROV camera's frame.
        """
        Log.debug("Updating micro-ROV camera")
        frame = self.manager.references.micro_camera.frame_qt
        frame = frame.scaled(min(self._micro_camera.width(), frame.width()),
                             min(self._micro_camera.height(), frame.height()),
                             aspectMode=Qt.KeepAspectRatio, mode=Qt.SmoothTransformation)
        self._micro_camera.setPixmap(frame)
