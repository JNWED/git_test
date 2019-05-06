"""
server module
"""
# -*- coding:utf-8 -*-
import time
import subprocess
from common.share import kill_with_port
from common.log import Log


class Server():
    def __init__(self, deviceobject):
        '''
        Server init
        '''
        self.logger = Log.logger
        self._deviceobject = deviceobject
        self._cmd = "appium -p %s -bp %s -U %s --session-override\
        " % (self._deviceobject[1].serverPort, self._deviceobject[1].bootstrapPort,
             self._deviceobject[1].deviceUdid)

    def start(self):
        '''
        Start Server
        '''
        self.kill(self._deviceobject[1].serverPort)
        time.sleep(3)
        info = "Start devices:%s Appium Server" % self._deviceobject[1].deviceName
        self.logger.info(info)
        self.logger.info(self._cmd)
        subprocess.call(self._cmd, shell=True)

    def stop(self):
        '''
        Stop Server
        '''
        self.kill(self._deviceobject[1].serverPort)

    def kill(self, port):
        '''
        Kill server
        '''
        kill_with_port(port)

    def list_connect_devices(self):
        '''
        List connect devices
        '''
        info = "Connected dev:%s ------ %s" % (
            self._deviceobject[1].deviceUdid, self._deviceobject[1].deviceName)
        self.logger.info(info)
