# -*- coding:utf-8 -*-
import sys
import time
from common.basetestcase import BaseTestCase

sys.path.append('../..')


class TestLogin(BaseTestCase):

    @classmethod
    def setUpClass(cls):#类方法cls
                        #setUpClass在所有case执行之前准备一次环境，并在所有case执行结束之后再清理环境
        pass

    def setUp(self):#测试环境的搭建，每执行一个用例自动执行一次
        self.tester.logger.info("Device: %s Start case: %s" % (
            self.tester.device.deviceName, self._testMethodName))
        time.sleep(5)

    def logout(self):
        '''logout function
        '''
        self.tester.find_element_by_id_and_tap(
            'com.netease.cloudmusic:id/mainDrawerIcon')
        time.sleep(1)
        if self.tester.is_element_exist('com.netease.cloudmusic:id/drawerUserName'):
            time.sleep(1)
            #logout at first
            self.tester.find_element_by_id_and_tap(
                'com.netease.cloudmusic:id/drawerSetting')
            time.sleep(2)
            self.tester.swipe_down_bottom()
            self.tester.find_element_by_id_and_tap(
                'com.netease.cloudmusic:id/pfLogout')
            self.tester.find_element_by_id_and_tap(
                'com.netease.cloudmusic:id/buttonDefaultPositive')
            if self.tester.is_element_exist("立即登录"):
                self.tester.logger.info(
                "Device: %s User logout" % (self.tester.device.deviceName))
                return True
            else:
                self.tester.logger.error(
                "Device: %s User failed to logout" % (self.tester.device.deviceName))
                return False
        else:
            return True

    def login_email(self):
        '''login with email
        '''
        if (self.tester.is_element_exist("立即登录")):
            self.find_element_by_uiautomator_and_tap(
                'new UiSelector().text("立即登录")')
        time.sleep(1)
        self.tester.find_element_by_id_and_tap(
            'com.netease.cloudmusic:id/mail')
        self.tester.find_element_by_id_and_send_keys(
            'com.netease.cloudmusic:id/email', self.tester.user.email)
        self.tester.find_element_by_id_and_send_keys(
            'com.netease.cloudmusic:id/password', self.tester.user.epassword)
        self.tester.find_element_by_id_and_tap(
            'com.netease.cloudmusic:id/login')

    def test_login_00_email(self):
        '''
        login in with email
        '''
        # app站内登录--邮箱登录
        self.logout()
        time.sleep(1)
        self.login_email()
        self.tester.find_element_by_id_and_tap(
            'com.netease.cloudmusic:id/mainDrawerIcon')
        username = self.tester.driver.find_element_by_id(
            'com.netease.cloudmusic:id/drawerUserName')
        self.assertIsNotNone(username, msg="邮箱登录失败")
        self.tester.logger.info(
                "设备: %s 邮箱登录成功" % (self.tester.device.deviceName))

    def test_login_02_mobilphone(self):

        # app站内登录--手机号登录
        self.skipTest("skip mobilphone login at first")
        self.tester.find_element_by_id_and_tap(
            'com.netease.cloudmusic:id/mainDrawerIcon')
        time.sleep(1)
        if self.tester.is_element_exist('com.netease.cloudmusic:id/drawerUserName'):
            time.sleep(1)
            self.tester.driver.back()

            # driver.back()返回上一页
            # driver.forward()去下一页
            # driver.refresh()刷新

            time.sleep(2)
            self.login_01_anonymous()
            self.tester.find_element_by_id_and_tap(
                'com.netease.cloudmusic:id/mainDrawerIcon')
        self.tester.find_element_by_id_and_tap(
            'com.netease.cloudmusic:id/drawerAnonymousHeaderLogin')
        self.tester.driver.find_element_by_android_uiautomator(
            'new UiSelector().text("手机号登录")').click()
        self.tester.find_element_by_id_and_send_keys(
            'com.netease.cloudmusic:id/phoneNumber', self.tester.user.mobile)
        self.tester.find_element_by_id_and_send_keys(
            'com.netease.cloudmusic:id/password', self.tester.user.mpassword)
        self.tester.find_element_by_id_and_tap(
            'com.netease.cloudmusic:id/login')
        self.tester.find_element_by_id_and_tap(
            'com.netease.cloudmusic:id/mainDrawerIcon')
        try:
            nikename = self.tester.driver.find_element_by_id(
                'com.netease.cloudmusic:id/drawerUserName')
            nikename_rel = "七七七"
            self.assertIsNotNone(nikename, msg="手机号登录失败")
            self.assertEqual(nikename.text, nikename_rel, "账号与登录账号不一致")
            self.tester.logger.info(
                "设备: %s %s 账号登录成功" % (self.tester.device.deviceName, nikename.text))
        except Exception:
            self.tester.logger.info(
                "设备: %s 登录异常" % (self.tester.device.deviceName))
            self.fail("phonenum login fail")


    def tearDown(self):#测试环境的还原，每执行一个用例自动执行一次
        self.tester.addfailscreenshot(self._testMethodName)
        self.tester.back_to_start()

    @classmethod
    def tearDownClass(cls):
        pass
