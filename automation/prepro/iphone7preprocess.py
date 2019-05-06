# -*- coding:utf-8 -*-

from basedevicepreprocess import BaseDevicePreProcess
from common.tester import Tester
from common.log import Log


class Iphone7PreProcess (BaseDevicePreProcess):

    def __init__(self, tester):
        super(Iphone7PreProcess, self).__init__(tester)

    def install_app(self):
        pass

    def pre_process(self):
        Log.logger.info(
            "Device: %s start prepare process..." %
            self.tester.device.deviceName)
        driver = self.tester.driver
        #TBF
        return True

    def install_process(self):
        pass
