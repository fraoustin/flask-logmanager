#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Module flask_logmanager
"""

__version_info__ = (0, 1, 0)
__version__ = '.'.join([str(val) for val in __version_info__])

__namepkg__ = "flask-logmanager"
__desc__ = "Flask LogManager module"
__urlpkg__ = "https://github.com/fraoustin/flask-logmanager.git"
__entry_points__ = {}

from flask_logmanager.main import *
