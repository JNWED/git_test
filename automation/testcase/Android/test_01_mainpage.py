# -*- coding:utf-8 -*-
import sys
import time
from common.basetestcase import BaseTestCase
sys.path.append('../..')

class TestMainpage(BaseTestCase):
    """
    主页推荐模块测试类
    """
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.tester.logger.info("Device: %s Start case: %s" % (
            self.tester.device.deviceName, self._testMethodName))
        time.sleep(5)

    def test_mainpage_00_rcmd(self):

        # 检查首页推荐龙珠操作正常
        try:
            myrcmd_btn = self.tester.driver.find_element_by_accessibility_id(
                "我的推荐")
            time.sleep(2)
            if myrcmd_btn:
                self.assertIsNotNone(myrcmd_btn, msg="匿名登录失败")
                myrcmd_btn.click()
                time.sleep(1)
            else:
                self.fail("%s 找不到我的推荐" % (self.tester.device.deviceName))
            self.tester.driver.find_element_by_android_uiautomator(
                'new UiSelector().text("推荐")').click()
            if not self.tester.is_element_exist(
                    'com.netease.cloudmusic:id/mainRcmdResultView'):
                self.fail("%s 找不到推荐" % (self.tester.device.deviceName))
                self.fail("推荐点击失败")

            # 打开每日推荐页面
            time.sleep(2)
            self.tester.find_element_by_id_and_tap(
                'com.netease.cloudmusic:id/dayIcon')
            day_rcmd = self.tester.driver.find_element_by_android_uiautomator(
                'new UiSelector().text("每日推荐")')
            time.sleep(1)
            self.assertIsNotNone(day_rcmd, "每日推荐页面打开失败")
            self.tester.logger.info("Device: %s 每日推荐页面打开成功"
                                    % (self.tester.device.deviceName))
            self.tester.driver.back()
            self.tester.wait_element_id_display(self.tester.driver, 
            'com.netease.cloudmusic:id/dayIcon', "没有找到首页的日推按钮", 10)
            if self.tester.is_element_exist('com.netease.cloudmusic:id/dayIcon'):
                self.tester.logger.info("Device: %s 每日推荐页面返回主页成功"
                                    % (self.tester.device.deviceName))
            else:
                self.tester.logger.info("Device: %s 每日推荐页面没有返回主页"
                                    % (self.tester.device.deviceName))

            # 打开推荐歌单页面
            self.tester.find_element_by_id_and_tap(
                'com.netease.cloudmusic:id/mainRcmdEntryPlaylistIcon')
            playlist_rcmd = self.tester.driver.find_element_by_android_uiautomator(
                'new UiSelector().text("歌单")')
            time.sleep(3)
            self.assertIsNotNone(playlist_rcmd, "推荐歌单页面打开失败")
            self.tester.driver.back()
            time.sleep(3)

            # 打开排行榜页面
            self.tester.find_element_by_id_and_tap(
                'com.netease.cloudmusic:id/upBillIcon')
            time.sleep(3)
            upbill = self.tester.driver.find_element_by_android_uiautomator(
                'new UiSelector().text("排行榜")')
            time.sleep(3)
            self.assertIsNotNone(upbill, "排行榜页面打开失败")
            self.tester.driver.back()
            time.sleep(3)

        except Exception:
            self.fail("首页推荐模块执行出现异常")

    # 检查朋友tab显示正常，可以正常下拉
    def test_mainpage_01_friend(self):
        try:
            self.tester.driver.find_element_by_android_uiautomator(
                'new UiSelector().text("朋友")').click()
            self.tester.swipe_down(5)
        except Exception:
            self.fail("朋友tab执行出现异常")

    def test_mainpage_02_radio(self):
        try:
            self.tester.driver.find_element_by_android_uiautomator(
                'new UiSelector().text("电台")').click()
            pageheaderentry_ele = self.tester.find_element_by_id(
                'com.netease.cloudmusic:id/radioPageHeaderEntry')
            self.assertIsNotNone(pageheaderentry_ele, "电台tab页面打开失败")
            time.sleep(1)
            self.tester.swipe_down(5)

        except Exception:
            self.fail("电台tab执行出现异常")

    def tearDown(self):
        self.tester.addfailscreenshot(self._testMethodName)
        self.tester.back_to_start()

    @classmethod
    def tearDownClass(cls):
        pass
