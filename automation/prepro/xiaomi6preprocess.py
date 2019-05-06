# -*- coding:utf-8 -*-

from basedevicepreprocess import BaseDevicePreProcess
from common.tester import Tester
from common.log import Log


class Xiaomi6PreProcess (BaseDevicePreProcess):

    def __init__(self, tester):
        super(Xiaomi6PreProcess, self).__init__(tester)

    def install_app(self):
        pass

    def pre_process(self):
        Log.logger.info(
            "Device: %s start prepare process..." % 
            self.tester.device.deviceName)
        driver = self.tester.driver
        try:
            concel = "取消"
            box_8 = self.tester.find_element_by_uiautomator(
                'new UiSelector().text("{}")'.format(concel))
            if box_8:
                self.tester.find_element_by_uiautomator_and_tap(
                    'new UiSelector().text("{}")'.format(concel))
            login_or_register = self.tester.find_element_by_id('com.netease.cloudmusic:id/loginOrRegister', 10)
            use_now = self.tester.find_element_by_id('com.netease.cloudmusic:id/useNow', 10)
            if login_or_register or use_now:
                self.tester.find_element_by_id_and_tap('com.netease.cloudmusic:id/loginOrRegister')
                # app站内登录--手机号登录
                self.tester.find_element_by_id_and_tap(
                    'com.netease.cloudmusic:id/mail')
                self.tester.find_element_by_id_and_send_keys(
                    'com.netease.cloudmusic:id/email', self.tester.user.email)
                self.tester.find_element_by_id_and_send_keys(
                    'com.netease.cloudmusic:id/password', self.tester.user.epassword)
                self.tester.find_element_by_id_and_tap(
                    'com.netease.cloudmusic:id/login')
            else:
                self.tester.logger.info(
                    "设备: %s 设备可能已经登录状态" % self.tester.device.deviceName)

            #Wait for stable UI after login or app start
            self.tester.wait_for_stable_main_page(10)

            # Grant necessary rom permission in pre process
            Log.logger.info(
                "Device: %s start grant necessary permission before run testcase..." %
                self.tester.device.deviceName)
            if '_' in self.tester.device.deviceName:
                brand = self.tester.device.deviceName.split('_')[0].lower()
                self.tester.grant_contants_access_ahead(brand)
            else:
                Log.logger.error(
                "Device: %s current deviceName non-compliance with rule" %
                self.tester.device.deviceName)
            Log.logger.info(
                "Device: %s End grant necessary permission before run testcase..." %
                self.tester.device.deviceName)
        except:
            self.tester.logger.info(
                "设备: %s 设备启动异常" % self.tester.device.deviceName)  
        
    def install_process(self):
        pass
