"""
GUI Utils
=========

Standard utils module storing all values, classes and other objects which may change throughout the execution of the
program, or are modifying their contents. Includes common to the package functions.
"""

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from .statics import *
from ..common import Log
import typing
import abc


class Screen(QWidget, abc.ABC, metaclass=type("_", (type(abc.ABC), type(QWidget)), {})):
    """
    Semi-abstract class used as a base for any "screen" / "panel" currently displayed in the main window.

    Provides a static enumeration of all available screens as well as a collection of abstract and standard methods.

    Functions
    ---------

    The following list shortly summarises each function:

        * __init__ - a constructor to create all QT objects and class-specific fields
        * _background_pixmap - a getter to retrieve a default :class:`PySide2.QtGui.QPixmap` used in the background
        * manager - a getter to retrieve the associated (global) screen manager
        * _config - an abstract method to place all items created in __init__
        * _set_style - a semi-abstract method to set the style of current screen
        * post_init - a semi-abstract method called directly after the screen is created
        * on_switch - a semi-abstract method called whenever the screen manager switches the screen

    Usage
    -----

    You should always attempt to implement the abstract (and the semi-abstract) methods for more custom functionality.

    In order to simply use the default functionality, write::

        def inherited_abstract_method():
            super().inherited_abstract_method()

    where `inherited_abstract_method` is one of the abstract methods declared in this class.

    .. note::

        Remember to add an enumeration constant when creating a new screen, and instantiate it in the `__init__` file!
    """

    Loading = 0
    Home = 1

    def __init__(self):
        """
        Standard constructor.

        Additionally sets the name attribute which is used by the screen manager.
        """
        super(Screen, self).__init__()

        # Initialise the GUI window name
        self.name = self.__class__.__name__

    @property
    def _background_pixmap(self) -> QPixmap:
        """
        Getter to create and return a default background "canvas".

        :return: QPixmap styled to represent the default background
        """
        r, g, b, a = Colour.MAJOR.value
        brush = QBrush(QColor(r, g, b, a))

        # Create an empty canvas and fill it with the colour
        canvas = QPixmap(SCREEN_WIDTH, SCREEN_HEIGHT)
        painter = QPainter()
        painter.begin(canvas)
        painter.setBrush(brush)
        painter.drawRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        painter.end()

        return canvas

    @property
    def manager(self) -> typing.Union[QMainWindow, None]:
        """
        Getter to find the screen manager and return it.

        :return: :class:`ScreenManager` or None if couldn't be found
        """

        for widget in QApplication.instance().topLevelWidgets():
            if "ScreenManager" in repr(widget):
                return widget
        return None

    @abc.abstractmethod
    def _config(self):
        """
        An abstract method to configure the initial state of the objects created in :func:`__init__`.
        """
        pass

    @abc.abstractmethod
    def _set_style(self):
        """
        A semi-abstract method to set style of the main window.

        Sets the background colour by default.
        """
        pal = self.manager.palette()
        pal.setBrush(QPalette.Window, QBrush(self._background_pixmap))
        self.manager.setPalette(pal)

    @abc.abstractmethod
    def post_init(self):
        """
        A semi-abstract method executed directly after the screen is created.
        """
        Log.debug("Successfully initialised \"{}\" screen".format(self.name))

    @abc.abstractmethod
    def on_switch(self):
        """
        A semi-abstract method executed on screen switching.

        :return:
        """
        Log.debug("Switched screen to {}".format(self.name))
        self._set_style()


class ScreenManager(QMainWindow):
    """
    Manager class used as the GUI's main window.

    Handles screen switching and display.

    Functions
    ---------

    The following list shortly summarises each function:

        * __init__ - a constructor to create and configure all QT objects and class-specific fields
        * screen - a property to switch between the screens
        * screens - a getter to retrieve all screens stored
        * post_init - a method which calls `post_init` of each screen

    Usage
    -----

    The manager should be used to switch in between screens correctly.

    In order to switch a screen from within another screen, write::

        self.manager.screen = Screen.screen_to_switch_to

    where `screen_to_switch_to` is one of the enums within the :class:`Screen` class.
    """

    def __init__(self, *args):
        """
        Standard constructor.

        Creates a stacked widget to store screens, puts it in a box layout and configures a `container` widget to use
        that layout. The `container` is then used as a central widget for the main window.

        :param args: A collection of :class:`Screen` instances to manage
        """
        super(ScreenManager, self).__init__()

        self._flag_setting(indicator=WINDOW_INDICATOR)

        # Declare the screen structure - a box layout with a stacked widget holding the screens
        self._base = QHBoxLayout()
        self._screens_stacked = QStackedWidget()
        self._screens = dict()

        # Add all screens
        for screen in args:
            self._screens_stacked.addWidget(screen)
            self._screens[screen.name] = screen
        self._base.addWidget(self._screens_stacked)

        # Finally set the layout
        self._container = QWidget()
        self._container.setLayout(self._base)
        self.setCentralWidget(self._container)
        self.screen = Screen.Loading

    @property
    def screen(self) -> Screen:
        """
        Getter to retrieve the current screen

        :return: Current :class:`Screen`
        """
        return self._screens_stacked.currentWidget()

    @screen.setter
    def screen(self, index: int):
        """
        Setter to switch to a screen at a given index.

        Additionally sets the window name and calls the screen's `on_switch` method.

        :param index: :class:`Screen` enumeration's value
        """
        self._screens_stacked.setCurrentIndex(index)
        self.setWindowTitle(self._screens_stacked.currentWidget().name)
        self._screens_stacked.currentWidget().on_switch()

    @property
    def screens(self) -> dict:
        """
        Getter to retrieve a mapping of screen name (str) to a :class:`Screen` object.
        """
        return self._screens

    def post_init(self):
        """
        Helper function to call `post_init` methods of all screens in a single call.
        """
        for scr in self._screens.values():
            scr.post_init()

    def _flag_setting(self, indicator='borders'):
        """
        Set display mode for the window

        :param indicator:
        'borders':      Setting the window with borders
        'full_screen':  Set full screen
        'border_less':  Setting the window without borders
        """
        self.setGeometry(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        if indicator.__eq__('borders'):
            pass
        elif indicator.__eq__('full_screen'):
            self.showFullScreen()
        elif indicator.__eq__('border_less'):
            self.setWindowFlags(Qt.FramelessWindowHint)

    def keyPressEvent(self, event: QKeyEvent):
        """
        This is the overridden of  QMainWindow.keyPressEvent

        Press 'ESC' to close the window
        """
        if event.key().__eq__(Qt.Key_Escape):
            exit()
            event.accept()
