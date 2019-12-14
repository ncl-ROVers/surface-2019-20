"""
Common Utils
============

Standard utils module storing common to the package classes, functions, constants, and other objects.
"""
import os as _os

# Declare path to the root folder (surface)
ROOT_DIR = _os.path.normpath(_os.path.join(_os.path.dirname(__file__), "..", ".."))

# Declare paths to the main folders
ASSETS_DIR = _os.path.join(ROOT_DIR, "assets")
SRC_DIR = _os.path.join(ROOT_DIR, "src")
LOG_DIR = _os.path.join(ROOT_DIR, "log")

# Declare the paths to the source paths
SRC_COMMON_DIR = _os.path.join(SRC_DIR, "common")
SRC_GUI_DIR = _os.path.join(SRC_DIR, "gui")
SRC_LOG_DIR = _os.path.join(SRC_DIR, "log")

# Declare the paths to the assets folders
GUI_LOADING_DIR = _os.path.join(ASSETS_DIR, "gui_loading")
COMMON_LOGGER_DIR = _os.path.join(ASSETS_DIR, "common_logger")
COMMON_LOCKS_DIR = _os.path.join(ASSETS_DIR, "common_locks")

# Declare shared memory data mappings
TRANSMISSION_DICT = {
    "placeholder": 0
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
