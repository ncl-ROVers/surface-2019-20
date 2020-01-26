"""
TODO: Document
"""
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from .utils import Screen
from .. import common
import os


class Controller(Screen):
    """
    TODO: Document
    """

    def __init__(self):
        """
        Standard constructor.
        """
        super(Controller, self).__init__()

        # These values will be used to scale the images correctly, they are set in the `on_switch` method.
        self._width = 0
        self._height = 0

        self._label = QLabel()
        self._layout = QVBoxLayout()

        self._config()
        self.setLayout(self._layout)

    def _config(self):
        """
        Standard configuration method.

        Margins must be set to 0 or else the screen's width will be (image size + margin), and push the menu bar away.
        """
        super()._config()
        self._layout.addWidget(self._label, alignment=Qt.AlignCenter)
        self._layout.setMargin(0)
        self._label.setMargin(0)

    def _set_style(self):
        """
        Standard styling method.
        """
        super()._set_style()

        # Scale the model to match the size of the screen and set it as the label's pixel map
        controller = QPixmap(os.path.join(common.GUI_CONTROLLER_DIR, "controller.png"))
        controller = controller.scaled(min(self._width, controller.width()), min(self._height, controller.height()),
                                       aspectMode=Qt.KeepAspectRatio, mode=Qt.SmoothTransformation)
        self._label.setPixmap(controller)

    def post_init(self):
        """
        Default inherited.
        """
        super().post_init()

    def on_switch(self):
        """
        Save the width and height calculated on switch, to adjust the image size correctly.
        """
        self._width = self.width()
        self._height = self.height()
        super().on_switch()

    def on_exit(self):
        """
        Default inherited.
        """
        super().on_exit()
