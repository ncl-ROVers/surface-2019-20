"""
TODO: Document
"""
from .utils import Screen
from .. import common

from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

import os

class Description(QWidget):
    def __init__(self, input_names):
        """
        Default inherited.
        """
        super(Description, self).__init__()
        self._layout = QVBoxLayout()
        self._label = QLabel()
        self._layout.addWidget(self._label)
        text = '\n'.join(input_names)
        self._label.setText(text)
        self.setLayout(self._layout)

class Sample(Screen):
    """
    TODO: Document
    """

    def __init__(self):
        """
        Default inherited.
        """
        super(Sample, self).__init__()
        scene = QGraphicsScene()
        self.Group1 = scene.addWidget(Description(['what', 'hi']))
        self.Group2 = scene.addWidget(Description(['what', 'hi']))
        self.Group3 = scene.addWidget(Description(['what', 'hi']))
        self.Group4 = scene.addWidget(Description(['what', 'hi']))
        self.Group5 = scene.addWidget(Description(['what', 'hi']))
        self.Group6 = scene.addWidget(Description(['what', 'hi']))

        # For the controller
        self.Pixmap = QPixmap(os.path.join(common.GUI_LOADING_DIR, "controller.png")) # Temporary directory for now
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setPixmap(self.Pixmap)
        self.Group7 = scene.addWidget(self.label)

        layout = QGraphicsGridLayout()
        layout.addItem(self.Group1, 0, 0)
        layout.addItem(self.Group2, 1, 0)
        layout.addItem(self.Group3, 2, 0)
        layout.addItem(self.Group4, 0, 2)
        layout.addItem(self.Group5, 1, 2)
        layout.addItem(self.Group6, 2, 2)
        layout.addItem(self.Group7, 0, 1, 3, 1) # Controller image

        form = QGraphicsWidget()
        form.setLayout(layout)
        scene.addItem(form)

        button = QPushButton("Click me")
        button.clicked.connect(self.say_hello)

        view = QGraphicsView(scene)
        self._layout = QHBoxLayout()
        self._layout.addWidget(view)
        self._layout.addWidget(button)

        self.setLayout(self._layout)
        view.setScene(scene)

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
        self.label.setStyleSheet("QLabel {background-color: red;}")

    def post_init(self):
        """
        Default inherited.
        """
        super().post_init()
        self.Group1.pos()

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
