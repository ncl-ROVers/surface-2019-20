from PySide2.QtWidgets import *
from PySide2.QtCore import *
from .utils import Screen as Screen
from .. import common
import os

_MAX_LOADING = 100
_MIN_LOADING = 0


class Loading(Screen):
    """
    TODO: Document
    """

    def __init__(self):
        """
        TODO: Document
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
        TODO: Document

        :return:
        """

        self._bar.setRange(_MIN_LOADING, _MAX_LOADING)

        self._label.setText("Loading ...")
        self._label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self._layout.addWidget(self._label)
        self._layout.addWidget(self._bar)
        self._layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

    def _set_style(self):
        """
        TODO: Document
        :return:
        """
        x = os.path.join(common.GUI_LOADING, "download.jpg").replace("\\", "/")  # TODO: Error, can't load it :(
        self._get_manager().setStyleSheet(f"background-image: url({x});")

    def post_init(self):
        """
        TODO: Document
        :return:
        """

        super().post_init()

    def on_switch(self):
        """
        TODO: Document
        :return:
        """

        super().on_switch()

    @property
    def progress(self):
        """
        TODO: Document
        :return:
        """

        return self._progress

    @progress.setter
    def progress(self, value: int):
        """
        TODO: Document
        :param value:
        :return:
        """

        if not _MIN_LOADING <= self._progress <= _MAX_LOADING:
            raise ValueError(f"Progress must be between {_MIN_LOADING} and {_MAX_LOADING}")
        else:
            self._progress = value
            self._bar.setValue(value)

    def load(self):
        """
        TODO: Document
        :return:
        """

        # TODO: Sample to be removed later
        from time import sleep
        for x in range(101):
            QApplication.instance().processEvents()
            self.progress = x
            sleep(0.01)
