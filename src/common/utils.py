"""
Common Utils
============

Standard utils module storing common to the package classes, functions, constants, and other objects.
"""
import os as _os
import psutil as _psutil
import GPUtil as _GPUtil

# Declare path to the root folder (surface)
ROOT_DIR = _os.path.normpath(_os.path.join(_os.path.dirname(__file__), "..", ".."))

# Declare paths to the main folders
ASSETS_DIR = _os.path.join(ROOT_DIR, "assets")
SRC_DIR = _os.path.join(ROOT_DIR, "src")
LOG_DIR = _os.path.join(ROOT_DIR, "log")
TESTS_DIR = _os.path.join(ROOT_DIR, "tests")

# Declare the paths to the source paths
SRC_COMMON_DIR = _os.path.join(SRC_DIR, "common")
SRC_GUI_DIR = _os.path.join(SRC_DIR, "gui")
SRC_CONTROL_DIR = _os.path.join(SRC_DIR, "control")

# Declare the paths to the assets folders
GUI_LOADING_DIR = _os.path.join(ASSETS_DIR, "gui_loading")
COMMON_LOGGER_DIR = _os.path.join(ASSETS_DIR, "common_logger")
COMMON_LOCKS_DIR = _os.path.join(ASSETS_DIR, "common_locks")
TESTS_ASSETS_DIR = _os.path.join(TESTS_DIR, "assets")

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


def _get_processes():
    # TODO need to use the defined MASTER PID, not the current pid (won't return
    # all processes if current is child -- put into _References in src/gui/utils.py ?)
    current_pid = _os.getpid()
    process_list = [current_pid]

    current_process = _psutil.Process(current_pid)

    children = current_process.children(recursive=True)
    for child in children:
        process_list.append(child.pid)

    return process_list


def _get_threads(processes):
    """TODO: document """
    process_threads = {}

    for process in processes:
        process_threads[process] = _psutil.Process(process).num_threads()

    return process_threads


def _get_cpu_load(processes):
    """TODO: document"""
    process_cpu_load = {}

    for process in processes:
        p = _psutil.Process(process)
        p.cpu_percent(interval=None)
        process_cpu_load[process] = p.cpu_percent(interval=None)

    return process_cpu_load


def _get_total_memory(processes):
    """TODO: document"""
    total_memory = 0

    for process in processes:
        memory_info = _psutil.Process(process).memory_info()
        total_memory += (memory_info.rss + memory_info.vms)

    # return the amount in megabytes
    return total_memory / (1024.0 * 1024.0)


def _get_gpu_info():
    """TODO: document"""
    load = 0
    total_memory = 0
    gpus = _GPUtil.getGPUs()

    for gpu in gpus:
        load += gpu.load
        total_memory += gpu.memoryUsed
    return load, total_memory


def get_hardware():
    """TODO document"""
    processes = _get_processes()
    process_dict = _get_threads(processes)
    num_processes = len(process_dict)
    processes_cpu_load = _get_cpu_load(processes)
    total_memory = _get_total_memory(processes)
    gpu_info = _get_gpu_info()

    return str(process_dict), str(num_processes), str(processes_cpu_load), str(total_memory), str(gpu_info)
