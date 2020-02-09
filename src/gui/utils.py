"""
GUI Utils
=========

Standard utils module storing common to the package classes, functions, constants, and other objects.
"""

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from .. import comms, control
from ..common import Log
import pyautogui
import typing
import abc
import enum

SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
SLIDING_MENU_WIDTH = SCREEN_WIDTH // 8
MENU_BAR_HEIGHT = SCREEN_HEIGHT // 12

# Set the interval to check the connection status and reconnect on errors
CONNECTION_CLOCK_INTERVAL = 1000


def check_connection():
    """
    Function used to check the connection and reconnect if disconnected.
    """
    if _References.connection.status == comms.ConnectionStatus.DISCONNECTED:
        _References.connection.connect()
    elif _References.connection.status == comms.ConnectionStatus.CONNECTED:
        if not _References.connection.connected:
            _References.connection.reconnect()


def get_manager() -> typing.Union[QMainWindow, None]:
    """
    Getter to find the screen manager and return it.
    :return: :class:`ScreenManager` or None if couldn't be found
    """
    Log.debug("Retrieving screen manager")
    for widget in QApplication.instance().topLevelWidgets():
        if "ScreenManager" in repr(widget):
            return widget
    return None


class _References:
    """
    Helper class used to store the references to objects loaded within the loading screen.

    Each reference can be either None or of the type hinted.
    """
    controller: control.Controller = None
    control_manager: control.ControlManager = None
    connection: comms.Connection = None
    connection_clock: QTimer = None


class Colour(enum.Enum):
    """
    Colour enumeration storing different colour values for the GUI style.

    Each colour is in the RGBA format.
    """

    MAJOR = 34, 51, 54, 255


class _SlidingMenu(QListWidget):
    """
    Sliding menu widget used to navigate between screens.

    Functions
    ---------

    The following list shortly summarises each function:

        * __init__ - a constructor to create the widget and add all buttons
        * toggled - getter determining if the menu is currently shown
        * _show - show the menu (slide in)
        * _hide - hide the menu (slide out)
        * toggle - show/hide the menu (depending on current state)

    Usage
    -----

    You can access the menu through the manager, and display or hide it::

        get_manager().menu.toggle()
    """

    class _MenuButton(QPushButton):
        """
        Button class representing a button within the sliding menu.

        Styles it properly and adds custom functionality.

        TODO: Ideally we'd want this to inherit from QListWidgetItem
        """

        def __init__(self, name: str):
            """
            Standard constructor.

            Connects the click event to switching screens.

            :param name: Name of the screen (displayed as the button)
            """
            super(_SlidingMenu._MenuButton, self).__init__(name)
            self._name = name
            self.clicked.connect(self._on_click)

        def _on_click(self):
            """
            Function executed when a sliding menu button is pressed.
            """
            Log.debug("Pressed sliding menu button - {}".format(self._name))
            get_manager().screen = getattr(Screen, self._name)

    def __init__(self, parent, screen_names: list):
        """
        Standard constructor.

        Creates the buttons to display within the menu and setups the menu to display correctly.

        :param parent: Parent passed to QWidget's init
        :param screen_names: Screen names to display in the sliding menu
        """
        super().__init__(parent)

        # Set animation properties
        self._toggle = QPropertyAnimation(self, QByteArray(b"width"))
        self._toggle.setDuration(100)
        self._toggle.setStartValue(0)
        self._toggle.setEndValue(SLIDING_MENU_WIDTH)
        self._toggle.valueChanged.connect(self.setFixedWidth)

        # Remember if the menu has been shown
        self._toggled = False

        # Set the widget's style and move it to the correct place
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedSize(0, SCREEN_HEIGHT)
        self.setContentsMargins(0, 0, 0, 0)
        self.move(0, 0)

        # Create the buttons dynamically for each screen, and add them to the view
        for name in screen_names:
            if getattr(Screen, name) != Screen.Loading:
                _item = QListWidgetItem(name)
                self.addItem(_item)
                self.setItemWidget(_item, self._MenuButton(name))

    @property
    def toggled(self) -> bool:
        """
        Getter to retrieve boolean determining if the menu is currently displayed.
        """
        return self._toggled

    def _show(self):
        Log.debug("Showing sliding menu")
        self._toggle.setDirection(QAbstractAnimation.Forward)
        self._toggle.start()
        self.show()
        self._toggled = True

    def _hide(self):
        Log.debug("Hiding sliding menu")
        self._toggle.setDirection(QAbstractAnimation.Backward)
        self._toggle.start()
        self._toggled = False

    def toggle(self):
        """
        Function used to show/hide the menu based on its current state (opposite action)
        """
        if self._toggled:
            self._hide()
        else:
            self._show()


class _MenuBar(QWidget):
    """
    Menu bar layout containing various widgets which will be visible in all screens (apart from the loading screen).

    Functions
    ---------

    The following list shortly summarises each function:

        * __init__ - a constructor to create the widget and add them to the layout

    Elements
    --------

    The following elements are provided:

        * Menu button - a button used to show/hide the sliding menu
    """

    def __init__(self):
        """
        Standard constructor.

        Creates the widgets to display within the menu bar.
        """
        super(_MenuBar, self).__init__()

        # Create the sliding menu button
        self._menu_button = QPushButton("Show/hide menu")
        self._menu_button.clicked.connect(lambda _: get_manager().menu.toggle())

        # Create the exit button
        self._exit_button = QPushButton("Exit application")
        self._exit_button.clicked.connect(lambda _: QApplication.closeAllWindows())

        # Add all widgets and set the layout
        self._layout = QHBoxLayout()
        self._layout.addWidget(self._menu_button)
        self._layout.addWidget(self._exit_button)
        self.setFixedHeight(MENU_BAR_HEIGHT)
        self.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)


class _LineBreak(QFrame):
    """
    Line break widget to separate the menu bar and the screen widget.
    """

    def __init__(self):
        """
        Standard constructor.
        """
        super(_LineBreak, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)


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
        * on_exit - a semi-abstract method called whenever the screen manager switches to a different screen

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
    Controller = 2

    def __init__(self):
        """
        Standard constructor.

        Additionally sets the name attribute which is used by the screen manager.
        """
        super(Screen, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)

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
        return get_manager()

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
        """
        Log.debug("Switched screen to {}".format(self.name))
        self._set_style()

    @abc.abstractmethod
    def on_exit(self):
        """
        A semi-abstract method executed on exiting current screen.
        """
        Log.debug("Switched out of {}".format(self.name))


class ScreenManager(QMainWindow):
    """
    Manager class used as the GUI's main window.

    Handles screen switching and display.

    Functions
    ---------

    The following list shortly summarises each function:

        * __init__ - a constructor to create and configure all QT objects and class-specific fields
        * references - a getter to retrieve the references loaded in the loading screen
        * screen - a property to switch between the screens
        * screens - a getter to retrieve all screens stored
        * menu - a getter to retrieve the sliding menu
        * bar - a getter to retrieve the menu bar
        * line_break - a getter to retrieve the line break
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

        # Declare access to the references - objects loaded by the load function will be stored there
        self._references = _References

        # Prepare the main screen as a vertical box
        self._base_widget = QWidget()
        self.setCentralWidget(self._base_widget)
        self._base_layout = QVBoxLayout(self._base_widget)
        self.setFixedSize(SCREEN_WIDTH, SCREEN_HEIGHT)

        # Create main components - a menu bar and a screen holder widget, separated by a line break
        self._menu_bar = _MenuBar()
        self._menu_bar.setVisible(False)
        self._line_break = _LineBreak()
        self._line_break.setVisible(False)
        self._screens_stacked = QStackedWidget()

        # Construct the layout
        self._base_layout.setSpacing(0)
        self._base_layout.addWidget(self._menu_bar)
        self._base_layout.addWidget(self._line_break)
        self._base_layout.addWidget(self._screens_stacked)

        # Add all screens and create an associated sliding window
        self._screens = dict()
        for screen in args:
            self._screens_stacked.addWidget(screen)
            self._screens[screen.name] = screen
        self._sliding_menu = _SlidingMenu(self, list(self._screens.keys()))

        # Finally load the layout
        self.showFullScreen()
        self.setLayout(self._base_layout)
        self.screen = Screen.Loading

    @property
    def references(self) -> _References:
        """
        Getter to retrieve the references to items

        :return: Instance of the references class
        """
        return self._references

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
        # Ignore attempts to switch to current screen (apart from loading screen)
        if self._screens_stacked.currentIndex() == index and index != 0:
            Log.debug("Attempted to switch to current screen")
            return

        # Ignore attempts to switch to the loading screen (except for the initial switch)
        if self._screens_stacked.currentIndex() != 0 and index == 0:
            Log.error("Attempted to switch to the loading screen")
            return

        # Switch the screen by setting the index and calling associated screen functions
        self._screens_stacked.currentWidget().on_exit()
        self._screens_stacked.setCurrentIndex(index)
        self.setWindowTitle(self._screens_stacked.currentWidget().name)
        self._screens_stacked.currentWidget().on_switch()

    @property
    def screens(self) -> dict:
        """
        Getter to retrieve a mapping of screen name (str) to a :class:`Screen` object.
        """
        return self._screens

    @property
    def menu(self) -> _SlidingMenu:
        """
        Getter to retrieve the sliding menu.
        """
        return self._sliding_menu

    @property
    def bar(self) -> _MenuBar:
        """
        Getter to retrieve the menu bar.
        """
        return self._menu_bar

    @property
    def line_break(self):
        """
        Getter to retrieve the line break.
        """
        return self._line_break

    def post_init(self):
        """
        Helper function to call `post_init` methods of all screens in a single call.
        """
        for scr in self._screens.values():
            scr.post_init()
