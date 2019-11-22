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
from PySide2.QtGui import QBrush, QColor
from PySide2.QtCore import Qt
from .component.indicator import Leak_Sensor, Temperature, Depth, Acceleration, Rotation
from src.gui.gui_process.process_management import Process_On


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

        self.number_leak = 0
        self.number_temperature = 0
        self.number_depth = 0
        self.number_acceleration = 0
        self.number_rotation_x = 0
        self.number_rotation_y = 0
        self.number_rotation_z = 0

        self.scene_leak = Leak_Sensor()
        self.scene_temperature = Temperature()
        self.scene_depth = Depth()
        self.scene_acceleration = Acceleration()
        self.scene_rotation = Rotation()

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
        self.process = Process_On(self)
        self.process.start()

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
        self.box_acceleration.setScene(Acceleration())
        self.box_rotation.setScene(Rotation())

        self.brush = QBrush()
        self.brush.setColor(QColor(8, 64, 67))
        self.brush.setStyle(Qt.SolidPattern)

        self.box_leak.setBackgroundBrush(self.brush)
        self.box_temperature.setBackgroundBrush(self.brush)
        self.box_depth.setBackgroundBrush(self.brush)
        self.box_acceleration.setBackgroundBrush(self.brush)
        self.box_rotation.setBackgroundBrush(self.brush)

    def _set_size(self):
        self.box_leak.setMaximumSize(200, 200)
        self.box_temperature.setMaximumSize(200, 200)
        self.box_depth.setMaximumSize(200, 200)
        self.box_acceleration.setMaximumSize(200, 200)
        self.box_rotation.setMaximumSize(200, 200)
        self.box_team_name.setMaximumSize(200, 200)
        self.box_title.setMaximumSize(200, 100)
        self.box_leak.setStyleSheet("border: 0px")
        self.box_temperature.setStyleSheet("border: 0px")
        self.box_depth.setStyleSheet("border: 0px")
        self.box_acceleration.setStyleSheet("border: 0px")
        self.box_rotation.setStyleSheet("border: 0px")

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
        super()._set_style()

    def update_date(self, leak, temperature, depth, acceleration, x, y, z):
        self.number_leak = leak
        self.number_temperature = temperature
        self.number_depth = depth
        self.number_acceleration = acceleration
        self.number_rotation_x = x
        self.number_rotation_y = y
        self.number_rotation_z = z
        self._update()

    def _update(self):
        self.scene_leak._update(self.number_leak)
        self.scene_temperature._update(self.number_temperature)
        self.scene_depth._update(self.number_depth)
        self.scene_acceleration._update(self.number_acceleration)
        self.scene_rotation._update(self.number_rotation_x, self.number_rotation_y, self.number_rotation_z)
        self.box_leak.setScene(self.scene_leak)
        self.box_temperature.setScene(self.scene_temperature)
        self.box_depth.setScene(self.scene_depth)
        self.box_acceleration.setScene(self.scene_acceleration)
        self.box_rotation.setScene(self.scene_rotation)

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
