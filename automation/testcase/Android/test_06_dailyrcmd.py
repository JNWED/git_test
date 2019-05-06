# -*- coding:utf-8 -*-
import sys
import time
from common.basetestcase import BaseTestCase
sys.path.append('../..')


class DailyRcmd(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.tester.logger.info("Device: %s Start case: %s" % (
            self.tester.device.deviceName, self._testMethodName))
        time.sleep(5)

    def test_dailyrcmd_00_open(self):
        '''
        推荐模块页面开启测试--每日推荐、推荐歌单、排行榜
        '''
        try:
            myrcmd_btn = self.tester.driver.find_element_by_accessibility_id(
                "我的推荐")
            if myrcmd_btn:
                myrcmd_btn.click()
                time.sleep(1)
            self.tester.driver.find_element_by_android_uiautomator(
                'new UiSelector().text("推荐")').click()
            if self.tester.is_element_exist(
                    'com.netease.cloudmusic:id/mainRcmdResultView'):
                self.tester.logger.info(
                    "设备: %s 打开推荐tab" % (self.tester.device.deviceName))

            # 打开每日推荐页面
            self.tester.find_element_by_id_and_tap(
                'com.netease.cloudmusic:id/dayIcon')
            dailymusic_list = self.tester.find_element_by_id(
                'com.netease.cloudmusic:id/musicListItemContainer')
            time.sleep(1)
            if dailymusic_list:
                self.assertIsNotNone(dailymusic_list, "日推页面打开失败")
                self.tester.logger.info(
                    "设备: %s 日推页面打开成功" % (self.tester.device.deviceName))
                self.tester.find_element_by_id_and_tap(
                    'com.netease.cloudmusic:id/playAllArea')
                self.tester.logger.info(
                    "设备: %s 日推页面点击全部播放" % (self.tester.device.deviceName))
                time.sleep(2)
            else:
                self.tester.logger.info(
                    "设备: %s 没有找到日推banner" % (self.tester.device.deviceName))

        except Exception:
            self.tester.logger.info(
                "设备: %s 推荐模块出现异常" % (self.tester.device.deviceName))

    def tearDown(self):
        self.tester.addfailscreenshot(self._testMethodName)
        self.tester.back_to_start()

    @classmethod
    def tearDownClass(cls):
        pass
