import json
from flask import request
from flask_logmanager.models.error_model import ErrorModel
from flask_logmanager.models.logger import Logger
from flask_logmanager.models.loggers import Loggers 
from ..util import NotFoundLoggerError, NotAddLoggerError, Error, to_json

@to_json
def get_logger(loggerId):
    """
    Find logger by ID
    Returns a logger
    :param loggerId: ID of logger that needs to be fetched
    :type loggerId: str

    :rtype: Logger
    """
    return Loggers().getLogger(loggerId).to_dict()


   

@to_json
def get_loggers():
    """
    list of logger
    Returns list of logger

    :rtype: List[Logger]
    """
    logs = [logger for logger in Loggers()]
    logs.sort()
    return [ logger.to_dict() for logger in logs ]


@to_json
def set_logger(loggerId):
    """
    Updates a logger with form data
    update logger by Id
    :param loggerId: ID of logger that needs to be updated
    :type loggerId: str
    :param body: Logger object that needs to be updated
    :type body: dict | bytes

    :rtype: None
    """
    data = json.loads(request.data.decode())
    if loggerId != data['id']:
        raise Error(status=405, title='invalid INPUT', type='RG-003', detail='loggerId is not compatible with logger object')
    try:
        Logger().from_dict(data)
    except ValueError as err:
        raise Error(status=405, title='invalid INPUT', type='RG-004', detail=str(err))
    return data
