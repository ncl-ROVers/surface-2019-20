"""
Common Utils
============

Standard utils module storing common to the package classes, functions, constants, and other objects.
"""
import os as _os
import psutil as _psutil
import GPUtil as _GPUtil
import typing as _typing

# Declare path to the root folder (surface)
ROOT_DIR = _os.path.normpath(_os.path.join(_os.path.dirname(__file__), "..", ".."))

# Declare paths to the main folders
ASSETS_DIR = _os.path.join(ROOT_DIR, "assets")
SRC_DIR = _os.path.join(ROOT_DIR, "src")
LOG_DIR = _os.path.join(ROOT_DIR, "log")

# Declare the paths to the source paths
SRC_COMMON_DIR = _os.path.join(SRC_DIR, "common")
SRC_GUI_DIR = _os.path.join(SRC_DIR, "gui")
SRC_CONTROL_DIR = _os.path.join(SRC_DIR, "control")

# Declare the paths to the assets folders
GUI_CONTROLLER_DIR = _os.path.join(ASSETS_DIR, "gui_controller")
GUI_LOADING_DIR = _os.path.join(ASSETS_DIR, "gui_loading")
COMMON_LOGGER_DIR = _os.path.join(ASSETS_DIR, "common_logger")
COMMON_LOCKS_DIR = _os.path.join(ASSETS_DIR, "common_locks")

# Declare shared memory data mappings
TRANSMISSION_DICT = {
    "T_HFP": 0,
    "T_HFS": 0,
    "T_HAP": 0,
    "T_HAS": 0,
    "T_VFP": 0,
    "T_VFS": 0,
    "T_VAP": 0,
    "T_VAS": 0
}
CONTROL_DICT = {
    "mode": 0,
    "manual_yaw": 0,
    "manual_pitch": 0,
    "manual_roll": 0,
    "manual_sway": 0,
    "manual_surge": 0,
    "manual_heave": 0,
    "autonomous_yaw": 0,
    "autonomous_pitch": 0,
    "autonomous_roll": 0,
    "autonomous_sway": 0,
    "autonomous_surge": 0,
    "autonomous_heave": 0
}
# TODO: Replace with proper data once known
RECEIVED_DICT = {
    "test": ""
}


def get_processes(pid: int) -> _typing.List[_typing.Type[_psutil.Process]]:
    """
    TODO: Document

    :param pid:
    :return:
    """
    parent = _psutil.Process(pid)

    return [parent] + parent.children(recursive=True)


def count_threads(processes: list) -> int:
    """
    TODO: Document

    :param processes:
    :return:
    """
    return sum(process.num_threads() for process in processes)


def get_cpu_load() -> float:
    """
    TODO: Document

    :param processes:
    :return:
    """
    return _psutil.cpu_percent()


def get_memory_usage() -> float:
    """
    TODO: Document

    :return:
    """
    return _psutil.virtual_memory().percent


def get_gpu_load():
    """
    TODO: Document

    :return:
    """
    return sum(gpu.load for gpu in _GPUtil.getGPUs()) * 100


def get_hardware(pid: int) -> _typing.Tuple[int, int, float, float, float]:
    """
    TODO: Document

    :param pid:
    :return:
    """
    processes = get_processes(pid)
    num_processes = len(processes)
    num_threads = count_threads(processes)

    return num_processes, num_threads, get_cpu_load(), get_memory_usage(), get_gpu_load()
