"""
Loading screen
==============

Module storing an implementation of a data manager, exposing some common values via shared memory. Gets replaced with an
instance of the manager on import.

.. note::

    Remember to adjust the module constants to register values in shared memory.
"""

import sys as _sys
import multiprocessing as _mp
from multiprocessing import shared_memory as _shm
from ..common import Log as _Log

# Declare names and key: default value pairs for different chunks of shared memory
_TRANSMISSION_NAME = "transmission"
_TRANSMISSION_DICT = {
    "placeholder": 0
}
_CONTROL_NAME = "control"
_CONTROL_DICT = {
    "mode": 0,
    "yaw": 0,
    "pitch": 0,
    "roll": 0,
    "sway": 0,
    "surge": 0,
    "heave": 0,
    "yaw_manual": 0,
    "pitch_manual": 0,
    "roll_manual": 0,
    "sway_manual": 0,
    "surge_manual": 0,
    "heave_manual": 0,
    "yaw_autonomous": 0,
    "pitch_autonomous": 0,
    "roll_autonomous": 0,
    "sway_autonomous": 0,
    "surge_autonomous": 0,
    "heave_autonomous": 0
}


class _Memory:
    """
    Class representing a shared memory segment.

    Provides a getter and a setter methods to modify the data indirectly.

    Functions
    ---------

    The following list shortly summarises each function:

        * __init__ - a constructor to create or fetch the shared memory objects
        * __getitem___ - a getter controlling access to the shared memory via locks
        * __getitem___ - a setter controlling access to the shared memory via locks

    Usage
    -----

    You should access the memory by calling the `__getitem__` and `__setitem__` methods::

        memory_obj["key"] = "value"
    """

    def __init__(self, name: str, data: dict):
        """
        Standard constructor.

        Builds a shared memory object or fetches it if it already exists.

        :param name: Name of the memory object
        :param data: Dictionary of values to store
        """
        self._name = name
        self._data = data
        self._lock = _mp.Lock()

        # Create a mapping dictionary which remembers positions of keys for faster access
        self._lookup = {k: i for i, k in enumerate(data)}

        # Create a shared memory object to store the data or fetch the existing one
        try:
            self._shm = _shm.ShareableList(tuple(v for v in data.values()), name=name)
            _Log.debug(f"Successfully created shared memory \"{name}\" with a total of {len(data)} keys")
        except FileExistsError:
            self._shm = _shm.ShareableList(name=name)

    def __getitem__(self, key: str):
        """
        Getter function to retrieve data from shared memory.

        Uses locks and the original dictionary passed in the constructor to safely access the data.

        :param key: Key to access
        :raises: KeyError
        :return: Value stored under the key
        """
        # Raise error early if key not registered
        if key not in self._lookup:
            raise KeyError(f"{key} not found - remember to add the key to the data manager!")

        self._lock.acquire()
        value = self._shm[self._lookup[key]]
        self._lock.release()
        return value

    def __setitem__(self, key: str, value):
        """
        Setter function to modify the data in shared memory.

        Uses locks and the original dictionary passed in the constructor to safely modify the data.

        :param key: Key to access
        :param value: Value to be inserted
        :raises: KeyError
        """
        # Raise error early if key not registered
        if key not in self._lookup:
            raise KeyError(f"{key} not found - remember to add the key to the data manager!")

        self._lock.acquire()
        self._shm[self._lookup[key]] = value
        self._lock.release()


class _DataManager:
    """
    Class representing a data manager which has access to all memory segments.

    Provides getter methods to each memory segment.

    ..warning::

        This module is replaced with an instance of this class on import.

    Functions
    ---------

    The following list shortly summarises each function:

        * __init__ - a constructor to create or fetch the shared memory objects
        * transmission - a getter controlling access to the transmission data shared memory
        * control - a setter controlling access to the control data shared memory

    Usage
    -----

    You should simply import the module and access the memory segments when needed::

        from ..common import data_manager as dm
        transmission = dm.transmission
        control = dm.control
    """

    def __init__(self):
        """
        TODO: Document
        """
        # Create shared memory objects to store the data, these will be read-only exposed via class properties
        self._transmission = _Memory(_TRANSMISSION_NAME, _TRANSMISSION_DICT)
        self._control = _Memory(_CONTROL_NAME, _CONTROL_DICT)

    @property
    def transmission(self):
        """
        TODO: Document
        :return:
        """
        return self._transmission

    @property
    def control(self):
        """
        TODO: Document

        :return:
        """
        return self._control


# Create some type hinting variables for PyInspections
transmission: _Memory
control: _Memory


# Override the module to be the class object instead
if not isinstance(_sys.modules[__name__], _DataManager):
    _sys.modules[__name__] = _DataManager()
