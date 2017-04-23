# coding: utf-8
import logging
try:
    #python3
    from logging import _levelToName as loggingLevel
except:
    #python2
    from logging import _levelNames as loggingLevel
from .logger import Logger
from ..util import NotFoundLoggerError, NotAddLoggerError

class Loggers(list):
    """
    Loggers - manage list of logger
    """
    def __init__(self):
        list.__init__(self)
        for id in logging.Logger.manager.loggerDict:
            list.append(self, Logger(id=id))

    def append(self, el):
        raise NotAddLoggerError()
    
    def getLogger(self, id):
        for logger in self:
            if logger.id == id:
                return logger
        raise NotFoundLoggerError(id)        

