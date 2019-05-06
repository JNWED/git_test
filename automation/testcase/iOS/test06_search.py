# -*- coding:utf-8 -*-
import sys
import time
import re
from common.basetestcase import BaseTestCase
sys.path.append('../..')


class SearchTest(BaseTestCase):
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
    搜索功能正确
    '''
    def test_SearchTest_01_searchTag(self):
        try:
            self.tester.find_element_by_xpath_and_click('//XCUIElementTypeStaticText[1]')
            self.tester.find_element_by_xpath_and_send_keys('//XCUIElementTypeStaticText[1]', "baby", timeout=20)
            self.tester.find_element_by_xpath_and_click('// XCUIElementTypeButton[@name="Search"]')
            self.tester.swipe_ios('down')
            time.sleep(2)
            list = self.tester.driver.find_elements_by_xpath('//XCUIElementTypeScrollView/XCUIElementTypeButton')
            for element in list:
                element.click()
                time.sleep(2)
                self.tester.logger.info("设备: %s 点击 %s" %((self.tester.device.deviceName),
                                                         (element.get_attribute("name"))))
            self.tester.logger.info("左滑")
            for j in range(1, len(list)):
                self.tester.swipe_ios("left")
                time.sleep(2)
                if j == len(list):
                    break
        except Exception:
            self.fail("设备: %s 搜索功能异常" %(self.tester.device.deviceName))

    '''
    单曲搜索结果正确
    '''
    def test_SearchTest_02_song(self):
        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeStaticText[1]')
        self.tester.find_element_by_xpath_and_send_keys('//XCUIElementTypeStaticText[1]', "baby", timeout=20)
        self.tester.find_element_by_xpath_and_click('// XCUIElementTypeButton[@name="Search"]')
        time.sleep(2)
        self.assertTrue(self.tester.is_element_exist("Baby"),
                        "设备: %s 单曲结果错误" %(self.tester.device.deviceName))
        self.tester.find_element_by_xpath_and_click('(//XCUIElementTypeStaticText[@name="Baby"])[1]')
        time.sleep(2)
        if self.tester.is_element_exist("暂停"):
            self.tester.logger.info("设备: %s 歌曲成功播放" %(self.tester.device.deviceName))
            self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="暂停"]')
            if self.tester.is_element_exist("播放"):
                self.tester.logger.info("设备: %s 歌曲成功暂停" %(self.tester.device.deviceName))
        else:
            self.fail(" 设备: %s 单曲未播放" %(self.tester.device.deviceName))
    '''
    歌手搜索结果正确
    '''
    def test_SearchTest_03_singer(self):
        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeStaticText[1]')
        self.tester.find_element_by_xpath_and_send_keys('//XCUIElementTypeStaticText[1]', "baby", timeout=20)
        self.tester.find_element_by_xpath_and_click('// XCUIElementTypeButton[@name="Search"]')
        time.sleep(2)
        '''点击进入"歌手"界面'''
        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="歌手 未选定"]')
        singer = self.tester.driver.find_element_by_xpath('//XCUIElementTypeStaticText[@name="Justin Bieber (贾斯汀.比伯)"]')
        self.assertIsNotNone(singer, "歌手搜索结果错误")
        singer.click()
        time.sleep(2)
        singe_info = self.tester.driver.find_element_by_xpath('//XCUIElementTypeButton[@name="艺人信息 未选定"]')
        self.assertIsNot(singe_info, "设备: %s 进入艺人信息界面失败" %(self.tester.device.deviceName))

    '''
    视频搜索结果正确
    '''
    def test_SearchTest_04_video(self):
        try:
            self.tester.find_element_by_xpath_and_click('//XCUIElementTypeStaticText[1]')
            self.tester.find_element_by_xpath_and_send_keys('//XCUIElementTypeStaticText[1]', "baby", timeout=20)
            self.tester.find_element_by_xpath_and_click('// XCUIElementTypeButton[@name="Search"]')
            time.sleep(2)
            '''点击进入"视频"界面'''
            self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="视频 未选定"]')
            time.sleep(2)
            video = self.tester.driver.find_element_by_xpath('//XCUIElementTypeCell[1]')
            self.assertIsNotNone(video, "设备: %s 视频搜索结果错误" %(self.tester.device.deviceName))
            video.click()
            time.sleep(3)
        except Exception:
            self.fail("设备: %s 搜索视频异常" %(self.tester.device.deviceName))

    @classmethod
    def tearDownClass(cls):
        pass

