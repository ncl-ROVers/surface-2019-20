"""
Manual Control
==============

Module storing an implementation of a controller and values associated with it.

The `Controller` class is the implementation of a closed loop control system for the ROV, with the hardware readings
executed in separate process. The readings are forwarded to the shared memory in a previously agreed format.
"""
from ..common import data_manager as _dm, Log as _Log
from .utils import DrivingMode as _DrivingMode, normalise as _normalise, \
    NORM_IDLE as _IDLE, NORM_MAX as _MAX, NORM_MIN as _MIN
import multiprocessing as _mp
import inputs as _inputs
import time as _time


# Initialise the controller, has to be a global variable due to multiprocessing
_CONTROLLER = _inputs.devices.gamepads[0] if _inputs.devices.gamepads else None

# Create the hardware to class value dispatcher
_DISPATCH_MAP = {
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
_INTENDED_AXIS_MAX = _MAX
_INTENDED_AXIS_MIN = _MIN
_INTENDED_TRIGGER_MAX = _MAX
_INTENDED_TRIGGER_MIN = _IDLE


def _normalise_axis(value: float) -> float:
    """
    Helper function used to normalise the controller axis values into a common range.

    :param value: Value to be normalised
    :raises: ValueError
    :return: Normalised value
    """
    return _normalise(value, _HARDWARE_AXIS_MIN, _HARDWARE_AXIS_MAX, _INTENDED_AXIS_MIN, _INTENDED_AXIS_MAX)


def _normalise_trigger(value: float) -> float:
    """
    Helper function used to normalise the controller trigger values into a common range.

    :param value: Value to be normalised
    :raises: ValueError
    :return: Normalised value
    """
    return _normalise(value, _HARDWARE_TRIGGER_MIN, _HARDWARE_TRIGGER_MAX, _INTENDED_TRIGGER_MIN, _INTENDED_TRIGGER_MAX)


class Controller:
    """
    Controller used to handle manual control systems.

    Uses the global `_CONTROLLER` reference to interact with hardware.

    Functions
    ---------

    The following list shortly summarises each function:

        * __init__ - standard constructor, returns early if the global `_CONTROLLER` reference is invalid
        * __bool__ - standard thruthness method, returns state of the global `_CONTROLLER` reference
        * _dispatch_event - a method to update the controller's state using hardware readings
        * state - a getter to get the current state of the controller
        * _update - a method to update the shared memory
        * _read - a wrapper method to execute everything in a separate process
        * start - a method to start the controller readings

    Controller mappings
    -------------------

    The following list shortly summarises each property (apart from state) within the class:

    Axis
    ++++
        - left_axis_x
        - left_axis_y
        - right_axis_x
        - right_axis_y

    Triggers
    ++++++++
        - left_trigger
        - right_trigger

    Hat
    +++
        - hat_y
        - hat_x

    Buttons
    +++++++
        - button_A
        - button_B
        - button_X
        - button_Y
        - button_LB
        - button_RB
        - button_left_stick
        - button_right_stick
        - button_select
        - button_start

    Model values
    ++++++++++++
        - mode
        - yaw
        - pitch
        - roll
        - sway
        - surge
        - heave

    Usage
    -----

    After creating an instance of the class, `start` method will either return a process ID of the started process, or
    -1 if the controller wasn't initialised correctly.
    """

    def __init__(self):
        """
        Constructor method used to initialise all fields or return early if no controller devices were detected.

        Most fields are internal values used by the class, however the `_delay` should be adjusted to modify
        the frequency of hardware readings.
        """

        # Stop the initialisation early if failed to recognise the controller
        if not _CONTROLLER:
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
        return _CONTROLLER is not None

    @property
    def state(self) -> dict:
        """
        Getter function used to fetch all (normalised) degrees of freedom in a dictionary format.

        :return: Dictionary with normalised degrees of freedom
        """
        return {k: self.__getattribute__(k) for k in self._data}

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
        """
        Setter which selects next driving mode (wrapping)

        :param value: State of the button
        """
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
        """
        Setter which selects next previous mode (wrapping)

        :param value: State of the button
        """
        self._button_select = bool(value)
        if value:
            try:
                # noinspection PyTypeChecker
                self._mode = _DrivingMode(self._mode.value - 1)
            except ValueError:
                self._mode = _DrivingMode(len(_DrivingMode.__members__) - 1)

    @property
    def mode(self) -> _DrivingMode:
        """
        Getter for the driving mode. Must be one of the `DrivingMode`-s defined in the statics module.

        :return: Current driving mode
        """
        return self._mode

    @property
    def yaw(self) -> float:
        """
        Yaw is determined by both triggers.

        :return: -1.0 for full port turn, 1.0 for full starboard turn
        """
        if self.right_trigger:
            return self.right_trigger
        elif self.left_trigger:
            return -self.left_trigger
        else:
            return 0

    @property
    def pitch(self) -> float:
        """
        Pitch is determined by the vertical right axis.

        :return: 1.0 for full bow pitch, -1.0 for full stern pitch
        """
        return self.right_axis_y

    @property
    def roll(self) -> float:
        """
        Roll is determined by the buttons X and B.

        :return: -1.0 for full port roll, 1.0 for full starboard roll, 0 otherwise
        """
        if self.button_B:
            return 1.0
        elif self.button_X:
            return -1.0
        else:
            return 0

    @property
    def sway(self) -> float:
        """
        Sway is determined by the horizontal right axis.

        :return: -1.0 for full port sway, 1.0 for full starboard sway
        """
        return self._right_axis_x

    @property
    def surge(self) -> float:
        """
        Surge is determined by the vertical left axis.

        :return: 1.0 for full foreward surge, -1.0 for full aft surge
        """
        return self.left_axis_y

    @property
    def heave(self) -> float:
        """
        Heave is determined by the buttons RB and LB.

        :return: 1.0 for full up heave, -1.0 for full down heave, 0 otherwise
        """
        if self.button_RB:
            return 1.0
        elif self.button_LB:
            return -1.0
        else:
            return 0

    def _dispatch_event(self, event: _inputs.InputEvent):
        """
        Dispatcher method used to update the controller's state with the hardware readings.

        :param event: Hardware reading event
        """
        # Ignore syncing events
        if event.code == "SYN_REPORT":
            return

        if event.code in _DISPATCH_MAP:
            self.__setattr__(_DISPATCH_MAP[event.code], event.state)
            self._update()
        else:
            _Log.error(f"Event not registered in the dispatch map - {event.code}")

    def _update(self):
        """
        Method used to update the shared memory controller data using the current controller's state.
        """

        # When entering the autonomous driving mode, reset the manual control values
        if self._mode == _DrivingMode.AUTONOMOUS:
            data = {k: (_DrivingMode.AUTONOMOUS if k == "mode" else 0) for k in self._data}
        else:
            data = self.state

        # Calculate the data differences and override the data to check for differences next time
        difference = {"manual_" + k: v for k, v in data.items() if v != self._data[k]}
        self._data = data

        # Make sure the mode is using a correct key and a correct value
        if "manual_mode" in difference:
            difference["mode"] = difference.pop("manual_mode").value

        # Finally update the data manager with a collection of values
        _dm.control.update(difference)

    def _read(self):
        """
        Wrapper method used as a target for the process spawning.
        """
        while True:
            self._dispatch_event(_CONTROLLER.read()[0])
            _time.sleep(self._delay)

    def start(self) -> int:
        """
        Method used to start the hardware readings in a separate process.

        :return: -1 on errors or process id
        """
        if not _CONTROLLER:
            _Log.error("Can not start - no game controllers detected")
            return -1
        else:
            self._process.start()
            _Log.info("Controller reading process started, pid {}".format(self._process.pid))
            return self._process.pid
