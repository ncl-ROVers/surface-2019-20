"""
TODO: Mention that degrees of freedom are expected to be in ranges - 0to1, -1to1 etc.
"""
from .statics import DrivingMode as _DrivingMode
from ..common import data_manager as _dm, CONTROL_DICT as _CONTROL_DICT, Log as _Log
import multiprocessing as _mp
import time as _time


class ControlManager:
    """
    TODO: Document
    """

    def __init__(self):
        self._process = _mp.Process(target=self._update)
        self._mode = _DrivingMode.MANUAL
        self._delay = 0.01

        # Initialise separate dictionaries for each type of control data
        self._manual_data = dict()
        self._autonomous_data = dict()
        self._data = dict()

    def _pull(self):
        for key in _CONTROL_DICT:
            if key.startswith("manual_"):
                self._manual_data[key.replace("manual_", "")] = _dm.control[key]
            elif key.startswith("autonomous_"):
                self._autonomous_data[key.replace("autonomous_", "")] = _dm.control[key]
            elif key == "mode":
                self._mode = _DrivingMode(_dm.control[key])

    def _merge(self):

        # Ignore autonomous data in manual control
        if self._mode == _DrivingMode.MANUAL:
            self._data = self._manual_data

        # Ignore manual data in autonomous control
        elif self._mode == _DrivingMode.AUTONOMOUS:
            self._data = self._autonomous_data

        # Otherwise in the balancing mode, manual steering
        else:
            self._data = {key: (self._manual_data[key] if self._manual_data[key] else self._autonomous_data[key])
                          for key in self._manual_data}

    def _push(self):
        for k, v in self._data.items():
            _dm.control[k] = v

    def _update(self):
        while True:
            self._pull()
            self._merge()
            self._push()
            _time.sleep(self._delay)

    def start(self):
        self._process.start()
        _Log.info("Control manager process started, pid {}".format(self._process.pid))
        return self._process.pid
