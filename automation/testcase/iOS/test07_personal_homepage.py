# -*- coding:utf-8 -*-
import sys
import time
from common.basetestcase import BaseTestCase
sys.path.append('../..')

user_name = '//XCUIElementTypeStaticText[@name="云中酒哥"]'


class PersonalHomepageTest(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.tester.logger.info("Device: %s Start case: %s" % (
            self.tester.device.deviceName, self._testMethodName))
        time.sleep(5)
        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="帐号"]')
        self.commom_ops()
        self.tester.wait_element_xpath_display(self.tester.driver, '//XCUIElementTypeButton[@name="我的资料"]')

        self.tester.logger.info("设备: %s 开始点击用户名进入个人主页：" % (self.tester.device.deviceName))
        self.tester.find_element_by_xpath_and_click(user_name)

    def tearDown(self):
        self.tester.addfailscreenshot(self._testMethodName)
        self.tester.back_to_start()

    def commom_ops(self):
        if self.tester.is_element_exist_ios('xpath', '//XCUIElementTypeStaticText[@name="私信"]'):
            self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="返回"]')
            time.sleep(2)
        else:
            pass

    '''
    个人用户名正常展示
    '''
    def test_personal_homepage_01_name(self):

        self.assertIsNotNone(self.tester.driver.find_element_by_xpath(user_name), "设备: %s 个人主页展示失败" % (self.tester.device.deviceName))

    '''
    关注数量，粉丝数显示正常，点击后进入关注和粉丝列表页
    '''
    def test_personal_homepage_02_focus(self):

        self.tester.wait_element_xpath_display(self.tester.driver, '//XCUIElementTypeButton[@name="编辑个人信息"]')

        self.tester.logger.info("设备: %s 开始点击关注数进入关注页：" % (self.tester.device.deviceName))

        # print self.tester.driver.page_source
        # 获取关注坐标并点击
        x = int(self.tester.driver.find_element_by_xpath('//XCUIElementTypeStaticText[contains(@name,"关注")]').location.get('x'))
        y = int(self.tester.driver.find_element_by_xpath('//XCUIElementTypeStaticText[contains(@name,"关注")]').location.get('y'))

        # 防止未点击到元素，多次点击
        i = 0
        while i < 5:
            self.tester.driver.tap([(x, y)], 100)
            if self.tester.is_element_exist_ios('xpath', '//XCUIElementTypeNavigationBar[@name="关注"]'):
                break
            else:
                self.tester.driver.tap([(x, y)], 100)
                i += 1

        time.sleep(2)
        self.tester.wait_element_xpath_display(self.tester.driver, '//XCUIElementTypeNavigationBar[@name="关注"]')
        self.assertIsNotNone(self.tester.driver.find_element_by_xpath('//XCUIElementTypeNavigationBar[@name="关注"]'),
                             "设备: %s 进入关注页失败" % (self.tester.device.deviceName))

        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="返回"]')
        self.tester.wait_element_xpath_display(self.tester.driver, '//XCUIElementTypeStaticText[contains(@name, "粉丝")]')

        self.tester.logger.info("设备: %s 开始点击粉丝数进入粉丝列表页：" % (self.tester.device.deviceName))
        # 防止未点击到元素，多次点击
        x = int(
            self.tester.driver.find_element_by_xpath('//XCUIElementTypeStaticText[contains(@name,"粉丝")]').location.get(
                'x'))
        y = int(
            self.tester.driver.find_element_by_xpath('//XCUIElementTypeStaticText[contains(@name,"粉丝")]').location.get(
                'y'))

        i = 0
        while i < 5:
            self.tester.driver.tap([(x, y)], 100)

            if self.tester.is_element_exist_ios('xpath', '//XCUIElementTypeNavigationBar[@name="粉丝"]'):
                break
            else:
                self.tester.driver.tap([(x, y)], 100)
                i += 1

        time.sleep(2)
        self.tester.wait_element_xpath_display(self.tester.driver, '//XCUIElementTypeNavigationBar[@name="粉丝"]')
        self.assertIsNotNone(self.tester.driver.find_element_by_xpath('	//XCUIElementTypeNavigationBar[@name="粉丝"]'),
                             "设备: %s 进入粉丝列表页失败" % (self.tester.device.deviceName))

    '''
    检查音乐、动态、关于TA三个tab，可以点击切换，也可以滑动切换
    '''
    def test_personal_homepage_03_tab(self):

        self.tester.wait_element_xpath_display(self.tester.driver, '//XCUIElementTypeButton[@name="编辑个人信息"]')

        self.tester.logger.info("设备: %s 开始切换动态tab：" % (self.tester.device.deviceName))
        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="动态 未选定"]')
        self.assertIsNotNone(self.tester.driver.find_element_by_xpath('//XCUIElementTypeButton[@name="动态 已选定"]'),
                             "设备: %s 切换动态" % (self.tester.device.deviceName))

        self.tester.logger.info("设备: %s 开始切换关于TAtab：" % (self.tester.device.deviceName))
        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="关于我 未选定"]')
        self.assertIsNotNone(self.tester.driver.find_element_by_xpath('//XCUIElementTypeButton[@name="关于我 已选定"]'),
                             "设备: %s 关于我动态" % (self.tester.device.deviceName))

        # 滑动代码稳定性不好控制，去掉这些case
        # self.tester.swipe_right_ios()
        # self.assertIsNotNone(self.tester.driver.find_element_by_id('动态 已选定'),
        #                      "设备: %s 滑动切换动态" % (self.tester.device.deviceName))
        #
        # self.tester.swipe_right_ios()
        # self.assertIsNotNone(self.tester.driver.find_element_by_id('音乐 已选定'),
        #                      "设备: %s 滑动切换音乐" % (self.tester.device.deviceName))

    @classmethod
    def tearDownClass(cls):
        pass

