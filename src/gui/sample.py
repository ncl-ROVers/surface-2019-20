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

        self._layout = QHBoxLayout()
        self.buttonLayout = QHBoxLayout()
        self.nameLayout = QVBoxLayout()
        self.topLeftLayout = QHBoxLayout()
        self.topRightLayout = QHBoxLayout()
        self.motorLayout = QVBoxLayout()
        self.bottonLeftLayout = QHBoxLayout()
        self.leftLayout = QVBoxLayout()
        self.RightLayout = QVBoxLayout()
        
        
        self.leakLabel = QLabel(self)
        self.temperatureLabel = QLabel(self)
        self.depthLabel = QLabel(self)
        self.accelarationLabel = QLabel(self)
        self.rotationLabel = QLabel(self)
        self.buttonHome = QPushButton("Home")
        self.buttonInfo = QPushButton("Info")
        self.buttonHelp = QPushButton("Help")
        self.axo = QGraphicsView()
        self.teamName = QPlainTextEdit("ROVER GUE")
        self.title = QTextEdit("Deep Water Exploration")
        self.camera_2 = QGraphicsView()
        self.camera_3 = QGraphicsView()
        self.camera_1 = QGraphicsView()
        self.horizon = QGraphicsView()
        self.links = QGraphicsView()
        self.buttonMotorLeft = QPushButton("Left Motor")
        self.buttonMotorRight = QPushButton("Right Motor")
        self.buttonMotorFront = QPushButton("Front Motor")
        self.buttonMotorBack = QPushButton("Back Motor")

        self._config()
        self.setLayout(self._layout)


    def _config(self):
        """
        TODO: Document

        :return:
        """
        self.leakLabel.setText("Leak Sensor")
        self.temperatureLabel.setText("Temperature")
        self.depthLabel.setText("Depth")
        self.accelarationLabel.setText("Accelaration")
        self.rotationLabel.setText("Rotation")
        self.buttonHome.setObjectName("buttonHome")
        self.buttonInfo.setObjectName("buttonInfo")
        self.buttonHelp.setObjectName("buttonHelp")
        self.axo.setObjectName("Axo")
        self.teamName.setObjectName("teamName")
        self.title.setObjectName("title")
        self.links.setObjectName("Links")
        self.camera_2.setObjectName("camera_2")
        self.camera_3.setObjectName("camera_3")
        self.camera_1.setObjectName("camera_1")
        self.horizon.setObjectName("horizon")

        self.buttonLayout.addWidget(self.buttonHome)
        self.buttonLayout.addWidget(self.buttonInfo)
        self.buttonLayout.addWidget(self.buttonHelp)
        self.nameLayout.addWidget(self.teamName)
        self.nameLayout.addWidget(self.axo)
        self.topRightLayout.addWidget(self.camera_2)
        self.topRightLayout.addWidget(self.camera_3)
        self.topRightLayout.addWidget(self.horizon)
        self.motorLayout.addWidget(self.buttonMotorLeft)
        self.motorLayout.addWidget(self.buttonMotorRight)
        self.motorLayout.addWidget(self.buttonMotorFront)
        self.motorLayout.addWidget(self.buttonMotorBack)
        self.bottonLeftLayout.addWidget(self.leakLabel)
        self.bottonLeftLayout.addWidget(self.temperatureLabel)
        self.bottonLeftLayout.addWidget(self.depthLabel)
        self.bottonLeftLayout.addWidget(self.accelarationLabel)
        self.bottonLeftLayout.addWidget(self.rotationLabel)
        self.topLeftLayout.addLayout(self.buttonLayout)
        self.topLeftLayout.addLayout(self.nameLayout)
        self.leftLayout.addLayout(self.topLeftLayout)
        self.leftLayout.addLayout(self.motorLayout)
        self.leftLayout.addLayout(self.bottonLeftLayout)
        self.RightLayout.addLayout(self.topRightLayout)
        self.RightLayout.addWidget(self.camera_1)
        self.RightLayout.addWidget(self.links)
        self._layout.addLayout(self.leftLayout)
        self._layout.addLayout(self.RightLayout)

       


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
