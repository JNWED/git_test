# -*- coding:utf-8 -*-
import sys
import time
from common.basetestcase import BaseTestCase
sys.path.append('../..')


class TestMaindraw(BaseTestCase):
    """
    侧边栏测试类
    """
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.tester.logger.info("Device: %s Start case: %s" % (
            self.tester.device.deviceName, self._testMethodName))
        self.tester.find_element_by_id_and_tap(
            'com.netease.cloudmusic:id/mainDrawerIcon')
        time.sleep(5)

    def test_maindraw_00_message(self):
        # 我的消息
        self.tester.find_element_by_id_and_tap(
            'com.netease.cloudmusic:id/mainDrawerMessage')
        time.sleep(1)
        message_title = self.tester.find_element_by_uiautomator(
            'new UiSelector().text("我的消息")')
        time.sleep(1)
        if message_title is None:
            message_title = self.tester.find_element_by_uiautomator(
                'new UiSelector().text("我的消息")')
            self.assertIsNotNone(message_title, "打开我的消息页面失败")
        self.tester.logger.info("设备: %s %s 页面打开成功"
                                % (self.tester.device.deviceName, message_title.text))


    def test_maindraw_01_friends(self):
        self.tester.find_element_by_id_and_tap(
            'com.netease.cloudmusic:id/mainDrawerFriends')
        time.sleep(1)

        # 检查如果出现允许确认弹框点击允许(首次打开页面会出现)
        if self.tester.is_element_exist(
                'com.netease.cloudmusic:id/buttonDefaultPositive'):
            allow_box = self.tester.find_element_by_uiautomator(
                'new UiSelector().text("允许")')
            if allow_box:
                self.assertIsNotNone(allow_box, "点击确认弹框失败")
                self.tester.find_element_by_uiautomator_and_tap(
                'new UiSelector().text("允许")')
                time.sleep(2)
                self.tester.logger.info("设备: %s 我的好友页面允许获取通讯录联系人列表"
                                        % (self.tester.device.deviceName))
            else:
                self.tester.logger.info("设备: %s 获取通讯录联系人列表没有”允许“按钮"
                                        % (self.tester.device.deviceName))
        else:
            self.tester.logger.info("设备: %s 没有出现弹框：获取通讯录联系人列表"
                                    % (self.tester.device.deviceName))

        # 检查不出现允许弹框可以直接进入页面
        friends_title = self.tester.find_element_by_uiautomator(
            'new UiSelector().text("我的好友")')
        time.sleep(2)
        if friends_title is None:
            friends_title = self.tester.find_element_by_uiautomator(
                'new UiSelector().text("我的好友")')
            self.assertIsNotNone(friends_title, "进入我的好友页面失败")
            self.tester.logger.info("设备: %s %s 页面打开成功"
                                    % (self.tester.device.deviceName, friends_title.text))

        self.tester.logger.info("设备: %s %s 页面打开成功"
                                    % (self.tester.device.deviceName, friends_title.text))

    # 个性换肤
    def test_maindraw_02_theme(self):
        # 检查侧边栏下滑到底部
        self.tester.swipe_down_bottom()
        self.tester.logger.info(
            "设备: %s 侧边栏下滑到底部" %
            (self.tester.device.deviceName))
        time.sleep(2)
        self.tester.find_element_by_id_and_tap(
            'com.netease.cloudmusic:id/mainDrawerTheme')
        time.sleep(2)
        theme_title = self.tester.find_element_by_uiautomator(
            'new UiSelector().text("个性换肤")')
        if theme_title is None:
            theme_title = self.tester.find_element_by_uiautomator(
                'new UiSelector().text("个性换肤")')
            self.assertIsNotNone(theme_title, "打开换肤页面失败")
            self.tester.logger.info("设备: %s %s 页面打开成功"
                                    % (self.tester.device.deviceName, theme_title.text))

    # 音乐闹钟
    def test_maindraw_03_alarm(self):
        self.tester.swipe_down_bottom()
        time.sleep(1)
        self.tester.find_element_by_id_and_tap(
            'com.netease.cloudmusic:id/mainDrawerAlarmClock')
        alarmclock_title = self.tester.find_element_by_uiautomator(
            'new UiSelector().text("音乐闹钟")')
        time.sleep(2)
        if alarmclock_title is None:
            alarmclock_title = self.tester.find_element_by_uiautomator(
                'new UiSelector().text("音乐闹钟")')
            self.assertIsNotNone(alarmclock_title, "打开闹钟页面失败")
            self.tester.logger.info("设备: %s %s 页面打开成功"
                                    % (self.tester.device.deviceName, alarmclock_title.text))

    # 音乐云盘
    def test_maindraw_04_privatecloud(self):
        self.tester.swipe_down_bottom()
        time.sleep(1)
        self.tester.find_element_by_id_and_tap(
            'com.netease.cloudmusic:id/mainDrawerPrivateCloud')
        privatecloud_title = self.tester.find_element_by_uiautomator(
            'new UiSelector().text("音乐云盘")')
        time.sleep(1)
        if privatecloud_title is None:
            privatecloud_title = self.tester.find_element_by_uiautomator(
                'new UiSelector().text("音乐云盘")')
            self.assertIsNotNone(privatecloud_title, "打开云盘页面失败")
            self.tester.logger.info("设备: %s %s 页面打开成功"
                                    % (self.tester.device.deviceName, privatecloud_title.text))

    # 优惠券
    def test_maindraw_05_discountcoupon(self):
        self.tester.swipe_down_bottom()
        time.sleep(1)
        self.tester.find_element_by_id_and_tap(
            'com.netease.cloudmusic:id/mainDrawerDiscountCoupon')
        discountcoupon_title = self.tester.find_element_by_uiautomator(
            'new UiSelector().text("优惠券")')
        time.sleep(1)
        if discountcoupon_title is None:
            discountcoupon_title = self.tester.find_element_by_uiautomator(
                'new UiSelector().text("优惠券")')
            self.assertIsNotNone(discountcoupon_title, "打开优惠券页面失败")
            self.tester.logger.info("设备: %s %s 页面打开成功"
                                    % (self.tester.device.deviceName, discountcoupon_title.text))

    # 设置页
    def test_maindraw_06_drawersetting(self):
        self.tester.find_element_by_id_and_tap(
            'com.netease.cloudmusic:id/drawerSetting')
        setting_title = self.tester.find_element_by_uiautomator(
            'new UiSelector().text("设置")')
        time.sleep(1)
        if setting_title is None:
            setting_title = self.tester.find_element_by_uiautomator(
                'new UiSelector().text("设置")')
            self.assertIsNotNone(setting_title, "打开设置页面失败")
            self.tester.logger.info("设备: %s %s 页面打开成功"
                                    % (self.tester.device.deviceName, setting_title.text))

    def tearDown(self):
        self.tester.addfailscreenshot(self._testMethodName)
        self.tester.back_to_start()

    @classmethod
    def tearDownClass(cls):
        pass
