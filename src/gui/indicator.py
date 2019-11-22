from .utils import Screen
from PySide2.QtWidgets import *
from PySide2.QtGui import QBrush, QColor
from PySide2.QtCore import Qt
from .component import indicator


class Indicator(Screen):
    """
    Call the method update_date(self, leak, temperature, depth, acceleration, x, y, z)
    to update the data
    """

    def __init__(self):
        """
        TODO: Document
        """
        super(Indicator, self).__init__()

        self.number_leak = 50
        self.number_temperature = 32
        self.number_depth = 3.5
        self.number_acceleration = 4.5
        self.number_rotation_x = 30
        self.number_rotation_y = 65
        self.number_rotation_z = 27

        self._layout = QHBoxLayout()

        self.box_leak = QGraphicsView()
        self.box_temperature = QGraphicsView()
        self.box_depth = QGraphicsView()
        self.box_acceleration = QGraphicsView()
        self.box_rotation = QGraphicsView()

        self._config()

    def _config(self):
        """
        TODO: Document
        """
        super()._config()
        self._layout.addWidget(self.box_leak)
        self._layout.addWidget(self.box_temperature)
        self._layout.addWidget(self.box_depth)
        self._layout.addWidget(self.box_acceleration)
        self._layout.addWidget(self.box_rotation)

        self._set_size()
        self._set_indicator()
        self.setLayout(self._layout)

    def _set_size(self):
        self.box_leak.setMaximumSize(300, 300)
        self.box_temperature.setMaximumSize(300, 300)
        self.box_depth.setMaximumSize(300, 300)
        self.box_acceleration.setMaximumSize(300, 300)
        self.box_rotation.setMaximumSize(300, 300)
        self.box_leak.setStyleSheet("border: 0px")
        self.box_temperature.setStyleSheet("border: 0px")
        self.box_depth.setStyleSheet("border: 0px")
        self.box_acceleration.setStyleSheet("border: 0px")
        self.box_rotation.setStyleSheet("border: 0px")

    def _set_indicator(self):
        self.box_leak.setScene(indicator.Leak_Sensor())
        self.box_temperature.setScene(indicator.Temperature())
        self.box_depth.setScene(indicator.Depth())
        self.box_acceleration.setScene(indicator.Acceleration())
        self.box_rotation.setScene(indicator.Rotation())

        self.brush = QBrush()
        self.brush.setColor(QColor(8, 64, 67))
        self.brush.setStyle(Qt.SolidPattern)

        self.box_leak.setBackgroundBrush(self.brush)
        self.box_temperature.setBackgroundBrush(self.brush)
        self.box_depth.setBackgroundBrush(self.brush)
        self.box_acceleration.setBackgroundBrush(self.brush)
        self.box_rotation.setBackgroundBrush(self.brush)

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
        indicator.Leak_Sensor().update(self.number_leak)
        indicator.Temperature().update(self.number_temperature)
        indicator.Depth().update(self.number_depth)
        indicator.Acceleration().update(self.number_acceleration)
        indicator.Rotation().update(self.number_rotation_x, self.number_rotation_y, self.number_rotation_z)

    def _set_style(self):
        """
        TODO: Document
        """
        super()._set_style()

    def post_init(self):
        """
        TODO: Document
        """
        super().post_init()

    def on_switch(self):
        """
        TODO: Document
        """
        super().on_switch()