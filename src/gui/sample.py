"""
Date:2019/11/01
Author:Zhanqiu Wang
Note:The first version of sample screen
"""

from PySide2.QtWidgets import *
from PySide2.QtMultimedia import *
from PySide2.QtMultimediaWidgets import *
from .component.cameras import Camera
from .component.indicator import *
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
        self.layout_bottom_left = QHBoxLayout()
        self.layout_left = QVBoxLayout()
        self.layout_right = QVBoxLayout()

        self.box_leak = QGraphicsView()
        self.box_temperature = QGraphicsView()
        self.box_depth = QGraphicsView()
        self.box_acceleration = QGraphicsView()
        self.box_rotation = QGraphicsView()
        self.box_team_name = QGraphicsView()
        self.box_title = QGraphicsView()
        self.button_home = QPushButton("Home")
        self.button_info = QPushButton("Info")
        self.button_help = QPushButton("Help")
        self.button_motor_left = QPushButton("Left Motor")
        self.button_motor_right = QPushButton("Right Motor")
        self.button_motor_front = QPushButton("Front Motor")
        self.button_motor_back = QPushButton("Back Motor")
        self.box_axo = QGraphicsView()
        self.box_camera_1 = QCameraViewfinder()
        self.box_camera_2 = QCameraViewfinder()
        self.box_camera_3 = QCameraViewfinder()
        self.box_horizon = QGraphicsView()
        self.box_links = QGraphicsView()

        self._config()
        self.setLayout(self._layout)

    def _config(self):
        """
        TODO: Document

        :return:
        """
        self._set_left_layout()
        self._set_right_layout()
        # self._set_geometry()
        self._set_scene()
        self._set_camera()
        self._set_indicator()

        self._layout.addLayout(self.layout_left)
        self._layout.addLayout(self.layout_right)
        self._set_size()

    def _set_camera(self):
        Camera()._camera_1().setViewfinder(self.box_camera_1)
        Camera()._camera_2().setViewfinder(self.box_camera_2)
        Camera()._camera_3().setViewfinder(self.box_camera_3)
        self.box_camera_1.show()
        self.box_camera_2.show()
        self.box_camera_3.show()
        image_camera_1 = QCameraImageCapture(Camera()._camera_1())
        image_camera_2 = QCameraImageCapture(Camera()._camera_2())
        image_camera_3 = QCameraImageCapture(Camera()._camera_3())
        Camera()._camera_1().setCaptureMode(QCamera.CaptureStillImage)
        Camera()._camera_2().setCaptureMode(QCamera.CaptureStillImage)
        Camera()._camera_3().setCaptureMode(QCamera.CaptureStillImage)
        Camera()._camera_1().start()
        Camera()._camera_2().start()
        Camera()._camera_3().start()
        self.box_camera_1.setFixedSize(500, 375)
        self.box_camera_2.setFixedSize(200, 150)
        self.box_camera_3.setFixedSize(200, 150)

    def _set_indicator(self):
        self.box_leak.setScene(Leak_Sensor())
        self.box_temperature.setScene(Temperature())
        self.box_depth.setScene(Depth())
        self.box_rotation.setScene(Rotation())
        self.box_acceleration.setScene(Acceleration())

    def _set_size(self):
        self.box_leak.setMaximumSize(90, 100)
        self.box_temperature.setMaximumSize(90, 100)
        self.box_depth.setMaximumSize(90, 100)
        self.box_acceleration.setMaximumSize(90, 100)
        self.box_rotation.setMaximumSize(90, 100)
        self.box_team_name.setMaximumSize(200, 100)
        self.box_title.setMaximumSize(200, 100)

    def _set_scene(self):
        pass

    def _set_left_layout(self):
        self.layout_button.addWidget(self.button_home)
        self.layout_button.addWidget(self.button_info)
        self.layout_button.addWidget(self.button_help)
        self.layout_name.addWidget(self.box_team_name)
        self.layout_name.addWidget(self.box_title)
        self.layout_motor.addWidget(self.button_motor_left)
        self.layout_motor.addWidget(self.button_motor_right)
        self.layout_motor.addWidget(self.button_motor_front)
        self.layout_motor.addWidget(self.button_motor_back)
        self.layout_bottom_left.addWidget(self.box_leak)
        self.layout_bottom_left.addWidget(self.box_temperature)
        self.layout_bottom_left.addWidget(self.box_depth)
        self.layout_bottom_left.addWidget(self.box_acceleration)
        self.layout_bottom_left.addWidget(self.box_rotation)
        self.layout_top_left.addLayout(self.layout_button)
        self.layout_top_left.addLayout(self.layout_name)
        self.layout_left.addLayout(self.layout_top_left)
        self.layout_left.addLayout(self.layout_motor)
        self.layout_left.addLayout(self.layout_bottom_left)

    def _set_right_layout(self):
        self.layout_top_right.addWidget(self.box_horizon)
        self.layout_top_right.addWidget(self.box_camera_2)
        self.layout_top_right.addWidget(self.box_camera_3)
        self.layout_right.addLayout(self.layout_top_right)
        self.layout_right.addWidget(self.box_camera_1)
        self.layout_right.addWidget(self.box_links)

    def _set_style(self):
        x = os.path.join(common.GUI_LOADING, "download.jpg").replace("\\", "/")  # TODO: Error, can't load it :(
        self._get_manager().setStyleSheet(f"background-image: url({x});")

    # def _set_geometry(self):

    #    self.button_home.setGeometry(QtCore.QRect(20, 30, 75, 23))
    #    self.button_info.setGeometry(QtCore.QRect(110, 30, 75, 23))
    #    self.button_help.setGeometry(QtCore.QRect(200, 30, 75, 23))
    #    self.button_motor_front.setGeometry(QtCore.QRect(130, 190, 75, 23))
    #    self.button_motor_left.setGeometry(QtCore.QRect(30, 240, 75, 23))
    #    self.button_motor_right.setGeometry(QtCore.QRect(220, 240, 75, 23))
    #    self.button_motor_back.setGeometry(QtCore.QRect(130, 300, 75, 23))
    #    self.box_leak.setGeometry(QtCore.QRect(20, 650, 121, 131))
    #    self.box_temperature.setGeometry(QtCore.QRect(170, 650, 121, 131))
    #    self.box_depth.setGeometry(QtCore.QRect(310, 650, 121, 131))
    #    self.box_acceleration.setGeometry(QtCore.QRect(450, 650, 121, 131))
    #    self.box_rotation.setGeometry(QtCore.QRect(590, 650, 121, 131))
    #    self.box_horizon.setGeometry(QtCore.QRect(520, 20, 211, 141))
    #    self.box_camera_2.setGeometry(QtCore.QRect(750, 20, 211, 141))
    #    self.box_camera_3.setGeometry(QtCore.QRect(980, 20, 211, 141))
    #    self.box_camera_1.setGeometry(QtCore.QRect(670, 220, 461, 271))
    #    self.box_links.setGeometry(QtCore.QRect(760, 630, 411, 151))
    #    self.box_title.setGeometry(QtCore.QRect(330, 20, 120, 80))
    #    self.box_team_name.setGeometry(QtCore.QRect(330, 140, 120, 80))

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
