from PySide2.QtWidgets import *
import enum as _enum


class Screen(_enum.Enum):
    """
    TODO: Document
    TODO: Actually, make it an abstract class instead. It will have to set the background and specify methods
      for the manager (just like an enum name, value). Maybe do some other config too?
      Add this for example - self.setStyleSheet("background-color: rgba(34, 51, 54, 255)")
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
        self.show()

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
