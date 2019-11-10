"""
Common
======

Shared functions, classes, constants and other objects.

.. moduleauthor::
    Kacper Florianski <k.florianski@ncl.ac.uk>
"""

from .statics import *
from .utils import *
from .logger import *
from . import data_manager as dm
# TODO: Remove test sample
print(dm.transmission["test_t2"])
dm.transmission["test_t2"] = 12
print(dm.transmission["test_t2"])
