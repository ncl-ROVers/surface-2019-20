"""
Streams screen
==============

Module storing an implementation of a streams display screen and all values associated with it.
"""
from .utils import Screen, new_camera_update_func
from PySide2.QtWidgets import *


class Streams(Screen):
    """
    Streams screen used to display all 4 video streams.

    Functions
    ---------

    The following list shortly summarises each function:

        * __init__ - a constructor to create all QT objects and class-specific fields
        * _config - a method to place all items created in __init__
        * _set_style - default implementation of the inherited method
        * post_init - default implementation of the inherited method
        * on_switch - a method which connects the slots on switch
        * on_exit - a method which disconnects the slots on exit
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

        # Create the video stream update functions
        self._update_main_camera = new_camera_update_func(self._main_camera, "Main in Streams")
        self._update_top_camera = new_camera_update_func(self._top_camera, "Top-facing in Streams")
        self._update_bottom_camera = new_camera_update_func(self._bottom_camera, "Bottom-facing in Streams")
        self._update_micro_camera = new_camera_update_func(self._micro_camera, "Micro in Streams")

        self._config()
        self.setLayout(self._layout)

    def _config(self):
        """
        Standard configuration method.
        """
        super()._config()

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
        Connect frame displaying slots.
        """
        super().on_switch()
        self.manager.references.main_camera.frame_received.connect(self._update_main_camera)
        self.manager.references.top_camera.frame_received.connect(self._update_top_camera)
        self.manager.references.bottom_camera.frame_received.connect(self._update_bottom_camera)
        self.manager.references.micro_camera.frame_received.connect(self._update_micro_camera)

    def on_exit(self):
        """
        Disconnect frame displaying slots.
        """
        self.manager.references.main_camera.frame_received.disconnect(self._update_main_camera)
        self.manager.references.top_camera.frame_received.disconnect(self._update_top_camera)
        self.manager.references.bottom_camera.frame_received.disconnect(self._update_bottom_camera)
        self.manager.references.micro_camera.frame_received.disconnect(self._update_micro_camera)
