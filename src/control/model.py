"""
Control Model
=============

Module storing an implementation of the control model.

The `ControlManager` class is the implementation of a closed loop control system for the ROV, with the readings
from both the manual and the autonomous modes.

The normalised values are then converted to the ranges expected by hardware and pushed as transmission data.
"""
from .utils import DrivingMode as _DrivingMode, normalise as _normalise, \
    NORM_IDLE as _IDLE, NORM_MAX as _MAX, NORM_MIN as _MIN
from ..common import data_manager as _dm, CONTROL_DICT as _CONTROL_DICT, Log as _Log
import multiprocessing as _mp
import time as _time


# Declare the hardware-specific max and min values
_THRUSTER_MAX = 1900
_THRUSTER_MIN = 1100


def _normalise_thruster(value: float) -> int:
    """
    Helper function used to normalise the common range into hardware-specific ranges.

    :param value: Value to be normalised
    :raises: ValueError
    :return: Normalised value
    """
    return int(_normalise(value, _MIN, _MAX, _THRUSTER_MIN, _THRUSTER_MAX))


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
        _Log.debug("Pulling data for the control model")
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
        _Log.debug("Merging control model data")

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
        _Log.debug("Pushing control model data (updating transmission data)")
        _dm.transmission.update(self._convert())

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

    def _convert(self) -> dict:
        """
        Method used to convert normalised direction ranges into actual hardware values used to control the ROV.

        Each inner function corresponds to a component on the vehicle.

        :return: Dictionary of values to update the data manager with
        """
        # Retrieve the values as variable for convenience
        yaw = self._data["yaw"]
        pitch = self._data["pitch"]
        roll = self._data["roll"]
        sway = self._data["sway"]
        surge = self._data["surge"]
        heave = self._data["heave"]

        def _thruster_hfp() -> int:
            """
            Hierarchical control for horizontal fore port thruster.

            :return: Value between _THURSTER_MAX and _THRUSTER_MIN
            """
            if surge and yaw:

                # If backwards, else forwards
                if surge < _IDLE:
                    value = -surge
                else:
                    value = -yaw

            elif surge:
                value = -surge

            elif sway:
                value = sway

            elif yaw:
                value = -yaw

            else:
                value = _IDLE

            return _normalise_thruster(value)

        def _thruster_hfs() -> int:
            """
            Hierarchical control for horizontal fore starboard thruster.

            :return: Value between _THURSTER_MAX and _THRUSTER_MIN
            """
            if surge and yaw:

                # If backwards, else forwards
                if surge < _IDLE:
                    value = -surge
                else:
                    value = yaw

            elif surge:
                value = -surge

            elif sway:
                value = -sway

            elif yaw:
                value = yaw

            else:
                value = _IDLE

            return _normalise_thruster(value)

        def _thruster_hap() -> int:
            """
            Hierarchical control for horizontal aft port thruster.

            :return: Value between _THURSTER_MAX and _THRUSTER_MIN
            """
            if surge and yaw:
                # If backwards, else forwards
                if surge < _IDLE:
                    value = -yaw
                else:
                    value = surge

            elif surge:
                value = surge

            elif sway:
                value = sway

            elif yaw:
                value = yaw

            else:
                value = _IDLE

            return _normalise_thruster(value)

        def _thruster_has() -> int:
            """
            Hierarchical control for vertical aft starboard thruster.

            :return: Value between _THURSTER_MAX and _THRUSTER_MIN
            """
            if surge and yaw:

                # If backwards, else forwards
                if surge < _IDLE:
                    value = yaw
                else:
                    value = surge

            elif surge:
                value = surge

            elif sway:
                value = -sway

            elif yaw:
                value = -yaw

            else:
                value = _IDLE

            return _normalise_thruster(value)

        def _thruster_vfp() -> int:
            """
            Hierarchical control for vertical fore port thruster.

            :return: Value between _THURSTER_MAX and _THRUSTER_MIN
            """
            if heave:
                value = heave

            elif pitch:
                value = -pitch

            elif roll:
                value = roll

            else:
                value = _IDLE

            return _normalise_thruster(value)

        def _thruster_vfs() -> int:
            """
            Hierarchical control for vertical fore starboard thruster.

            :return: Value between _THURSTER_MAX and _THRUSTER_MIN
            """
            if heave:
                value = heave

            elif pitch:
                value = -pitch

            elif roll:
                value = -roll

            else:
                value = _IDLE

            return _normalise_thruster(value)

        def _thruster_vap() -> int:
            """
            Hierarchical control for vertical aft port thruster.

            :return: Value between _THURSTER_MAX and _THRUSTER_MIN
            """
            if heave:
                value = heave

            elif pitch:
                value = pitch

            elif roll:
                value = roll

            else:
                value = _IDLE

            return _normalise_thruster(value)

        def _thruster_vas() -> int:
            """
            Hierarchical control for vertical aft starboard thruster.

            :return: Value between _THURSTER_MAX and _THRUSTER_MIN
            """
            if heave:
                value = heave

            elif pitch:
                value = pitch

            elif roll:
                value = -roll

            else:
                value = _IDLE

            return _normalise_thruster(value)

            # Build the dictionary of values and return it

        return {
            "T_HFP": _thruster_hfp(),
            "T_HFS": _thruster_hfs(),
            "T_HAP": _thruster_hap(),
            "T_HAS": _thruster_has(),
            "T_VFP": _thruster_vfp(),
            "T_VFS": _thruster_vfs(),
            "T_VAP": _thruster_vap(),
            "T_VAS": _thruster_vas(),
        }

    def start(self):
        """
        Method used to start the updates in a separate process.

        :return: Process id
        """
        self._process.start()
        _Log.info("Control manager process started, pid {}".format(self._process.pid))
        return self._process.pid
