"""
TODO: Document
"""
from ..common import Log
from .utils import Screen
from PySide2.QtCore import *
from PySide2.QtWidgets import *


STREAM_UPDATE_INTERVAL = 50


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
        self._top_camera_clock = QTimer()
        self._bottom_camera_clock = QTimer()
        self._micro_camera_clock = QTimer()

        self._config()
        self.setLayout(self._layout)

    def _config(self):
        """
        Default inherited.
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

    def _update_main_camera(self):
        """
        TODO: Document
        :return:
        """
        Log.debug("Updating main, forward-facing camera")
        frame = self.manager.references.main_camera.frame_qt
        frame = frame.scaled(min(self._main_camera.width(), frame.width()),
                             min(self._main_camera.height(), frame.height()),
                             aspectMode=Qt.KeepAspectRatio, mode=Qt.SmoothTransformation)
        self._main_camera.setPixmap(frame)

    def _update_top_camera(self):
        """
        TODO: Document
        :return:
        """
        Log.debug("Updating top-facing camera")
        frame = self.manager.references.top_camera.frame_qt
        frame = frame.scaled(min(self._top_camera.width(), frame.width()),
                             min(self._top_camera.height(), frame.height()),
                             aspectMode=Qt.KeepAspectRatio, mode=Qt.SmoothTransformation)
        self._top_camera.setPixmap(frame)

    def _update_bottom_camera(self):
        """
        TODO: Document
        :return:
        """
        Log.debug("Updating bottom-facing camera")
        frame = self.manager.references.bottom_camera.frame_qt
        frame = frame.scaled(min(self._bottom_camera.width(), frame.width()),
                             min(self._bottom_camera.height(), frame.height()),
                             aspectMode=Qt.KeepAspectRatio, mode=Qt.SmoothTransformation)
        self._bottom_camera.setPixmap(frame)

    def _update_micro_camera(self):
        """
        TODO: Document
        :return:
        """
        Log.debug("Updating micro-ROV camera")
        frame = self.manager.references.micro_camera.frame_qt
        frame = frame.scaled(min(self._micro_camera.width(), frame.width()),
                             min(self._micro_camera.height(), frame.height()),
                             aspectMode=Qt.KeepAspectRatio, mode=Qt.SmoothTransformation)
        self._micro_camera.setPixmap(frame)

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
        self._main_camera_clock.start()
        self._top_camera_clock.start()
        self._bottom_camera_clock.start()
        self._micro_camera_clock.start()

    def on_exit(self):
        """
        Stop frame fetching clocks.
        """
        self._main_camera_clock.stop()
        self._top_camera_clock.stop()
        self._bottom_camera_clock.stop()
        self._micro_camera_clock.stop()
