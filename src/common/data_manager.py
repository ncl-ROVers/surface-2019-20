"""
TODO: Document
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
    TODO: Document
    """

    def __init__(self, name: str, data: dict):
        """
        TODO: Document

        :param name:
        :param data:
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

    def __getitem__(self, item: str):
        """
        TODO: Document

        :param item:
        :raises: KeyError
        :return:
        """
        # Raise error early if key not registered
        if item not in self._lookup:
            raise KeyError(f"{item} not found - remember to add the key to the data manager!")

        self._lock.acquire()
        value = self._shm[self._lookup[item]]
        self._lock.release()
        return value

    def __setitem__(self, key: str, value):
        """
        TODO: Document

        :param key:
        :param value:
        :return:
        """
        # Raise error early if key not registered
        if key not in self._lookup:
            raise KeyError(f"{key} not found - remember to add the key to the data manager!")

        self._lock.acquire()
        self._shm[self._lookup[key]] = value
        self._lock.release()


class _DataManager:
    """
    TODO: Document
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
