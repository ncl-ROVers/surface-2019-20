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
        self.layout_button = QHBoxLayout()
        self.layout_name = QVBoxLayout()
        self.layout_top_left = QHBoxLayout()
        self.layout_top_right = QHBoxLayout()
        self.layout_motor = QVBoxLayout()
        self.layout_botton_left = QHBoxLayout()
        self.layout_left = QVBoxLayout()
        self.layout_right = QVBoxLayout()
        
        
        self.label_leak = QLabel()
        self.label_temperature = QLabel()
        self.label_depth = QLabel()
        self.label_accelaration = QLabel()
        self.label_rotation = QLabel()
        self.label_team_name = QLabel()
        self.label_title = QLabel()
        self.button_home = QPushButton("Home")
        self.button_info = QPushButton("Info")
        self.button_help = QPushButton("Help")
        self.button_motor_left = QPushButton("Left Motor")
        self.button_motor_right = QPushButton("Right Motor")
        self.button_motor_front = QPushButton("Front Motor")
        self.button_motor_back = QPushButton("Back Motor")
        self.box_axo = QGraphicsView()
        self.box_camera_2 = QGraphicsView()
        self.box_camera_3 = QGraphicsView()
        self.box_camera_1 = QGraphicsView()
        self.box_horizon = QGraphicsView()
        self.box_links = QGraphicsView()
        

        self._config()
        self.setLayout(self._layout)


    def _config(self):
        """
        TODO: Document

        :return:
        """
        self._set_name()
        self._set_left_layout()
        self._set_right_layout()
            
        self._layout.addLayout(self.layout_left)
        self._layout.addLayout(self.layout_right)
        

       
    def _set_name(self):

        self.label_leak.setText("Leak Sensor")
        self.label_temperature.setText("Temperature")
        self.label_depth.setText("Depth")
        self.label_accelaration.setText("Accelaration")
        self.label_rotation.setText("Rotation")
        self.label_team_name.setText("ROVER GUE")
        self.label_title.setText("Deep Water Exploration")
        self.button_home.setObjectName("buttonHome")
        self.button_info.setObjectName("buttonInfo")
        self.button_help.setObjectName("buttonHelp")
        self.box_axo.setObjectName("Axo")
        self.box_links.setObjectName("Links")
        self.box_camera_1.setObjectName("camera_1")
        self.box_camera_2.setObjectName("camera_2")
        self.box_camera_3.setObjectName("camera_3")
        self.box_horizon.setObjectName("horizon")

    def _set_left_layout(self):

        self.layout_button.addWidget(self.button_home)
        self.layout_button.addWidget(self.button_info)
        self.layout_button.addWidget(self.button_help)
        self.layout_name.addWidget(self.label_team_name)
        self.layout_name.addWidget(self.label_title)
        self.layout_motor.addWidget(self.button_motor_left)
        self.layout_motor.addWidget(self.button_motor_right)
        self.layout_motor.addWidget(self.button_motor_front)
        self.layout_motor.addWidget(self.button_motor_back)
        self.layout_botton_left.addWidget(self.label_leak)
        self.layout_botton_left.addWidget(self.label_temperature)
        self.layout_botton_left.addWidget(self.label_depth)
        self.layout_botton_left.addWidget(self.label_accelaration)
        self.layout_botton_left.addWidget(self.label_rotation)
        self.layout_top_left.addLayout(self.layout_button)
        self.layout_top_left.addLayout(self.layout_name)
        self.layout_left.addLayout(self.layout_top_left)
        self.layout_left.addLayout(self.layout_motor)
        self.layout_left.addLayout(self.layout_botton_left)

    def _set_right_layout(self):

        self.layout_top_right.addWidget(self.box_camera_2)
        self.layout_top_right.addWidget(self.box_camera_3)
        self.layout_top_right.addWidget(self.box_horizon)
        self.layout_right.addLayout(self.layout_top_right)
        self.layout_right.addWidget(self.box_camera_1)
        self.layout_right.addWidget(self.box_links)
        

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
