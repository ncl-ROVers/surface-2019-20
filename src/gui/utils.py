from PySide2.QtWidgets import *
from .statics import *
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

    def _get_manager(self):
        """
        TODO: Document
        :return:
        """

        parent = self.parent()
        while parent:
            if "ScreenManager" in repr(parent):
                return parent
            else:
                parent = parent.parent()
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

        pass

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


class ScreenManager(QWidget):
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

        # Add all screens
        for screen in args:
            self._screens_stacked.addWidget(screen)
            self._screens[screen.name] = screen
        self._base.addWidget(self._screens_stacked)

        self._set_default_style()

        # Finally set the layout and the current screen
        self.setLayout(self._base)
        self.screen = Screen.Loading

    def _set_default_style(self):
        """
        TODO: Document
        :return:
        """

        self.setFixedSize(SCREEN_WIDTH, SCREEN_HEIGHT)

        r, g, b, a = Colour.MAJOR.value
        self.setStyleSheet(f"background-color: rgba({r}, {g}, {b}, {a})")

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
