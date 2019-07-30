#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Module flask_logmanager
"""

__version_info__ = (0, 2, 11)
__version__ = '.'.join([str(val) for val in __version_info__])

__namepkg__ = "flask-logmanager"
__desc__ = "Flask LogManager module"
__urlpkg__ = "https://github.com/fraoustin/flask-logmanager.git"
__entry_points__ = {}

from logging import Logger, getLogger, DEBUG
try:
    #python3
    from logging import _nameToLevel, _levelToName
    loggingLevel = _nameToLevel
    for k in _levelToName:
        loggingLevel[k] = _levelToName[k]
except:
    #python2
    from logging import _levelNames as loggingLevel
from logging import getLogger, Logger
loggerDict = Logger.manager.loggerDict

from flask_logmanager.main import *
