from PySide2.QtWidgets import *
from PySide2.QtGui import *
from .statics import *
import typing
import abc


class Screen(QWidget, abc.ABC, metaclass=type("_", (type(abc.ABC), type(QWidget)), {})):
    """
    TODO: Document
    """

    Loading = 0
    Home = 1

    def __init__(self):
        """
        TODO: Document
        """
        super(Screen, self).__init__()

        # Initialise the GUI window name
        self.name = self.__class__.__name__

    @property
    def _background_pixmap(self) -> QPixmap:
        """
        TODO: Document
        :return:
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
        TODO: Document
        :return:
        """

        for widget in QApplication.instance().topLevelWidgets():
            if "ScreenManager" in repr(widget):
                return widget
        return None

    @abc.abstractmethod
    def _config(self):
        """
        TODO: Document

        :return:
        """

        pass

    @abc.abstractmethod
    def _set_style(self):
        """
        TODO: Document
        :return:
        """

        pal = self.manager.palette()
        pal.setBrush(QPalette.Window, QBrush(self._background_pixmap))
        self.manager.setPalette(pal)

    @abc.abstractmethod
    def post_init(self):
        """
        TODO: Document
        :return:
        """

        pass

    @abc.abstractmethod
    def on_switch(self):
        """
        TODO: Document
        :return:
        """

        self._set_style()


class ScreenManager(QMainWindow):
    """
    TODO: Document
    """

    def __init__(self, *args):
        """
        TODO: Document

        :param args:
        """

        super(ScreenManager, self).__init__()

        # Declare the screen structure - a box layout with a stacked widget holding the screens
        self._base = QHBoxLayout()
        self._screens_stacked = QStackedWidget()
        self._screens = dict()

        # Set some basic window properties
        self.setFixedSize(SCREEN_WIDTH, SCREEN_HEIGHT)

        # Add all screens
        for screen in args:
            self._screens_stacked.addWidget(screen)
            self._screens[screen.name] = screen
        self._base.addWidget(self._screens_stacked)

        # Finally set the layout and the current screen
        self._container = QWidget()
        self._container.setLayout(self._base)
        self.setCentralWidget(self._container)
        self.screen = Screen.Loading

    @property
    def screen(self) -> Screen:
        """
        TODO: Document
        """

        return self._screens_stacked.currentWidget()

    @screen.setter
    def screen(self, index: int):
        """
        TODO: Document
        """

        self._screens_stacked.setCurrentIndex(index)
        self.setWindowTitle(self._screens_stacked.currentWidget().name)
        self._screens_stacked.currentWidget().on_switch()

    @property
    def screens(self) -> dict:
        """
        TODO: Document
        :return:
        """

        return self._screens

    def post_init(self):
        """
        TODO: Document
        :return:
        """

        for scr in self._screens.values():
            scr.post_init()
