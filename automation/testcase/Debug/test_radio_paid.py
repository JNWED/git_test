# -*- coding:utf-8 -*-

import sys
import time
from common.basetestcase import BaseTestCase

sys.path.append('../..')


class Radiotest2(BaseTestCase):
    """
    检查付费精品
    """

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.tester.logger.info("Device: %s Start case: %s" % (
            self.tester.device.deviceName, self._testMethodName))
        time.sleep(7)

    def test_radio_06(self):
        self.skipTest("skip test_radio_07 due to stability issue")

        # 检查付费精品
        ele_radio = self.tester.driver.find_element_by_android_uiautomator(
            'new UiSelector().text("电台")')
        if ele_radio:
            ele_radio.click()
            time.sleep(3)
        else:
            self.fail("找不到电台按钮")
        self.tester.swipe_down(2)

        radio_id = "com.netease.cloudmusic:id/more"
        self.tester.wait_element_for_a_while(radio_id, 10)
        find_element = self.tester.find_element_by_id(radio_id)
        if find_element is None:
            self.tester.swipe_to_page_top()
            self.tester.scroll_to_exact_element(radio_id)
            find_element = self.tester.find_element_by_id(radio_id)

        self.assertIsNotNone(find_element,'找不到全部精品按钮,Fail')
        find_element.click()
        self.tester.swipe_down(3)

    def test_radio_07(self):
        # 检查付费电台
        self.skipTest("skip test_radio_07 due to stability issue")
        ele_radio2 = self.tester.driver.find_element_by_android_uiautomator(
            'new UiSelector().text("电台")')
        if ele_radio2:
            ele_radio2.click()
            time.sleep(3)
        else:
            self.fail("找不到电台按钮")

        self.tester.swipe_down(2)

        radio2_id = "com.netease.cloudmusic:id/radioCover"
        self.tester.wait_element_for_a_while(radio2_id, 10)
        find_element_paid = self.tester.find_element_by_id(radio2_id)
        if find_element_paid is None:
            self.tester.swipe_to_page_top()
            self.tester.scroll_to_exact_element(radio2_id)
            find_element_paid = self.tester.find_element_by_id(radio2_id)
        self.assertIsNotNone(find_element_paid,'找不到付费精品按钮,Fail')
        find_element_paid.click()
        time.sleep(3)

        radio3_id = "com.netease.cloudmusic:id/radioProgramSubscibeBtn"
        self.tester.wait_element_for_a_while(radio3_id, 10)
        find_element_pay = self.tester.find_element_by_id(radio3_id)
        if find_element_pay is None:
            self.tester.wait_element_for_a_while(radio3_id, 10)
            find_element_pay = self.tester.find_element_by_id(radio3_id)
        self.assertIsNotNone(find_element_pay,'找不到购买按钮,Fail')
        find_element_pay.click()
        time.sleep(3)
        self.tester.driver.back()

    def tearDown(self):
        '''
        tearDown
        '''
        self.tester.addfailscreenshot(self._testMethodName)
        self.tester.back_to_start()

    @classmethod
    def tearDownClass(cls):
        pass
