# coding: utf-8
try:
    #python3
    from logging import _nameToLevel as loggingLevel
except:
    #python2
    from logging import _levelNames as loggingLevel
from logging import getLogger

from .base_model_ import Model


class Logger(Model):
    def __init__(self, id=None, level=None):
        """
        Logger 

        :param id: The id of this Logger.
        :type id: str
        :param level: The level of this Logger.
        :type level: str
        """
        self._id = id
        self._level = level

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

        self._id = id

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
        
