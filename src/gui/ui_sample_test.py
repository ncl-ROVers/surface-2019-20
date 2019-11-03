import sys
from PySide2 import QtGui, QtWidgets, QtCore
from PySide2.QtWidgets import QApplication, QMainWindow
from .ui_sample import Ui_MainWindow


# 主窗体类
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

app = QApplication()
window = MainWindow()
app.exec_();

