from .process_update import Read_Data
from PySide2.QtCore import QTimer

"""
The process management file, add the process here
"""

_CLOCK = 500  # The clock


class Process_On:
    def __init__(self, home):
        self.home = home
        self.read_data = Read_Data(self.home)
        self.clock = QTimer()
        self.clock.setInterval(_CLOCK)

    def start(self):
        self.clock.timeout.connect(self.on_process)
        self.clock.start()

    def on_process(self):
        """
        The processes
        """
        self.read_data.on_process()
