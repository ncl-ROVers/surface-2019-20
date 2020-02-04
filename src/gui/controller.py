"""
Controller screen
==============

Module storing an implementation of a controller layout screen that uses QPixmap.

Although QPixmap supports many ccmmon image formats, this implementation currently only supports PNG image
format due to a need to implement filename processing. The QPixmap will be displayed as long as it is located within
assets/gui_controller and is named controller.png 
"""
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from .utils import Screen
from .. import common
import os


class Controller(Screen):
    """
    Screen used to display sample image of the controller. QPixmap that is contained within a QLabel is used to
    display the controller asset located in GUI_CONTROLLER_DIR that is specified within utils.py.

    Functions
    ---------
    The following list shortly summarises each function:

        * __init__ - a constructor to create all QT objects and class-specific fields
        * _config - a method to place all items created in __init__ as well as set the margins to ensure consistency.
        * _set_style - a method to set the style of QPixmap
        * post_init - default implementation of the inherited method
        * on_switch - a method to retrieve the information about screen size
        * on_exit - default implementation of the inherited method
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

        If width and height of the controller pixmap exceeds the screen length, then pixmap will be scaled to the
        size of the window calculated during on_switch. Otherwise, the original size of the controller is used.

        Qt.SmoothTransformation option needs to be passed to the QPixmap.scaled method to ensure that image is not
        pixelated.
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
