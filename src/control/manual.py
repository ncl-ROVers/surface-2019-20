"""
TODO: Document
"""
from ..common import data_manager as _dm, Log as _Log
from .utils import normalise as _normalise, DrivingMode as _DrivingMode
import multiprocessing as _mp
import inputs as _inputs
import time as _time


# Initialise the controller, has to be a global variable due to multiprocessing
_controller = _inputs.devices.gamepads[0] if _inputs.devices.gamepads else None

# Create the hardware to class value dispatcher
_dispatch_map = {
    "ABS_X": "left_axis_x",
    "ABS_Y": "left_axis_y",
    "ABS_RX": "right_axis_x",
    "ABS_RY": "right_axis_y",
    "ABS_Z": "left_trigger",
    "ABS_RZ": "right_trigger",
    "ABS_HAT0X": "hat_x",
    "ABS_HAT0Y": "hat_y",
    "BTN_SOUTH": "button_A",
    "BTN_EAST": "button_B",
    "BTN_WEST": "button_X",
    "BTN_NORTH": "button_Y",
    "BTN_TL": "button_LB",
    "BTN_TR": "button_RB",
    "BTN_THUMBL": "button_left_stick",
    "BTN_THUMBR": "button_right_stick",
    "BTN_START": "button_select",
    "BTN_SELECT": "button_start"
}

# Declare the max and min values - the hardware and the expected ones
_HARDWARE_AXIS_MAX = 32767
_HARDWARE_AXIS_MIN = -32768
_HARDWARE_TRIGGER_MAX = 255
_HARDWARE_TRIGGER_MIN = 0
_INTENDED_AXIS_MAX = 1
_INTENDED_AXIS_MIN = -1
_INTENDED_TRIGGER_MAX = 1
_INTENDED_TRIGGER_MIN = 0


def _normalise_axis(value: float) -> float:
    """
    TODO: Document, helper function
    :param value:
    :raises: ValueError
    :return:
    """
    if not (_HARDWARE_AXIS_MAX >= value >= _HARDWARE_AXIS_MIN):
        raise ValueError(f"Value {value} is not be between {_HARDWARE_AXIS_MIN} and {_HARDWARE_AXIS_MAX}")
    else:
        return _normalise(value, _HARDWARE_AXIS_MIN, _HARDWARE_AXIS_MAX, _INTENDED_AXIS_MIN, _INTENDED_AXIS_MAX)


def _normalise_trigger(value: float) -> float:
    """
    TODO: Document, helper function
    :param value:
    :raises: ValueError
    :return:
    """
    if not (_HARDWARE_TRIGGER_MAX >= value >= _HARDWARE_TRIGGER_MIN):
        raise ValueError(f"Value {value} is not be between {_HARDWARE_TRIGGER_MIN} and {_HARDWARE_TRIGGER_MAX}")
    else:
        return _normalise(value, _HARDWARE_TRIGGER_MIN, _HARDWARE_TRIGGER_MAX,
                          _INTENDED_TRIGGER_MIN, _INTENDED_TRIGGER_MAX)


class Controller:
    """
    TODO: Document
    """

    def __init__(self):
        """
        TODO: Document
        """

        # Stop the initialisation early if failed to recognise the controller
        if not _controller:
            _Log.error("No game controllers detected")
            return

        self._process = _mp.Process(target=self._read, name="Controller")
        self._mode = _DrivingMode.MANUAL
        self._delay = 0.01
        self._data = {
            "mode": 0,
            "yaw": 0,
            "pitch": 0,
            "roll": 0,
            "sway": 0,
            "surge": 0,
            "heave": 0,
        }

        # Initialise the axis
        self._left_axis_x = 0
        self._left_axis_y = 0
        self._right_axis_x = 0
        self._right_axis_y = 0

        # Initialise the triggers
        self._left_trigger = 0
        self._right_trigger = 0

        # Initialise the hat
        self._hat_y = 0
        self._hat_x = 0

        # Initialise the buttons
        self.button_A = False
        self.button_B = False
        self.button_X = False
        self.button_Y = False
        self.button_LB = False
        self.button_RB = False
        self.button_left_stick = False
        self.button_right_stick = False
        self._button_select = False
        self._button_start = False

    def __bool__(self):
        return _controller is not None

    @property
    def left_axis_x(self):
        return self._left_axis_x

    @left_axis_x.setter
    def left_axis_x(self, value):
        self._left_axis_x = _normalise_axis(value)

    @property
    def left_axis_y(self):
        return self._left_axis_y

    @left_axis_y.setter
    def left_axis_y(self, value):
        self._left_axis_y = _normalise_axis(value)

    @property
    def right_axis_x(self):
        return self._right_axis_x

    @right_axis_x.setter
    def right_axis_x(self, value):
        self._right_axis_x = _normalise_axis(value)

    @property
    def right_axis_y(self):
        return self._right_axis_y

    @right_axis_y.setter
    def right_axis_y(self, value):
        self._right_axis_y = _normalise_axis(value)

    @property
    def left_trigger(self):
        return self._left_trigger

    @left_trigger.setter
    def left_trigger(self, value):
        self._left_trigger = _normalise_trigger(value)

    @property
    def right_trigger(self):
        return self._right_trigger

    @right_trigger.setter
    def right_trigger(self, value):
        self._right_trigger = _normalise_trigger(value)

    @property
    def hat_x(self):
        return self._hat_x

    @hat_x.setter
    def hat_x(self, value):
        self._hat_x = value

    @property
    def hat_y(self):
        return self._hat_y

    @hat_y.setter
    def hat_y(self, value):
        self._hat_y = value * (-1)

    @property
    def button_start(self):
        return self._button_start

    @button_start.setter
    def button_start(self, value):
        self._button_start = bool(value)
        if value:
            try:
                # noinspection PyTypeChecker
                self._mode = _DrivingMode(self._mode.value + 1)
            except ValueError:
                self._mode = _DrivingMode(0)

    @property
    def button_select(self):
        return self._button_select

    @button_select.setter
    def button_select(self, value):
        self._button_select = bool(value)
        if value:
            try:
                # noinspection PyTypeChecker
                self._mode = _DrivingMode(self._mode.value - 1)
            except ValueError:
                self._mode = _DrivingMode(len(_DrivingMode.__members__) - 1)

    @property
    def mode(self):
        return self._mode

    @property
    def yaw(self):
        if self.right_trigger:
            return self.right_trigger
        elif self.left_trigger:
            return -self.left_trigger
        else:
            return 0

    @property
    def pitch(self):
        return self.right_axis_y

    @property
    def roll(self):
        if self.button_B:
            return 1
        elif self.button_X:
            return -1
        else:
            return 0

    @property
    def sway(self):
        return self._right_axis_x

    @property
    def surge(self):
        return self.left_axis_y

    @property
    def heave(self):
        if self.button_RB:
            return 1
        elif self.button_LB:
            return -1
        else:
            return 0

    def _dispatch_event(self, event: _inputs.InputEvent):
        """
        TODO: Document
        :param event:
        :return:
        """
        # Ignore syncing events
        if event.code == "SYN_REPORT":
            return

        if event.code in _dispatch_map:
            self.__setattr__(_dispatch_map[event.code], event.state)
            self._update()
        else:
            _Log.error(f"Event not registered in the dispatch map - {event.code}")

    def _next_data(self) -> dict:
        return {k: self.__getattribute__(k) for k in self._data}

    def _update(self):
        """
        TODO: Document
        :return:
        """

        # When entering the autonomous driving mode, reset the manual control values
        if self._mode == _DrivingMode.AUTONOMOUS:
            data = {k: (_DrivingMode.AUTONOMOUS if k == "mode" else 0) for k in self._data}
        else:
            data = self._next_data()

        # Calculate the data differences and override the data to check for differences next time
        difference = {k: v for k, v in data.items() if v != self._data[k]}
        self._data = data

        for k, v in difference.items():
            if k == "mode":
                _dm.control["mode"] = v.value
            else:
                _dm.control["manual_" + k] = v

    def _read(self):
        """
        TODO: Document
        :return:
        """
        while True:
            self._dispatch_event(_controller.read()[0])
            _time.sleep(self._delay)

    def start(self) -> int:
        """
        TODO: Document
        :return:
        """

        if not _controller:
            _Log.error("Can not start - no game controllers detected")
            return -1
        else:
            self._process.start()
            _Log.info("Controller reading process started, pid {}".format(self._process.pid))
            return self._process.pid
