from PySide2.QtWidgets import *
from PySide2.QtCore import *

_MAX_LOADING = 100
_MIN_LOADING = 0


class Loading(QWidget):
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
        self._bar.text()

        self._label.setText("Loading ...")
        self._label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self._layout.addWidget(self._label)
        self._layout.addWidget(self._bar)
        self._layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

    @property
    def progress(self):
        """

        :return:
        """
        return self._progress

    @progress.setter
    def progress(self, value: int):
        """

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

        :return:
        """

        # TODO: Sample to be removed later
        from time import sleep
        for x in range(101):
            QApplication.instance().processEvents()
            self.progress = x
            sleep(0.01)
