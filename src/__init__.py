"""
Source code
===========

Package exposing packages, modules and other objects to the application's main. Remember to use relative path imports
when developing the code.

Each external package should be imported in the following way::

    from .. import package

Each module within the same package should be imported in the following way::

    from . import module
"""

from . import common
from . import gui
