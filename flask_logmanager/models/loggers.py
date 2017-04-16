# coding: utf-8
import logging
try:
    #python3
    from logging import _levelToName as loggingLevel
except:
    #python2
    from logging import _levelNames as loggingLevel
from .logger import Logger
from ..util import Error

class NotFoundLoggerError(Error):

    def __init__(self, key=""):
        Error.__init__(self,
            status=404,
            title="Not Found Logger",
            type="RG-001",
            key=key)

    def __str__(self):
        return "%s logger not found" % self._key

class NotAddLoggerError(Error):

    def __init__(self):
        Error.__init__(self,
            status=404,
            title="Not Add Logger",
            type="RG-002",
            key=key)

    def __str__(self):
        return "not logger add"



class Loggers(list):
    """
    Loggers - manage list of logger
    """
    def __init__(self):
        list.__init__(self)
        for id in logging.Logger.manager.loggerDict:
            list.append(self, Logger(id=id, level=loggingLevel[logging.getLogger(id).level]))    

    def append(self, el):
        raise NotAddLoggerError()
    
    def getLogger(self, id):
        for logger in self:
            if logger.id == id:
                return logger
        raise NotFoundLoggerError(id)        

