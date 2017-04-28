# coding: utf-8

from .base_model_ import Model


class ErrorModel(Model):
    
    def __init__(self, status=None, type=None, title=None, detail=None, instance=None):
        """
        ErrorModel

        :param status: The status of this ErrorModel.
        :type status: int
        :param type: The type of this ErrorModel.
        :type type: str
        :param title: The title of this ErrorModel.
        :type title: str
        :param detail: The detail of this ErrorModel.
        :type detail: str
        :param instance: The instance of this ErrorModel.
        :type instance: str
        """
        self._status = status
        self._type = type
        self._title = title
        self._detail = detail
        self._instance = instance

    @property
    def status(self):
        """
        Gets the status of this ErrorModel.

        :return: The status of this ErrorModel.
        :rtype: int
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this ErrorModel.

        :param status: The status of this ErrorModel.
        :type status: int
        """

        self._status = status

    @property
    def type(self):
        """
        Gets the type of this ErrorModel.

        :return: The type of this ErrorModel.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this ErrorModel.

        :param type: The type of this ErrorModel.
        :type type: str
        """

        self._type = type

    @property
    def title(self):
        """
        Gets the title of this ErrorModel.

        :return: The title of this ErrorModel.
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """
        Sets the title of this ErrorModel.

        :param title: The title of this ErrorModel.
        :type title: str
        """

        self._title = title

    @property
    def detail(self):
        """
        Gets the detail of this ErrorModel.

        :return: The detail of this ErrorModel.
        :rtype: str
        """
        return self._detail

    @detail.setter
    def detail(self, detail):
        """
        Sets the detail of this ErrorModel.

        :param detail: The detail of this ErrorModel.
        :type detail: str
        """

        self._detail = detail

    @property
    def instance(self):
        """
        Gets the instance of this ErrorModel.

        :return: The instance of this ErrorModel.
        :rtype: str
        """
        return self._instance

    @instance.setter
    def instance(self, instance):
        """
        Sets the instance of this ErrorModel.

        :param instance: The instance of this ErrorModel.
        :type instance: str
        """

        self._instance = instance

