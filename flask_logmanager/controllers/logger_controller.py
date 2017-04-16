import json
from flask import request
from flask_logmanager.models.error_model import ErrorModel
from flask_logmanager.models.logger import Logger
from flask_logmanager.models.loggers import Loggers, NotFoundLoggerError, NotAddLoggerError 
from ..util import Error


def get_logger(loggerId):
    """
    Find logger by ID
    Returns a logger
    :param loggerId: ID of logger that needs to be fetched
    :type loggerId: str

    :rtype: Logger
    """
    try:
        return json.dumps(Loggers().getLogger(loggerId).to_dict())
    except NotFoundLoggerError as e:
        return e.to_problem()
    except NotAddLoggerError as e:
        return e.to_problem()
    else: 
        return Error(status=500, title='Error System', type='UNKNOW', value=e.__str__()).to_problem()   

    


def get_loggers():
    """
    list of logger
    Returns list of logger

    :rtype: List[Logger]
    """
    logs = [logger for logger in Loggers()]
    logs.sort()
    return json.dumps([ logger.to_dict() for logger in logs ])



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
    try:
        data = json.loads(request.data.decode())
        if loggerId != data['id']:
            return Error(status=405, title='invalid INPUT', type='RG-003', value='loggerId is not compatible with logger object').to_problem()
        body = Logger().from_dict(data)
        return json.dumps(data)
    except ValueError as e:
            return Error(status=405, title='invalid INPUT', type='RG-004', value='not json body').to_problem()
    except NotFoundLoggerError as e:
        return e.to_problem()
    except NotAddLoggerError as e:
        return e.to_problem()
    else: 
        return Error(status=500, title='Error System', type='UNKNOW', value=e.__str__()).to_problem()   
