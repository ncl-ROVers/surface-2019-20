from PySide2.QtWidgets import *
import enum as _enum


class Screen(_enum.Enum):
    """
    TODO: Document
    """

    Loading = 0
    Home = 1


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
        self._screens = QStackedWidget()

        # Add all screens
        for screen in args:
            self._screens.addWidget(screen)

        # Finally set the layout and the current screen
        self._base.addWidget(self._screens)
        self.setLayout(self._base)
        self.screen = Screen.Loading

    @property
    def screen(self):
        """
        TODO: Document
        """

        return self._screens.currentWidget()

    @screen.setter
    def screen(self, screen: Screen):
        """
        TODO: Document
        """

        self._screens.setCurrentIndex(screen.value)
        self.setWindowTitle(screen.name)
