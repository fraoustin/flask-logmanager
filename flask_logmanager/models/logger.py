# coding: utf-8
from flask_logmanager import loggingLevel, getLogger, loggerDict
from .base_model_ import Model
from ..util import NotFoundLoggerError



class Logger(Model):
    def __init__(self, id=None, level=None, rule=None):
        """
        Logger 

        :param id: The id of this Logger.
        :type id: str
        :param level: The level of this Logger.
        :type level: str
        """
        self._level = level
        self._rule = rule
        # if get id, i check and search value from logging module
        if id:
            self.id = id
        else:
            self._id = id

    @property
    def id(self):
        """
        Gets the id of this Logger.
        id of logger

        :return: The id of this Logger.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this Logger.
        id of logger

        :param id: The id of this Logger.
        :type id: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")
        if id not in loggerDict:
            raise NotFoundLoggerError(id)
        self._id = id
        if self._level:
            self.level = self._level
        else:
            self.level = loggingLevel[getLogger(id).level]
        if self._rule:
            self.rule = self._rule
        else:
            self.rule =  '_rule' in getLogger(id).__dict__ and getLogger(id)._rule or None

    @property
    def level(self):
        """
        Gets the level of this Logger.
        level of logger

        :return: The level of this Logger.
        :rtype: str
        """
        return self._level

    @level.setter
    def level(self, level):
        """
        Sets the level of this Logger.
        level of logger

        :param level: The level of this Logger.
        :type level: str
        """
        if level is None:
            raise ValueError("Invalid value for `level`, must not be `None`")
        if level not in loggingLevel.keys():
            raise ValueError("Invalid value for `level`, not list in %s" % ','.join(loggingLevel.keys()))
        if self.id is not None:
            getLogger(self.id).setLevel(loggingLevel[level])
        self._level = level    

    @property
    def rule(self):
        """
        Gets the rule of this Logger.
        rule of logger

        :return: The rule of this Logger.
        :rtype: str
        """
        return self._rule

    @rule.setter
    def rule(self, rule):
        """
        Sets the rule of this Logger.
        rule of logger

        :param rule: The rule of this Logger.
        :type rule: str
        """
        if self.id is not None:
            if '_rule' in getLogger(self.id).__dict__ and getLogger(self.id)._rule != rule:
                raise ValueError("Invalid value for `rule`, you can not change value of rule: %s" % getLogger(self.id)._rule)
            getLogger(self.id)._rule = rule
        self._rule = rule


    def __lt__(self, other):
        return self.id < other.id

    def __le__(self, other):
        return self.id <= other.id

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    def __gt__(self, other):
        return self.id > other.id

    def __ge__(self, other):
        return self.id >= other.id
        
