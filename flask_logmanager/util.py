import json
import flask

from .models.error_model import ErrorModel

class Error(Exception, ErrorModel):
    
    def __init__(self, status=400, title=None, type=None,
                      instance=None, headers=None, key=None):
        Exception.__init__(self)
        ErrorModel.__init__(self, status, type, title, key, instance)
        self._key = key
        self.headers = headers

    def __str__(self):
        return self._key

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


