"""
Date:2019/11/01
Author:Zhanqiu Wang
Note:The first version of sample screen
"""

from PySide2 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(681, 433)
        MainWindow.setMouseTracking(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("res/background.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.buttonHome = QtWidgets.QPushButton(MainWindow)
        self.buttonHome.setGeometry(QtCore.QRect(10, 20, 51, 51))
        self.buttonHome.setObjectName("buttonHome")
        self.buttonInfo = QtWidgets.QPushButton(MainWindow)
        self.buttonInfo.setGeometry(QtCore.QRect(70, 20, 51, 51))
        self.buttonInfo.setObjectName("buttonInfo")
        self.buttonHelp = QtWidgets.QPushButton(MainWindow)
        self.buttonHelp.setGeometry(QtCore.QRect(130, 20, 51, 51))
        self.buttonHelp.setObjectName("buttonHelp")
        self.Axo = QtWidgets.QGraphicsView(MainWindow)
        self.Axo.setGeometry(QtCore.QRect(10, 90, 311, 181))
        self.Axo.setObjectName("Axo")
        self.teamName = QtWidgets.QPlainTextEdit(MainWindow)
        self.teamName.setGeometry(QtCore.QRect(190, 20, 104, 31))
        self.teamName.setObjectName("teamName")
        self.title = QtWidgets.QTextEdit(MainWindow)
        self.title.setGeometry(QtCore.QRect(190, 50, 161, 31))
        self.title.setObjectName("title")
        self.camera_2 = QtWidgets.QGraphicsView(MainWindow)
        self.camera_2.setGeometry(QtCore.QRect(470, 20, 81, 51))
        self.camera_2.setObjectName("camera_2")
        self.camera_3 = QtWidgets.QGraphicsView(MainWindow)
        self.camera_3.setGeometry(QtCore.QRect(580, 20, 81, 51))
        self.camera_3.setObjectName("camera_3")
        self.camera_1 = QtWidgets.QGraphicsView(MainWindow)
        self.camera_1.setGeometry(QtCore.QRect(360, 90, 311, 181))
        self.camera_1.setObjectName("camera_1")
        self.horizon = QtWidgets.QGraphicsView(MainWindow)
        self.horizon.setGeometry(QtCore.QRect(360, 20, 81, 51))
        self.horizon.setObjectName("horizon")
        self.links = QtWidgets.QGraphicsView(MainWindow)
        self.links.setGeometry(QtCore.QRect(360, 290, 311, 51))
        self.links.setObjectName("links")
        self.slider = QtWidgets.QGraphicsView(MainWindow)
        self.slider.setGeometry(QtCore.QRect(10, 290, 311, 51))
        self.slider.setObjectName("slider")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "Form", None, -1))
        self.buttonHome.setText(QtWidgets.QApplication.translate("MainWindow", "HOME", None, -1))
        self.buttonInfo.setText(QtWidgets.QApplication.translate("MainWindow", "INFO", None, -1))
        self.buttonHelp.setText(QtWidgets.QApplication.translate("MainWindow", "HELP", None, -1))
        self.teamName.setPlainText(QtWidgets.QApplication.translate("MainWindow", "ROVER GUE", None, -1))

