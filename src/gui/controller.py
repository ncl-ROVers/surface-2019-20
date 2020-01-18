"""
TODO: Document
"""
from .utils import Screen
from .. import common

from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

import os
import pyautogui

SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()


class QPixmap(QPixmap):
    def ScaledToScreen(self, percent):
        # Gets window screen size and returns pixmap after applying scaling factor in percentage
        _scaledwidth = SCREEN_WIDTH * percent
        _scaledheight = SCREEN_HEIGHT * percent
        return self.scaled(_scaledwidth, _scaledheight, aspectMode=Qt.KeepAspectRatio, mode=Qt.SmoothTransformation)


class Controller(Screen):
    """
    TODO: Document
    """

    def __init__(self):
        """
        Default inherited.
        """
        # Controller pixmap
        super(Controller, self).__init__()
        self._pixmap = QPixmap(os.path.join(common.GUI_LOADING_DIR, "controller.png"))
        # Enlarge controller pixmap to 85% of screen size
        self._pixmap = self._pixmap.ScaledToScreen(0.85)

        self._label = QLabel()
        self._label.setPixmap(self._pixmap)

        self._layout = QVBoxLayout()
        self._layout.addWidget(self._label, alignment=Qt.AlignCenter)
        self.setLayout(self._layout)

    def _config(self):
        """
        Default inherited.
        """
        super()._config()

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
        Display the menu bar as it should only be disabled in the loading screen.
        """
        super().on_switch()
        self.manager.bar.parent().setVisible(True)

    def on_exit(self):
        """
        Default inherited.
        """
        super().on_exit()
