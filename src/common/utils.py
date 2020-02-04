"""
Common Utils
============

Standard utils module storing common to the package classes, functions, constants, and other objects.
"""
import os as _os
import psutil as _psutil

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


def get_processes():
    # TODO need to use the defined MASTER PID, not the current pid (won't return
    # all processes if current is child)
    currentPid = _os.getpid()
    processList = [currentPid]

    currentProcess = _psutil.Process(currentPid)

    children = currentProcess.children(recursive=True)
    for child in children:
        processList.append(child.pid)

    return processList


def get_threads(processes):
    """TODO: document """

    processThreads = {}

    for process in processes:
        processThreads[process] = _psutil.Process(process).num_threads()

    return processThreads


def get_cpu_load(processes):
    """TODO: document"""

    processCPULoad = {}

    for process in processes:
        p = _psutil.Process(process)
        p.cpu_percent(interval=None)
        processCPULoad[process] = p.cpu_percent(interval=None)

    return processCPULoad


def get_total_memory(processes):
    """TODO: document"""

    totalRAM = 0

    for process in processes:
        memoryInfo = _psutil.Process(process).memory_info()
        totalRAM = totalRAM + memoryInfo.rss + memoryInfo.vms

    return totalRAM / (1024.0 * 1024.0)
