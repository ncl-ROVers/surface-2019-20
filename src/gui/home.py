"""
TODO: Document
"""
import typing
from ..common import data_manager as dm, Log
from .utils import Screen, Colour
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

# Declare low and high limits for the sensor indicators
_CRITICAL_LEAK = 50
_CRITICAL_TEMPERATURE = 50

# Declare the frequencies of the data updates
_SENSORS_CLOCK_INTERVAL = 1000
_CONNECTIONS_CLOCK_INTERVAL = 10


class _SensorIndicator(QWidget):
    """
    TODO: Document
    """

    def __init__(self, header: str, body: str, *, low_limit: float = None, high_limit: float = None,
                 text_format_func: typing.Callable = None):
        """
        TODO: Document

        .. warning::
            `text_format_func` must follow the signature present in `_default_text_format`.

        :param header: Header text displayed above the values
        :param body: Body containing the values
        :param low_limit: Optional, lower limit of the values
        :param high_limit: Optional, higher limit of the values
        :param text_format_func: Optional text formatting function for custom text rendering
        """
        super(_SensorIndicator, self).__init__()
        self._low_limit = low_limit
        self._high_limit = high_limit
        self._header = header
        self._body = body

        # Remember the number of "{}" elements which will be formatted via Python string formatting
        self._placeholder_count = self._body.count("{}")

        # The text formatting function should be flexible for each indicator, so allow passing a specific one
        self._text_format_func = text_format_func if text_format_func else self._default_text_format

        # Create the QT objects and set the layout
        self._layout = QVBoxLayout()
        self._header_label = QLabel()
        self._body_label = QLabel()
        self._footer_label = QLabel()
        self._layout.addWidget(self._header_label)
        self._layout.addWidget(self._body_label)
        self._layout.addWidget(self._footer_label)
        self.setLayout(self._layout)

        # Set the alignments to center, to display all text in the middle
        self._body_label.setAlignment(Qt.AlignCenter)
        self._header_label.setAlignment(Qt.AlignHCenter)

        # Set spacing to 0 to remove the default margin
        self._layout.setSpacing(0)

        # Expanding size policy allows the widget to take full available space in the layout
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Set the style and initially update the visible items
        self._set_style()
        self._header_label.setText(self._header)
        self.update_text(*("0" for _ in range(self._placeholder_count)))

    @staticmethod
    def _default_text_format(body: str, body_label: QLabel, *args):
        """
        Function used as a default text formatter for the indicator.

        By default renders everything except for units with font-size 60, whereas the units have font-size set to 30.

        :param body: Body text containing the values to format
        :param body_label: QLabel wrapper around the body
        :param args: New values to be displayed
        """
        index = body.rfind("{}") + 2
        text = body[:index] + "<span style=\"font-size:30px;\">" + body[index:] + "</span>"
        text = text.replace("\n", "<br>")
        text = text.format(*args)
        body_label.setText(text)

    def _set_style(self):
        """
        Styling method used to ensure all items are visually matching the expected outcome.
        """
        r, g, b, _ = Colour.ACCENT.value

        # Each element has its own style sheet for maximum flexibility
        self.setStyleSheet(f"""
            QWidget {{ 
                background-color: rgb({r}, {g}, {b});
            }}""")
        self._header_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 30px;
            }""")
        self._footer_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 30px;
            }""")
        self._body_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 60px;
            }""")

        # Make sure the body takes as much of the space as possible by making the header and footer as small as possible
        self._header_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self._footer_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)

        # Rich text flag is mandatory due to the HTML code injections within the label's text
        self._body_label.setTextFormat(Qt.RichText)

    def update_text(self, *args):
        """
        Update the text with new values. The number of supplied values must match the number of placeholders in the
        body.

        :param args: New values to display
        """
        if len(args) != self._placeholder_count:
            raise ValueError(f"Mismatch between expected number of arguments: {len(self._format_chars_count)}, "
                             f"and received: {len(args)}")
        if len(args) > 0:
            self._text_format_func(self._body, self._body_label, *args)
        else:
            self._body_label.setText(self._body)

        # Change the colour if a single argument was supplied (skip rotation) and there is a low or high limit set
        if len(args) == 1 and (self._low_limit is not None or self._high_limit is not None):
            value = args[0]

            # Initial value is empty string
            if isinstance(value, str) and value.isdigit():
                value = int(value)

            # Going over or below allowed values should result in different text colours
            if self._low_limit is not None and value <= self._low_limit:
                self._body_label.setStyleSheet("""
                    QLabel {
                        color: red;
                        font-size: 60px;
                    }""")
            elif self._high_limit is not None and value >= self._high_limit:
                self._body_label.setStyleSheet("""
                    QLabel {
                        color: red;
                        font-size: 60px;
                    }""")
            else:
                self._body_label.setStyleSheet("""
                    QLabel {
                        color: white;
                        font-size: 60px;
                    }""")


class _SensorIndicators(QHBoxLayout):
    """
    TODO: Document
    """

    def __init__(self):
        """
        TODO: Document
        """
        super(_SensorIndicators, self).__init__()

        # Create the widgets and add them to the layout
        self._leak = _SensorIndicator("Leak", "{}%", high_limit=_CRITICAL_LEAK)
        self._temp = _SensorIndicator("Temperature", "{}℃", high_limit=_CRITICAL_TEMPERATURE)
        self._depth = _SensorIndicator("Depth", "{}cm")
        self._acc = _SensorIndicator("Acceleration", "{}m/s")
        self._rot = _SensorIndicator("Rotation:", "x: {}\ny: {}\nz: {}", text_format_func=self._rotation_text_format)
        self.addWidget(self._leak)
        self.addWidget(self._temp)
        self.addWidget(self._depth)
        self.addWidget(self._acc)
        self.addWidget(self._rot)

    @staticmethod
    def _rotation_text_format(body: str, body_label: QLabel, *args):
        """
        TODO: Document

        :param body:
        :param body_label:
        :param args:
        :return:
        """
        text = "<span style=\"font-size:45px;\">" + body + "</span>"
        text = text.replace("\n", "<br>")
        text = text.format(*args)
        body_label.setText(text)

    def update_readings(self):
        """
        TODO: Document

        :return:
        """
        Log.debug("Updating sensor readings")

        readings = dm.received.get_all()
        self._acc.update_text(readings["acceleration"])
        self._depth.update_text(readings["depth"])
        self._leak.update_text(readings["leak"])
        self._temp.update_text(readings["temperature"])
        self._rot.update_text(readings["rotation_x"], readings["rotation_y"], readings["rotation_z"])


class Home(Screen):
    """
    TODO: Document
    """

    def __init__(self):
        """
        Standard constructor.
        """
        super(Home, self).__init__()

        # Clocks used to update the sensor readings and the connections
        self._sensors_clock = QTimer()
        self._sensors_clock.setInterval(_SENSORS_CLOCK_INTERVAL)
        self._connections_clock = QTimer()
        self._connections_clock.setInterval(_CONNECTIONS_CLOCK_INTERVAL)

        # Basic layout consists of vertical box layout, within which there are two rows (cameras and indicators)
        self._layout = QVBoxLayout()
        self._cameras = QGridLayout()
        self._indicators = QHBoxLayout()

        # Within the cameras section, there are 3 cameras provided (main and two side cameras)
        self._main_camera = QPushButton("Main camera placeholder")
        self._top_camera = QPushButton("Top camera placeholder")
        self._bottom_camera = QPushButton("Bottom camera placeholder")

        # Within the indicators, there are sensor and connection indicators
        self._sensors = _SensorIndicators()
        self._connections = QPushButton("Indicators placeholder")

        self._config()
        self.setLayout(self._layout)

    def _config(self):
        """
        Standard configuration method.
        """
        super()._config()

        # Connect the clock timers to the functions
        self._sensors_clock.timeout.connect(self._sensors.update_readings)
        # TODO: Enable once added to the screen
        # self._connections_clock.timeout.connect(self._connections.update_readings)

        # TODO: Placeholders - making them take max space available for properly visible items
        self._main_camera.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._top_camera.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._bottom_camera.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._connections.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Main camera takes the height of 2 side cameras and 2/3 of the width of the screen
        self._cameras.addWidget(self._main_camera, 0, 0, 2, 1)
        self._cameras.addWidget(self._top_camera, 0, 1)
        self._cameras.addWidget(self._bottom_camera, 1, 1)
        self._cameras.setColumnStretch(0, 2)
        self._cameras.setColumnStretch(1, 1)

        # Sensors are to the left, whereas connections are to the right
        self._indicators.addLayout(self._sensors)
        self._indicators.addWidget(self._connections)

        # Cameras take 3/4 of the height of the screen
        self._layout.addLayout(self._cameras)
        self._layout.addLayout(self._indicators)
        self._layout.setStretch(0, 3)
        self._layout.setStretch(1, 1)

    def _set_style(self):
        """
        Default inherited.
        """
        super()._set_style()

    def post_init(self):
        """
        Default inherited.
        """
        super().post_init()

    def on_switch(self):
        """
        Display the menu bar as it should only be disabled in the loading screen, and start all clocks.
        """
        super().on_switch()
        self.manager.bar.parent().setVisible(True)
        self._sensors_clock.start()
        self._connections_clock.start()

    def on_exit(self):
        """
        Stop the clocks.
        """
        super().on_exit()
        self._sensors_clock.stop()
        self._connections_clock.stop()
