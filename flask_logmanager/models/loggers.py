# coding: utf-8
from flask_logmanager import loggerDict, loggingLevel
from .logger import Logger
from ..util import NotFoundLoggerError, NotAddLoggerError

class Loggers(list):
    """
    Loggers - manage list of logger
    """
    def __init__(self):
        list.__init__(self)
        for id in loggerDict:
            list.append(self, Logger(id=id))

    def append(self, el):
        raise NotAddLoggerError()
    
    def getLogger(self, id):
        for logger in self:
            if logger.id == id:
                return logger
        raise NotFoundLoggerError(id)        

