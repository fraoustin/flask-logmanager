#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from os.path import join, dirname
from flask import Blueprint, current_app, send_from_directory, redirect, request, send_file
from flask_logmanager.controllers.logger_controller import get_loggers, get_logger, set_logger

def static_web_index():
    return send_from_directory(join(dirname(__file__),'swagger-ui'),"index.html")



def static_web(filename):
    if filename == "index.html":
        return redirect(request.url[:-1 * len('index.html')])
    return send_from_directory(join(dirname(__file__),'swagger-ui'),filename)


class LoggerByRule(logging.Logger):

    def __init__(self, name, level):
        logging.Logger.__init__(self, name, level)

    def debug(self, msg, *args, **kwargs):  
        try:
            if request.url_rule.rule.replace('/','>') in logging.Logger.manager.loggerDict: 
                logging.getLogger(request.url_rule.rule.replace('/','>')).debug(msg, *args, **kwargs)
            else:
                raise Exception('logger not found')
        except:
            logging.Logger.debug(self, msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):  
        try:
            if request.url_rule.rule.replace('/','>') in logging.Logger.manager.loggerDict: 
                logging.getLogger(request.url_rule.rule.replace('/','>')).info(msg, *args, **kwargs)
            else:
                raise Exception('logger not found')
        except:
            logging.Logger.info(self, msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):  
        try:
            if request.url_rule.rule.replace('/','>') in logging.Logger.manager.loggerDict: 
                logging.getLogger(request.url_rule.rule.replace('/','>')).warning(msg, *args, **kwargs)
            else:
                raise Exception('logger not found')
        except:
            logging.Logger.warning(self, msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):  
        try:
            if request.url_rule.rule.replace('/','>') in logging.Logger.manager.loggerDict: 
                logging.getLogger(request.url_rule.rule.replace('/','>')).error(msg, *args, **kwargs)
            else:
                raise Exception('logger not found')
        except:
            logging.Logger.error(self, msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):  
        try:
            if request.url_rule.rule.replace('/','>') in logging.Logger.manager.loggerDict: 
                logging.getLogger(request.url_rule.rule.replace('/','>')).critical(msg, *args, **kwargs)
            else:
                raise Exception('logger not found')
        except:
            logging.Logger.critical(self, msg, *args, **kwargs)

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
        #reset level of logger
        current_app.logger.debug('reset level of logger')
        levels = [current_app.logger.getEffectiveLevel(),]
        levels = levels + [h.level for h in current_app.logger.handlers]
        effectiveLevel = max(levels)
        current_app.logger.setLevel(effectiveLevel)
        for h in current_app.logger.handlers:
            h.setLevel(logging.DEBUG)
        #dynamic logger
        current_app.logger.debug('add dynamic logger')
        for rule in current_app.url_map.iter_rules():
            current_app.logger.debug(rule.rule)
            l = logging.getLogger(rule.rule.replace('/','>'))
            l.setLevel(current_app.logger.level)
            for h in current_app.logger.handlers:
                l.addHandler(h)
        #change current_app.logger
        logger_by_rule = LoggerByRule(current_app.logger.name, current_app.logger.level)
        for h in current_app.logger.handlers:
            logger_by_rule.addHandler(h)
        logging.Logger.manager.loggerDict[current_app.logger.name]=logger_by_rule
        current_app._logger=logger_by_rule


