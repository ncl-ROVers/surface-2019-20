"""
TODO: Document
"""
from ..common import get_hardware_info, Log, dm
from .utils import Screen, Colour, get_manager
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *


HARDWARE_READINGS_INTERVAL = 3000
CONNECTION_READINGS_INTERVAL = 1000


class _Indicator(QWidget):
    """
    TODO: Document
    """

    def __init__(self, header: str, body: str, footer: str = ""):
        """
        TODO: Document

        :param header: Header text displayed above the values
        :param body: Body containing the values
        :param footer: Footer text displayed below the values, empty by default
        """
        super(_Indicator, self).__init__()

        # Remember passed values and initialise the display text (body with substituted placeholder)
        self._header = header
        self._body = body
        self._footer = footer
        self._text = self._body.format("0")

        # Create the QT objects and set the layout
        self._layout = QVBoxLayout()
        self._header_label = QLabel()
        self._body_label = QLabel()
        self._footer_label = QLabel()
        self._layout.addWidget(self._header_label)
        self._layout.addWidget(self._body_label)
        self._layout.addWidget(self._footer_label)
        self.setLayout(self._layout)

        # Set the style and initially update the visible items
        self._set_style()
        self._header_label.setText(self._header)
        self._footer_label.setText(self._footer)
        self._set_text("0")

    @property
    def text(self):
        """
        TODO: Document
        :return:
        """
        return self._text

    @text.setter
    def text(self, value):
        """
        TODO: Document
        :param value:
        :return:
        """
        # TODO: Error check
        self._set_text(value)

    def _set_style(self):
        """
        Styling method used to ensure all items are visually matching the expected outcome.
        """
        r, g, b, _ = Colour.ACCENT.value

        # Set the alignments to center, to display all text in the middle
        self._body_label.setAlignment(Qt.AlignCenter)
        self._header_label.setAlignment(Qt.AlignHCenter)
        self._footer_label.setAlignment(Qt.AlignHCenter)

        # Set spacing to 0 to remove the default margin
        self._layout.setSpacing(0)

        # Expanding size policy allows the widget to take full available space in the layout
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

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

    def _set_text(self, value):
        """
        TODO: Document

        :param value:
        :return:
        """
        self._text = self._body.format(value)
        index = self._body.rfind("{}") + 2
        text = self._body[:index] + "<span style=\"font-size:30px;\">" + self._body[index:] + "</span>"
        text = text.replace("\n", "<br>")
        text = text.format(value)
        self._body_label.setText(text)


class _Indicators(QHBoxLayout):
    """
    TODO: Document
    """

    class _HardwareIndicators:
        """
        TODO: Document
        """

        def __init__(self):
            """
            TODO: Document
            """
            self._processes = _Indicator("Processes", "{}")
            self._threads = _Indicator("Threads", "{}")
            self._cpu = _Indicator("CPU", "{}%")
            self._memory = _Indicator("Memory", "{}%")
            self._gpu = _Indicator("GPU", "{}%")

            self.indicators = [self._processes, self._threads, self._cpu, self._memory, self._gpu]

        def update(self):
            """
            TODO: Document
            """
            processes, threads, cpu_load, memory_usage, gpu_load = \
                get_hardware_info(get_manager().references.parent_pid)
            Log.hardware(processes, threads, cpu_load, memory_usage, gpu_load)

            self._processes.text = processes
            self._threads.text = threads
            self._cpu.text = cpu_load
            self._memory.text = memory_usage
            self._gpu.text = gpu_load

    class _ConnectionIndicators:
        """
        TODO: Document
        """

        def __init__(self):
            """
            TODO: Document
            """
            self._pi = _Indicator("Raspberry Pi", "{}", "Status")
            self._pi._body_label.setStyleSheet("""
                        QLabel {
                            color: white;
                            font-size: 25px;
                        }""")
            self._ard_o = _Indicator("Arduino O", "{}", "Reachable?")
            self._ard_i = _Indicator("Arduino I", "{}", "Reachable?")

            self.indicators = [self._pi, self._ard_o, self._ard_i]

        def update(self):
            """
            TODO: Document
            """
            pi_status = get_manager().references.connection.status.name
            o_connection, i_connection = dm.received["A_O"], dm.received["A_I"]

            self._pi.text = pi_status
            self._ard_o.text = o_connection
            self._ard_i.text = i_connection

    def __init__(self):
        """
        TODO: Document
        """
        super(_Indicators, self).__init__()
        self._hardware_indicators = self._HardwareIndicators()
        self._connection_indicators = self._ConnectionIndicators()

        for indicator in self._hardware_indicators.indicators + self._connection_indicators.indicators:
            self.addWidget(indicator)

    @property
    def hardware(self):
        """
        TODO: Document
        """
        return self._hardware_indicators

    @property
    def connections(self):
        """
        TODO: Document
        """
        return self._connection_indicators


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
        self._hardware_readings_clock = QTimer()
        self._connection_readings_clock = QTimer()

        # Basic layout consists of vertical box layout, within which there are two rows (cameras and indicators)
        self._layout = QVBoxLayout()
        self._cameras = QGridLayout()
        self._indicators = _Indicators()

        # Within the cameras section, there are 3 cameras provided (main and two side cameras)
        self._main_camera = QLabel()
        self._top_camera = QLabel()
        self._bottom_camera = QLabel()

        self._config()
        self.setLayout(self._layout)

    def _config(self):
        """
        Standard configuration method.
        """
        super()._config()

        # Connect the clock timers to the functions
        self._hardware_readings_clock.setInterval(HARDWARE_READINGS_INTERVAL)
        self._hardware_readings_clock.timeout.connect(self._indicators.hardware.update)
        self._connection_readings_clock.setInterval(CONNECTION_READINGS_INTERVAL)
        self._connection_readings_clock.timeout.connect(self._indicators.connections.update)

        # TODO: Placeholders - making them take max space available for properly visible items
        self._main_camera.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._top_camera.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._bottom_camera.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Main camera takes the height of 2 side cameras and 2/3 of the width of the screen
        self._cameras.addWidget(self._main_camera, 0, 0, 2, 1)
        self._cameras.addWidget(self._top_camera, 0, 1)
        self._cameras.addWidget(self._bottom_camera, 1, 1)
        self._cameras.setColumnStretch(0, 2)
        self._cameras.setColumnStretch(1, 1)

        # Cameras take 3/4 of the height of the screen
        self._layout.addLayout(self._cameras)
        self._layout.addLayout(self._indicators)
        self._layout.setStretch(0, 3)
        self._layout.setStretch(1, 1)

    def _set_style(self):
        """
        Default inherited.

        TODO: Actually use this lol
        """
        super()._set_style()

    def post_init(self):
        """
        Default inherited.
        """
        super().post_init()

    def on_switch(self):
        """
        TODO: Document (adjust)

        This screen is accessed immediately after the loading screen, hence it will have a lot of start-up
        functionalities. Currently the following are implemented:

            1. Display the menu bar (and the line break) as it should only be disabled in the loading screen.
            2. Start the connection check clock
        """
        super().on_switch()
        self.manager.bar.setVisible(True)
        self.manager.line_break.setVisible(True)
        self.manager.references.connection_clock.start()

        self._hardware_readings_clock.start()
        self._connection_readings_clock.start()

        self.manager.references.main_camera.frame_received.connect(self._update_main_camera)
        self.manager.references.top_camera.frame_received.connect(self._update_top_camera)
        self.manager.references.bottom_camera.frame_received.connect(self._update_bottom_camera)

    def on_exit(self):
        """
        Stop the clocks.
        """
        super().on_exit()
        self._hardware_readings_clock.stop()
        self._connection_readings_clock.stop()

        self.manager.references.main_camera.frame_received.disconnect(self._update_main_camera)
        self.manager.references.top_camera.frame_received.disconnect(self._update_top_camera)
        self.manager.references.bottom_camera.frame_received.disconnect(self._update_bottom_camera)

    @Slot(QPixmap)
    def _update_main_camera(self, frame):
        """
        Update main camera's frame.
        """
        Log.debug("Updating main, forward-facing camera")
        frame = frame.scaled(min(self._main_camera.width(), frame.width()),
                             min(self._main_camera.height(), frame.height()),
                             aspectMode=Qt.KeepAspectRatio, mode=Qt.SmoothTransformation)
        self._main_camera.setPixmap(frame)

    @Slot(QPixmap)
    def _update_top_camera(self, frame):
        """
        Update top camera's frame.
        """
        Log.debug("Updating top-facing camera")
        frame = frame.scaled(min(self._top_camera.width(), frame.width()),
                             min(self._top_camera.height(), frame.height()),
                             aspectMode=Qt.KeepAspectRatio, mode=Qt.SmoothTransformation)
        self._top_camera.setPixmap(frame)

    @Slot(QPixmap)
    def _update_bottom_camera(self, frame):
        """
        Update bottom camera's frame.
        """
        Log.debug("Updating bottom-facing camera")
        frame = frame.scaled(min(self._bottom_camera.width(), frame.width()),
                             min(self._bottom_camera.height(), frame.height()),
                             aspectMode=Qt.KeepAspectRatio, mode=Qt.SmoothTransformation)
        self._bottom_camera.setPixmap(frame)