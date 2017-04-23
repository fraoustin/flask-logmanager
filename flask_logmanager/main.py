#!/usr/bin/env python
# -*- coding: utf-8 -*-

from logging import Logger, getLogger, DEBUG
from os.path import join, dirname
from flask import Blueprint, current_app, send_from_directory, redirect, request, send_file
from flask_logmanager.controllers.logger_controller import get_loggers, get_logger, set_logger

def static_web_index():
    return send_from_directory(join(dirname(__file__),'swagger-ui'),"index.html")



def static_web(filename):
    if filename == "index.html":
        return redirect(request.url[:-1 * len('index.html')])
    return send_from_directory(join(dirname(__file__),'swagger-ui'),filename)


class LoggerByRule(Logger):

    def __init__(self, name, level):
        Logger.__init__(self, name, level)
    
    def get_logger_by_rule(self, rule):
        for logger in Logger.manager.loggerDict:
            try:
                if getLogger(logger)._rule == rule:
                    return getLogger(logger)
            except:
                pass
        return getLogger()

    def debug(self, msg, *args, **kwargs):  
        self.get_logger_by_rule(request.url_rule.rule).debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):  
        self.get_logger_by_rule(request.url_rule.rule).info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):  
        self.get_logger_by_rule(request.url_rule.rule).warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):  
        self.get_logger_by_rule(request.url_rule.rule).error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):  
        self.get_logger_by_rule(request.url_rule.rule).critical(msg, *args, **kwargs)

class LogManager(Blueprint):

    def __init__(self, name='logmanager', import_name=__name__, ui_testing=False, by_rule=True, *args, **kwargs):
        Blueprint.__init__(self, name, import_name, *args, **kwargs)
        self.add_url_rule('/loggers', 'get_loggers', get_loggers, methods=['GET'])
        self.add_url_rule('/logger/<loggerId>', 'get_logger', get_logger, methods=['GET'])
        self.add_url_rule('/logger/<loggerId>', 'set_logger', set_logger, methods=['PUT'])
        if ui_testing:
            self.add_url_rule('/loggers/ui/<path:filename>', 'static_web', static_web)
            self.add_url_rule('/loggers/ui/', 'static_web_index', static_web_index)
        if by_rule:
            self.before_app_first_request(self._add_dynamics_logger)

    def _add_dynamics_logger(self):
        current_app.logger.debug('start init of logManager')
        #reset level of logger
        current_app.logger.debug('reset level of logger')
        levels = [current_app.logger.getEffectiveLevel(),]
        levels = levels + [h.level for h in current_app.logger.handlers]
        effectiveLevel = max(levels)
        current_app.logger.setLevel(effectiveLevel)
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
        logger_by_rule = LoggerByRule(current_app.logger.name, current_app.logger.level)
        for h in current_app.logger.handlers:
            logger_by_rule.addHandler(h)
        Logger.manager.loggerDict[current_app.logger.name]=logger_by_rule
        current_app._logger=logger_by_rule
        current_app.logger.debug('end init of LogManager')


