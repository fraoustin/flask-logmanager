import json
import flask

from .models.error_model import ErrorModel

class Error(Exception, ErrorModel):
    
    def __init__(self, status=400, title=None, type=None,
                      instance=None, headers=None, detail=None):
        Exception.__init__(self)
        ErrorModel.__init__(self, status, type, title, detail, instance)
        self._detail = detail
        self.headers = headers

    def __str__(self):
        return self._detail

    def to_problem(self):
        flask.current_app.logger.error("{url} {type} {error}".format(url=flask.request.url, 
                                                        type=self.type,
                                                        error=self.__str__()))
        problem_response = {'type': self.type, 
                            'title': self.title, 
                            'detail': self.detail, 
                            'status': self.status,
                            'instance': self.instance }
        body = [json.dumps(problem_response, indent=2), '\n']
        response = flask.current_app.response_class(body, mimetype='application/problem+json',
                                                                 status=self.status)  # type: flask.Response
        if self.headers:
            response.headers.extend(headers)
        return response

class NotFoundLoggerError(Error):

    def __init__(self, detail=""):
        Error.__init__(self,
            status=404,
            title="Not Found Logger",
            type="RG-001",
            detail=detail)

    def __str__(self):
        return "%s logger not found" % self._detail

class NotAddLoggerError(Error):

    def __init__(self):
        Error.__init__(self,
            status=404,
            title="Not Add Logger",
            type="RG-002",
            detail="")

    def __str__(self):
        return "not logger add"

def to_json(fn):
    def _request_fn(*args, **kw):
        try:
            fn_exec = fn(*args, **kw)
            return json.dumps(fn_exec, sort_keys=True, indent=4, separators=(',', ': '))
        except Error as e:
            return e.to_problem()
        else:
            return Error(status=500, title='Error System', type='UNKNOW', detail=e.__str__()).to_problem()   


    return _request_fn
