# -*- coding:utf-8 -*-


class Device(object):

    def __init__(self, deviceUdid):
        self._deviceUdid = deviceUdid
        self._deviceName = ""
        self._deviceStatus = ""
        self._platformVersion = ""
        self._platformName = ""
        self._bootstrapPort = ""
        self._serverPort = ""
        self._server = ""
        self._app = ""
        self._appPackage = ""
        self._appActivity = ""

    @property
    def deviceUdid(self):
        return self._deviceUdid

    @deviceUdid.setter
    def deviceUdid(self, value):
        self._deviceUdid = value

    @property
    def deviceName(self):
        return self._deviceName

    @deviceName.setter
    def deviceName(self, value):
        self._deviceName = value

    @property
    def deviceStatus(self):
        return self._deviceStatus

    @deviceStatus.setter
    def deviceStatus(self, value):
        self._deviceStatus = value

    @property
    def platformVersion(self):
        return self._platformVersion

    @platformVersion.setter
    def platformVersion(self, value):
        self._platformVersion = value

    @property
    def platformName(self):
        return self._platformName

    @platformName.setter
    def platformName(self, value):
        self._platformName = value

    @property
    def bootstrapPort(self):
        return self._bootstrapPort

    @bootstrapPort.setter
    def bootstrapPort(self, value):
        self._bootstrapPort = value

    @property
    def serverPort(self):
        return self._serverPort

    @serverPort.setter
    def serverPort(self, value):
        self._serverPort = value

    @property
    def server(self):
        return self._server

    @server.setter
    def server(self, value):
        self._server = value

    @property
    def app(self):
        return self._app

    @app.setter
    def app(self, value):
        self._app = value

    @property
    def appPackage(self):
        return self._appPackage

    @appPackage.setter
    def appPackage(self, value):
        self._appPackage = value

    @property
    def appActivity(self):
        return self._appActivity

    @appActivity.setter
    def appActivity(self, value):
        self._appActivity = value
