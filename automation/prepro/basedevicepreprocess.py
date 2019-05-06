# -*- coding:utf-8 -*-

from appium.webdriver.common.touch_action import TouchAction


class BaseDevicePreProcess(object):

    def __init__(self, tester):
        self.tester = tester
        self.driver = self.tester.driver
        self.action = TouchAction(self.driver)
        self.user = self.tester.user

    def pre_process(self):
        driver = self.tester.driver

    def install_app(self):
        pass

    def upgrade_app(self):
        pass

    def install_process(self):
        pass

    def login_process(self):
        pass

    def login_success_process(self):
        pass

    def get_permission_process(self):
        pass

    def data_prepare(self):
        pass
