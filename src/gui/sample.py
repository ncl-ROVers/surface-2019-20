"""
Date:2019/11/01
Author:Zhanqiu Wang
Note:The first version of sample screen
"""

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from .utils import Screen as Screen
from .. import common
import os

class Sample(Screen):

    def __init__(self):
        """
        TODO: Document
        """

        super(Sample, self).__init__()

        self._progress = 0

        self._layout = QVBoxLayout()

        self.buttonHome = QPushButton()
        self.buttonInfo = QPushButton()
        self.buttonHelp = QPushButton()
        self.Axo = QGraphicsView()
        self.teamName = QPlainTextEdit()
        self.title = QTextEdit()
        self.camera_2 = QGraphicsView()
        self.camera_3 = QGraphicsView()
        self.camera_1 = QGraphicsView()
        self.horizon = QGraphicsView()
        self.links = QGraphicsView()
        self.slider = QGraphicsView()

        self._config()
        self.setLayout(self._layout)


    def _config(self):
        """
        TODO: Document

        :return:
        """

        self.buttonHome.setGeometry(QRect(10, 20, 51, 51))
        self.buttonHome.setObjectName("buttonHome")
        self.buttonInfo.setGeometry(QRect(70, 20, 51, 51))
        self.buttonInfo.setObjectName("buttonInfo")
        self.buttonHelp.setGeometry(QRect(130, 20, 51, 51))
        self.buttonHelp.setObjectName("buttonHelp")
        self.Axo.setGeometry(QRect(10, 90, 311, 181))
        self.Axo.setObjectName("Axo")
        self.teamName.setGeometry(QRect(190, 20, 104, 31))
        self.teamName.setObjectName("teamName")
        self.title.setGeometry(QRect(190, 50, 161, 31))
        self.title.setObjectName("title")
        self.camera_2.setGeometry(QRect(470, 20, 81, 51))
        self.camera_2.setObjectName("camera_2")
        self.camera_3.setGeometry(QRect(580, 20, 81, 51))
        self.camera_3.setObjectName("camera_3")
        self.camera_1.setGeometry(QRect(360, 90, 311, 181))
        self.camera_1.setObjectName("camera_1")
        self.horizon.setGeometry(QRect(360, 20, 81, 51))
        self.horizon.setObjectName("horizon")
        self.links.setGeometry(QRect(360, 290, 311, 51))
        self.links.setObjectName("links")
        self.slider.setGeometry(QRect(10, 290, 311, 51))
        self.slider.setObjectName("slider")

       


    def _set_style(self):
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

    """
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(681, 433)
        MainWindow.setMouseTracking(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("res/background.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "Form", None, -1))
        self.buttonHome.setText(QtWidgets.QApplication.translate("MainWindow", "HOME", None, -1))
        self.buttonInfo.setText(QtWidgets.QApplication.translate("MainWindow", "INFO", None, -1))
        self.buttonHelp.setText(QtWidgets.QApplication.translate("MainWindow", "HELP", None, -1))
        self.teamName.setPlainText(QtWidgets.QApplication.translate("MainWindow", "ROVER GUE", None, -1))
    """
