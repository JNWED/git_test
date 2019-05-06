# -*- coding:utf-8 -*-
import sys
import time
from common.basetestcase import BaseTestCase
sys.path.append('../..')


class VideoTest(BaseTestCase):
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
    视频流上拉下滑展示正常
    '''
    def test_VideoTest_01_videoContent(self):
        try:
            self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="视频"]')
            time.sleep(1)
            self.tester.swipe_ios('down')
            time.sleep(1)
            self.tester.swipe_ios("up")
        except Exception:
            self.fail("设备: %s 视频加载异常" %(self.tester.device.deviceName))

    '''
    视频能正确播放
    '''
    def test_VideoTest_02_playVideo(self):
        try:
            self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="视频"]')
            time.sleep(2)
            self.tester.find_element_by_xpath_and_click('//XCUIElementTypeCell[1]')
            time.sleep(4)
            if self.tester.is_element_exist("关注"):
                self.tester.logger.info("视频播放成功，提示用户关注")
            else:
                self.tester.logger.info("没找到关注元素")
            self.assertTrue(self.tester.is_element_exist("关注"), "设备: %s 视频播放失败" %(self.tester.device.deviceName))
        except Exception:
            self.fail("设备: %s 视频播放异常" %(self.tester.device.deviceName))

    @classmethod
    def tearDownClass(cls):
        pass

