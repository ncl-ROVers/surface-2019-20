"""
Data manager
============

Module storing an implementation of a data manager, exposing some common values via shared memory. Gets replaced with an
instance of the manager on import.

.. note::

    Remember to adjust the module constants to register values in shared memory.
"""

import sys as _sys
import os as _os
from multiprocessing import shared_memory as _shm
from .logger import Log as _Log
from .utils import TRANSMISSION_DICT as _TRANSMISSION_DICT, CONTROL_DICT as _CONTROL_DICT, \
    COMMON_LOCKS_DIR as _LOCKS_DIR, RECEIVED_DICT as _RECEIVED_DICT
from filelock import FileLock as _FileLock

# Declare shared memory names
_TRANSMISSION_NAME = "transmission"
_RECEIVED_NAME = "received"
_CONTROL_NAME = "control"


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
        * update - a setter controlling access to multiple items at once, using a dictionary

    Usage
    -----

    You should access the memory by calling the `__getitem__` and `__setitem__` methods::

        memory_obj["key"] = "value"
    """

    def __init__(self, name: str, data: dict, lock):
        """
        Standard constructor.

        Builds a shared memory object or fetches it if it already exists.

        :param name: Name of the memory object
        :param data: Dictionary of values to store
        :param lock: Named lock instance
        """
        self._name = name
        self._data = data
        self._lock = lock

        # Create a mapping dictionary which remembers positions of keys for faster access
        self._lookup = {k: i for i, k in enumerate(data)}

        # Create a shared memory object to store the data or fetch the existing one
        try:
            self._shm = _shm.ShareableList(tuple(v for v in data.values()), name=name)
            _Log.info(f"Successfully created shared memory \"{name}\" with a total of {len(data)} keys")
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
        _Log.debug(f"Getting {key} from {self._name} shared memory")

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
        _Log.debug(f"Setting {key} to {value} in {self._name} shared memory")

        # Raise error early if key not registered
        if key not in self._lookup:
            raise KeyError(f"{key} not found - remember to add the key to the data manager!")

        self._lock.acquire()
        self._shm[self._lookup[key]] = value
        self._lock.release()

    def get_all(self) -> dict:
        """
        Function used to read multiple data entries in shared memory, and return them as a dictionary.

        :return: Dictionary of stored values
        """
        _Log.debug(f"Getting all data from {self._name} shared memory")

        self._lock.acquire()
        data = {key: self._shm[self._lookup[key]] for key in self._data}
        self._lock.release()
        return data

    def update(self, data: dict):
        """
        Function used to modify multiple data entries in shared memory, using a dictionary

        :param data: Data to update
        :raises: KeyError
        """
        _Log.debug(f"Updating {self._name} shared memory with multiple entries")

        # Raise error early if any keys are not registered
        if not set(data.keys()).issubset(set(self._data.keys())):
            raise KeyError(f"{set(data.keys())} is not a subset of {set(self._data.keys())}")

        self._lock.acquire()
        for key, value in data.items():
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
        Standard constructor

        Fetches or creates the locks and the memory segments.
        """
        # Create or fetch named locks
        self._transmission_lock = _FileLock(_os.path.join(_LOCKS_DIR, _TRANSMISSION_NAME + ".lock"))
        self._control_lock = _FileLock(_os.path.join(_LOCKS_DIR, _CONTROL_NAME + ".lock"))
        self._received_lock = _FileLock(_os.path.join(_LOCKS_DIR, _RECEIVED_NAME + ".lock"))

        # Create shared memory objects to store the data, these will be read-only exposed via class properties
        self._transmission = _Memory(_TRANSMISSION_NAME, _TRANSMISSION_DICT, self._transmission_lock)
        self._control = _Memory(_CONTROL_NAME, _CONTROL_DICT, self._control_lock)
        self._received = _Memory(_RECEIVED_NAME, _RECEIVED_DICT, self._received_lock)

    @property
    def transmission(self) -> _Memory:
        """
        Getter for the transmission memory segment (data to transmit)

        :return: Transmission memory segment
        """
        return self._transmission

    @property
    def received(self) -> _Memory:
        """
        Getter for the received (data) memory segment

        :return: Received memory segment
        """
        return self._received

    @property
    def control(self) -> _Memory:
        """
        Getter for the control memory segment

        :return: Control memory segment
        """
        return self._control


# Create some type hinting variables for PyInspections
transmission: _Memory
control: _Memory
received: _Memory


# Override the module to be the class object instead
if not isinstance(_sys.modules[__name__], _DataManager):
    _sys.modules[__name__] = _DataManager()
