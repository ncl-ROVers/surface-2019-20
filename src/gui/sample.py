"""
TODO: Document
"""
from .utils import Screen
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

class SimpleItem(QGraphicsItem):

    def boundingRect(self):
        penWidth = 1.0
        return QRectF(-10 - penWidth / 2, -10 - penWidth / 2,
                      20 + penWidth, 20 + penWidth)

    def paint(self, painter, option, widget):
        painter.drawRoundedRect(-10, -10, 20, 20, 5, 5)

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
        scene.addText("Hello, world!")
        scene.addItem(SimpleItem())

        view = QGraphicsView(scene)
        self._layout = QHBoxLayout()
        self._layout.addWidget(view)
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
