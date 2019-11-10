"""
TODO: Document
"""
import sys as _sys
import multiprocessing as _mp
from multiprocessing import shared_memory as _shm
from ..common import Log

# Declare names and key: default value pairs for different chunks of shared memory
_TRANSMISSION_NAME = "transmission"
_TRANSMISSION_DICT = {
    "test_t1": 3,
    "test_t2": "oink"
}
_CONTROL_NAME = "control"
_CONTROL_DICT = {
    "test_c": "hello"
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

        # Create a shared memory object to store the data
        self._shm = _shm.ShareableList(tuple(v for v in data.values()), name=name)
        Log.debug(f"Successfully created shared memory \"{name}\" with a total of {len(data)} keys")

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


# Override the module to be the class object instead
if not isinstance(_sys.modules[__name__], _DataManager):
    _sys.modules[__name__] = _DataManager()
