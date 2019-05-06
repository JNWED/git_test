# -*- coding:utf-8 -*-
import sys
import time
from common.basetestcase import BaseTestCase
sys.path.append('../..')


class DailyTest(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.tester.logger.info("Device: %s Start case: %s" % (
            self.tester.device.deviceName, self._testMethodName))
        time.sleep(4)

    def tearDown(self):
        self.tester.addfailscreenshot(self._testMethodName)
        self.tester.back_to_start()
    '''
    今日推荐成功展示
    '''
    def test_DailyTest_01_bottomTag(self):
        try:
            self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="每日推荐"]')
            self.tester.wait_element_xpath_display(self.tester.driver, '//XCUIElementTypeButton[@name="播放全部"]',
                                                   timeout=5)
            self.tester.logger.info("设备: %s 滑动页面进行加载：" %(self.tester.device.deviceName))
            self.tester.swipe_ios('down')
            self.assertIsNotNone(self.tester.driver.find_element_by_xpath('//XCUIElementTypeStaticText[@name="每日推荐"]'),
                                 "设备: %s 今日推荐展示失败" %(self.tester.device.deviceName))
            self.assertIsNotNone(self.tester.driver.find_element_by_xpath('//XCUIElementTypeButton[@name="播放全部"]'),
                                 "设备: %s 今日推荐内容为空" % (self.tester.device.deviceName))
            self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="播放全部"]')
            time.sleep(3)
            self.tester.logger.info('今日推荐成功播放')
        except Exception:
            self.fail("设备: %s 今日推荐异常" %(self.tester.device.deviceName))

    @classmethod
    def tearDownClass(cls):
        pass

