# -*- coding:utf-8 -*-
import sys
import time
from common.basetestcase import BaseTestCase
sys.path.append('../..')


class PaidFmTest(BaseTestCase):
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
    付费精品展示正确
    '''
    def test_PaidFmTest_01_bottomTag(self):
        try:
            self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="主播电台 未选定"]')
            self.tester.wait_element_xpath_display(self.tester.driver, '//XCUIElementTypeButton[@name="付费精品"]',
                                                   timeout=5)
            self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="付费精品"]')
            fm = self.tester.driver.find_element_by_xpath('//XCUIElementTypeCell[1]')
            self.assertIsNotNone(fm, "设备: %s 未找到付费电台" %(self.tester.device.deviceName))
            element = self.tester.driver.find_element_by_xpath('//XCUIElementTypeCell[1]/XCUIElementTypeStaticText[2]')
            name = element.get_attribute("name")
            self.tester.logger.info(name)
            fm.click()
            time.sleep(3)
            fm_free = self.tester.driver.find_element_by_xpath('//XCUIElementTypeButton[@name="免费试听"]')
            self.assertIsNotNone(fm_free, "设备: %s 进入付费电台界面失败" %(self.tester.device.deviceName))
            self.tester.swipe_ios("down")
        except Exception:
            self.fail("付费精品异常")

    @classmethod
    def tearDownClass(cls):
        pass

