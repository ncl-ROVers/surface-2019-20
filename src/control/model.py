"""
Control Model
=============

Module storing an implementation of the control model.

The `ControlManager` class is the implementation of a closed loop control system for the ROV, with the readings
from both the manual and the autonomous modes.

The normalised values are then converted to the ranges expected by hardware and pushed as transmission data.
"""
from .utils import DrivingMode as _DrivingMode
from ..common import data_manager as _dm, CONTROL_DICT as _CONTROL_DICT, Log as _Log
import multiprocessing as _mp
import time as _time


class ControlManager:
    """
    Control managed used to decide which values should be transmitted to the PI based on the readings from manual
    and autonomous data.

    The process of getting the final values is as follows:

    1. Pull the readings from manual and autonomous control systems.
    2. Merge the readings depending on the driving mode.
    3. Translate the merged readings into proper hardware values.
    4. Push the final values to the shared memory as transmission data.

    .. note::
        The final readings are always sub-ranges between -1 to 1 inclusive. Some example ranges are <-1, 1>, <0, 1>.
        It is up to the translation code to convert them to values understood by the ROV's hardware.

    Functions
    ---------

    The following list shortly summarises each function:

        * __init__ - standard constructor
        * _pull - a method to get the data from manual and autonomous control systems
        * _merge - a method to merge both control systems
        * _push - a method to convert the values into the final format and update shared memory
        * _update - a wrapper method to execute everything in a separate process
        * start - a method to start the control model's calculations

    Usage
    -----

    After creating an instance of the class, `start` method will return a process ID of the started process.
    """

    def __init__(self):
        """
        Standard constructor.
        """
        self._process = _mp.Process(target=self._update)
        self._mode = _DrivingMode.MANUAL
        self._delay = 0.01

        # Initialise separate dictionaries for each type of control data
        self._manual_data = dict()
        self._autonomous_data = dict()

        # Initialise the data dictionary which will be used in conversion to the final, expected hardware values.
        self._data = dict()

    def _pull(self):
        """
        Method used to fetch control data.

        Dispatches each 'manual_' and 'autonomous_' key, value pairs into corresponding dictionaries, and the 'mode' key
        into a private field.
        """
        data = _dm.control.get_all()

        for key in _CONTROL_DICT:
            if key.startswith("manual_"):
                self._manual_data[key.replace("manual_", "")] = data[key]
            elif key.startswith("autonomous_"):
                self._autonomous_data[key.replace("autonomous_", "")] = data[key]
            elif key == "mode":
                self._mode = _DrivingMode(data[key])
            else:
                raise KeyError(f"Unexpected key retrieved - {key}, must be either \"mode\" or prefixed with"
                               "\"manual_\" or \"autonomous_\"")

    def _merge(self):
        """
        Method used to merge the data depending on which driving mode is currently on.

        1. In manual, ignore autonomous data
        2. In autonomous, ignore manual data
        3. In balancing, manual has a higher priority than manual.
        """

        # Ignore autonomous data in manual control
        if self._mode == _DrivingMode.MANUAL:
            self._data = self._manual_data

        # Ignore manual data in autonomous control
        elif self._mode == _DrivingMode.AUTONOMOUS:
            self._data = self._autonomous_data

        # Otherwise in the balancing mode, manual steering is preferred
        else:
            self._data = {key: (self._manual_data[key] if self._manual_data[key] else self._autonomous_data[key])
                          for key in self._manual_data}

    def _push(self):
        """
        Method used to translate normalised values into the expected hardware ranges, and push to the data manager.
        """
        _dm.transmission.update(_convert(self._data))

    def _update(self):
        """
        Wrapper method used as a target for the process spawning.

        Refer to the class documentation for more information on how the process of updating the data works.
        """
        while True:
            self._pull()
            self._merge()
            self._push()
            _time.sleep(self._delay)

    def start(self):
        """
        Method used to start the updates in a separate process.

        :return: Process id
        """
        self._process.start()
        _Log.info("Control manager process started, pid {}".format(self._process.pid))
        return self._process.pid


def _convert(data: dict) -> dict:
    """
    TODO: Write code in the same manner as the last year's hierarchy based control.
      Requires the actual values and ids to be known before writing it.

    TODO: Example::
        def thruster_ap():
            if surge and yaw:
                return normalise(yaw//2 + surge//2, ...)  <- possibly create helper normalise method (like in manual.py)
            elif surge:
                return normalise(surge, ...)
            elif yaw:
                return normalise(yaw, ...)
            else:
                return normalise(sway, ...)

    TODO: Consider moving this function elsewhere, for example into the ControlManager

    :param data: Values to convert into hardware-expected ranges
    :return: Dictionary of values to update the data manager with
    """
    return dict()
