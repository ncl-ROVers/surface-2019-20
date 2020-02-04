"""
Hardware File Handler
=======================

TODO document
"""
import logging as _logging
import os as _os
import psutil as _psutil
from src.common.utils import *

class _HardwareFileHandler(_logging.FileHandler):
    """
    TODO document
    """

    def __init__(self, filename, *args, **kwargs):
        _logging.FileHandler.__init__(self, filename, *args, **kwargs)

    def emit(self, record):
        """
        TODO document
        """
        
        processes = get_processes()
        record.processesDict = get_threads(processes)
        record.numProcesses = len(record.processesDict)
        record.processesCPULoad = get_cpu_load(processes)
        record.totalMemory = get_total_memory(processes)

        _logging.FileHandler.emit(self, record)
