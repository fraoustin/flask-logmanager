#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_logmanager import Logger, getLogger, DEBUG
from os.path import join, dirname
from flask import Blueprint, current_app, send_from_directory, redirect, request, send_file
from flask_logmanager.controllers.logger_controller import get_loggers, get_logger, set_logger

def static_web_index():
    return send_from_directory(join(dirname(__file__),'swagger-ui'),"index.html")

def static_web(filename):
    if filename == "index.html":
        return redirect(request.url[:-1 * len('index.html')])
    if filename == "swagger.yaml":
        swagger = open(join(dirname(__file__),'swagger-ui','swagger.yaml'),'r').read()
        swagger = swagger.replace('$host$', "%s:%s" % (request.environ['SERVER_NAME'], request.environ['SERVER_PORT']) )
        swagger = swagger.replace('$path$', [current_app.blueprints[i] for i in current_app.blueprints if current_app.blueprints[i].__class__.__name__ == 'LogManager'][0].url_prefix )
        return swagger
    return send_from_directory(join(dirname(__file__),'swagger-ui'),filename)

def get_logger_by_rule(rule):
    for logger in Logger.manager.loggerDict:
        try:
            if getLogger(logger)._rule == rule:
                return getLogger(logger)
        except:
            pass
    return current_app.logger

def debug(msg, *args, **kwargs):  
    Logger.debug(get_logger_by_rule(request.url_rule.rule), msg, *args, **kwargs)

def info(msg, *args, **kwargs):  
    Logger.info(get_logger_by_rule(request.url_rule.rule), msg, *args, **kwargs)

def warning(msg, *args, **kwargs):  
    Logger.warning(get_logger_by_rule(request.url_rule.rule), msg, *args, **kwargs)

def error(msg, *args, **kwargs):  
    Logger.error(get_logger_by_rule(request.url_rule.rule), msg, *args, **kwargs)

def critical(msg, *args, **kwargs):  
    Logger.critical(get_logger_by_rule(request.url_rule.rule), msg, *args, **kwargs)

def addHandler(hl):
    for logger in Logger.manager.loggerDict:
        try:
            if getLogger(logger)._rule == rule:
                getLogger(logger).addHandler(hl)
        except:
            pass
    return Logger.addHandler(hl) 

class LogManager(Blueprint):

    def __init__(self, name='logmanager', import_name=__name__, ui_testing=False, url_prefix="", by_rule=True, level=None, *args, **kwargs):
        Blueprint.__init__(self, name, import_name, url_prefix=url_prefix, *args, **kwargs)
        self._level = level
        self.add_url_rule('/loggers', 'get_loggers', get_loggers, methods=['GET'])
        self.add_url_rule('/logger/<loggerId>', 'get_logger', get_logger, methods=['GET'])
        self.add_url_rule('/logger/<loggerId>', 'set_logger', set_logger, methods=['PUT'])
        if ui_testing:
            self.add_url_rule('/ui/<path:filename>', 'static_web', static_web)
            self.add_url_rule('/ui/', 'static_web_index', static_web_index)
        if by_rule:
            self.before_app_first_request(self._add_dynamics_logger)

    def _add_dynamics_logger(self):
        current_app.logger.debug('start init of logManager')
        #reset level of logger
        current_app.logger.debug('reset level of logger')
        if not self._level:
            levels = [current_app.logger.getEffectiveLevel(),]
            levels = levels + [h.level for h in current_app.logger.handlers]
            self._level = max(levels)
        current_app.logger.setLevel(self._level)
        for h in current_app.logger.handlers:
            h.setLevel(DEBUG)
        #dynamic logger
        current_app.logger.debug('add dynamic logger')
        no = 0
        for rule in current_app.url_map.iter_rules():
            current_app.logger.debug(rule.rule)
            l = getLogger("logManager-%s" % no)
            l.setLevel(current_app.logger.level)
            l._rule = rule.rule
            for h in current_app.logger.handlers:
                l.addHandler(h)
            no = no +1    
        #change current_app.logger
        current_app.logger.debug = debug
        current_app.logger.info = info
        current_app.logger.critical = critical
        current_app.logger.warning = warning
        current_app.logger.error = error
        current_app.logger.addHandler = addHandler
        current_app.logger.debug('end init of LogManager')

    @property
    def endpoints(self):
        return ["%s.%s" % (self.name, i) for i in ['get_loggers','get_logger','set_logger']]
