"""
Loading screen
==============

Module storing an implementation of a loading screen and all values associated with it.
"""

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from .statics import *
from .utils import Screen
from .. import common
import os

# Declare the progress bar's range
_MAX_LOADING = 100
_MIN_LOADING = 0


class Loading(Screen):
    """
    Loading screen used to load all assets while displaying a visually-pleasing representation of the mentioned task.

    Functions
    ---------

    The following list shortly summarises each function:

        * __init__ - a constructor to create all QT objects and class-specific fields
        * _config - a method to place all items created in __init__
        * _set_style - a method to set the style of the loading screen - this screen uses custom assets
        * post_init - default implementation of the inherited method
        * on_switch - default implementation of the inherited method
        * progress - a property used to handle current progress bar's progress value
        * load - a function used to load all assets and initialise any objects needed later

    Usage
    -----

    This screen should only be switched to once, and its func:`load` method called.
    """

    def __init__(self):
        """
        Standard constructor.
        """
        super(Loading, self).__init__()

        self._progress = 0

        self._layout = QVBoxLayout()
        self._bar = QProgressBar()
        self._label = QLabel()

        self._config()
        self.setLayout(self._layout)

    def _config(self):
        """
        Standard configuration method.
        """
        self._bar.setRange(_MIN_LOADING, _MAX_LOADING)

        self._label.setText("Loading ...")
        self._label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self._layout.addWidget(self._label)
        self._layout.addWidget(self._bar)
        self._layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

    def _set_style(self):
        """
        Standard styling method.
        """
        # Fetch the net image and scale it to fit the window if it's too big
        net = QPixmap(os.path.join(common.GUI_LOADING, "net.png"))
        net = net.scaled(min(SCREEN_WIDTH, net.width()), min(SCREEN_HEIGHT, net.height()))

        # Paint the background and render the net in the middle
        canvas = self._background_pixmap
        painter = QPainter()
        painter.begin(canvas)
        painter.drawPixmap((SCREEN_WIDTH - net.width()) // 2, (SCREEN_HEIGHT - net.height()) // 2, net)
        painter.end()

        # Update the manager's palette to display the changes
        pal = self.manager.palette()
        pal.setBrush(QPalette.Window, QBrush(canvas))
        self.manager.setPalette(pal)

    def post_init(self):
        """
        Default inherited.
        """
        super().post_init()

    def on_switch(self):
        """
        Default inherited.
        """
        super().on_switch()

    @property
    def progress(self) -> int:
        """
        Getter to the current loading progress.

        :return: An integer between min and max progress
        """
        return self._progress

    @progress.setter
    def progress(self, value: int):
        """
        Setter to update the current loading progress.

        :param value: New progress to set, must be between min and max constants
        :raises: ValueError
        """

        if not _MIN_LOADING <= self._progress <= _MAX_LOADING:
            raise ValueError(f"Progress must be between {_MIN_LOADING} and {_MAX_LOADING}")
        else:
            self._progress = value
            self._bar.setValue(value)

    def load(self):
        """
        TODO: Currently a sample to be removed later. This function should load all assets and initialise all objects.
          Storing the objects is undecided as of now, probably put them into the manager because every screen can access
          the manager. Perhaps create a DataManager instance within the ScreenManager?
        """
        from time import sleep
        for x in range(101):
            QApplication.instance().processEvents()
            self.progress = x
            sleep(0.01)
