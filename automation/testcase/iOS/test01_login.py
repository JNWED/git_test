# -*- coding:utf-8 -*-
import sys
import time
from common.basetestcase import BaseTestCase
sys.path.append('../..')

experience = '//XCUIElementTypeButton[@name="立即体验"]'
allow = '//XCUIElementTypeButton[@name="允许"]'
account = '//XCUIElementTypeButton[@name="帐号"]'
login = '//XCUIElementTypeButton[@name="登录"]'
login_right_now = '//XCUIElementTypeButton[@name="立即登录"]'
login_by_iphone = '//XCUIElementTypeButton[@name="手机号登录"]'
email = '//XCUIElementTypeButton[@name="网易邮箱"]'


class TestLogin(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.tester.logger.info("Device: %s Start case: %s" % (
            self.tester.device.deviceName, self._testMethodName))
        time.sleep(4)

    def commom_ops(self):
        if self.tester.is_element_exist_ios('xpath', '//XCUIElementTypeStaticText[@name="私信"]'):
            self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="返回"]')
            time.sleep(2)
        else:
            pass
    '''
    匿名登录
    '''
    def test_login_01_Anonymously(self):
        if self.tester.is_element_exist_ios('xpath', experience):
            self.tester.find_element_by_xpath_and_click(experience)
        if self.tester.is_element_exist_ios('xpath', allow):
            self.tester.find_element_by_xpath_and_click(allow)
            time.sleep(1)
        self.tester.find_element_by_xpath_and_click(account)
        self.commom_ops()
        self.assertTrue(self.tester.is_element_exist_ios('xpath', '//XCUIElementTypeStaticText[@name="帐号"]') or
                        self.tester.is_element_exist_ios('xpath', '//XCUIElementTypeStaticText[@name="私信"]'), "匿名登陆失败")

    '''
    手机号登录
    '''
    def test_login_02_phone(self):
        self.skipTest("required phone_account")
        if self.tester.is_element_exist_ios('xpath', account):
            self.tester.find_element_by_xpath_and_click(account)
        if self.tester.is_element_exist_ios('xpath', login_right_now):
            self.tester.find_element_by_xpath_and_click(login_right_now)
            time.sleep(2)
            self.tester.find_element_by_xpath_and_click(login_by_iphone)
            time.sleep(1)
            self.tester.find_element_by_xpath_and_send_keys('//XCUIElementTypeTextField[@name="手机号输入"]',
                                                            self.tester.user.email, timeout=20)
            time.sleep(1)
            self.tester.find_element_by_xpath_and_send_keys('//XCUIElementTypeSecureTextField[@name="密码输入"]',
                                                            self.tester.user.epassword, timeout=20)
            time.sleep(1)
            self.tester.find_element_by_xpath_and_click(login)
        time.sleep(2)
        self.assertFalse(self.tester.is_element_exist_ios('xpath', login_right_now), "手机登录失败")
        self.tester.find_element_by_xpath_and_click(account)
        username = self.tester.driver.find_element_by_xpath('//XCUIElementTypeStaticText[@name="Shirly170511"]')
        self.assertIsNotNone(username, "设备: %s 登录信息不一致" % (self.tester.device.deviceName))
        self.tester.logger.info("设备: %s 登录账号一致" % (self.tester.device.deviceName))

    '''
    老账号登录(邮箱登录)
    '''
    def test_login_03_mailbox(self):
        if self.tester.is_element_exist_ios('xpath', account):
            self.tester.find_element_by_xpath_and_click(account)
            self.commom_ops()
            time.sleep(2)
        if self.tester.is_element_exist_ios('xpath', login_right_now):
            self.tester.find_element_by_xpath_and_click(login_right_now)
            time.sleep(2)
        elif self.tester.is_element_exist_ios('xpath', email):
            self.tester.logger.info("设备: %s  上次发生登录失败的异常事件" %(self.tester.device.deviceName))
        else:
            self.tester.logger.info("设备: %s 已经登录成功，需要退出账号" %(self.tester.device.deviceName))
            self.tester.swipe_ios("down")
            self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="退出登录"]')
            self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="确定"]')
        self.tester.wait_element_xpath_display(self.tester.driver, email, timeout=5)
        self.tester.find_element_by_xpath_and_click(email)
        time.sleep(1)
        self.tester.find_element_by_xpath_and_send_keys('//XCUIElementTypeTextField[@value="登录邮箱"]',
                                                        self.tester.user.email, timeout=20)
        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeStaticText[@name="listener09@163.com"]')
        self.tester.find_element_by_xpath_and_send_keys('//XCUIElementTypeSecureTextField[@value="密码"]',
                                                        self.tester.user.epassword, timeout=20)
        self.tester.find_element_by_xpath_and_click(login)
        time.sleep(2)
        self.tester.find_element_by_xpath_and_click(account)
        self.assertFalse(self.tester.is_element_exist_ios('xpath', login_right_now), "设备: %s 邮箱登陆失败" %(self.tester.device.deviceName))
        # self.tester.find_element_by_xpath_and_click(account)
        # time.sleep(1)
        # username = self.tester.driver.find_element_by_xpath('//XCUIElementTypeStaticText[@name="云中酒歌"]')
        # self.assertIsNot(username, "设备: %s登录账号不一致" %(self.tester.device.deviceName))

    def tearDown(self):

        self.tester.addfailscreenshot(self._testMethodName)
        self.tester.back_to_start()

    @classmethod
    def tearDownClass(cls):
        pass
