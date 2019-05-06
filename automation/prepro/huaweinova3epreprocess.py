# -*- coding:utf-8 -*-

from basedevicepreprocess import BaseDevicePreProcess
from common.tester import Tester
from common.log import Log
import time


class HuaWeiNova3ePreProcess (BaseDevicePreProcess):

    def __init__(self, tester):
        super(HuaWeiNova3ePreProcess, self).__init__(tester)

    def install_app(self):
        #cmd = "adb -s %s install -r %s" % (self.tester.device.deviceid, DataProvider.niceapk)
        #subprocess.call(cmd, shell=True)
        pass

    def pre_process(self):
        Log.logger.info(
            "Device: %s start prepare process..." %
            self.tester.device.deviceName)
        time.sleep(10)
        login_or_register = self.tester.find_element_by_id(
            'com.netease.cloudmusic:id/loginOrRegister', 10)
        use_now = self.tester.find_element_by_id(
            'com.netease.cloudmusic:id/useNow', 10)
        email_login = self.tester.find_element_by_id(
            'com.netease.cloudmusic:id/mail', 10)
        if login_or_register or use_now or email_login:
            if(login_or_register):
                login_or_register.click()
                # need to check again!
                email_login = self.tester.find_element_by_id(
                    'com.netease.cloudmusic:id/mail', 10)
            if(email_login):
                email_login.click()
                # app站内登录--Email登录
                self.tester.find_element_by_id_and_send_keys(
                    'com.netease.cloudmusic:id/email', self.tester.user.email)
                self.tester.find_element_by_id_and_send_keys(
                    'com.netease.cloudmusic:id/password', self.tester.user.epassword)
                self.tester.find_element_by_id_and_tap(
                    'com.netease.cloudmusic:id/login')
        else:
            self.tester.logger.info(
                "设备: %s 设备可能已经登录状态" % self.tester.device.deviceName)

        # Wait for stable UI after login or app start
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

    def install_process(self):
        pass
