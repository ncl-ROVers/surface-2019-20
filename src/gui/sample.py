"""
TODO: Document
"""
from .utils import Screen
from .. import common

from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

import os


class Sample(Screen):
    """
    TODO: Document
    """

    def __init__(self):
        """
        Default inherited.
        """
        # Background image
        super(Sample, self).__init__()
        self._Pixmap = QPixmap(os.path.join(common.GUI_LOADING_DIR, "controller.png")) # Temporary directory for now
        self._label = QLabel()
        self._label.setPixmap(self._Pixmap)

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
