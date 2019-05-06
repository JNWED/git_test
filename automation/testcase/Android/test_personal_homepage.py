# -*- coding:utf-8 -*-

import sys
import time
import datetime
from common.basetestcase import BaseTestCase

sys.path.append('../..')


class TestPersonalHomePage(BaseTestCase):
    """
    个人主页测试类
    """

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.tester.logger.info("Device: %s Start case: %s" % (
            self.tester.device.deviceName, self._testMethodName))
        self.tester.double_check_login()

    def tearDown(self):
        '''
        tearDown
        '''
        self.tester.addfailscreenshot(self._testMethodName)
        self.tester.back_to_start()

    @classmethod
    def tearDownClass(cls):
        pass

    def test_01_header(self):
        self.common_ops()

        # 检查音乐、动态、关于TA/我 三个tab显示正确，可以点击或滑动切换
        self.tester.swipe_left(2)
        self.tester.swipe_right(2)

        # 检查点击关注进入我的好友页面定位在关注tab
        follow_text = "关注"
        error_msg = "未找到" + follow_text + "关键字"
        self.tester.wait_element_for_a_while(follow_text, 20)
        self.assertTrue(self.tester.is_element_exist(follow_text), error_msg)

        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().textStartsWith("{}")'.format(follow_text))
        time.sleep(2)

        allow_resouce_id = "com.netease.cloudmusic:id/buttonDefaultPositive"
        if self.tester.is_element_exist(allow_resouce_id):
            self.tester.find_element_by_uiautomator_and_tap(
                'new UiSelector().text("{}")'.format(allow_resouce_id))
            time.sleep(3)

        # 兼容小米权限系统
        if self.tester.is_element_exist("android:id/button1"):
            self.tester.find_element_by_uiautomator_and_tap(
                'new UiSelector().text("{}")'.format("android:id/button1"))
            time.sleep(3)

        dot_3_res_id = "com.netease.cloudmusic:id/sendMailBtn"
        error_msg = "焦点不在" + follow_text + "tab页内"
        self.assertTrue(self.tester.is_element_exist(dot_3_res_id), error_msg)
        self.tester.press_back()

        # 检查点击粉丝进入我的好友页面定位在粉丝tab
        fans_text = "粉丝"
        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().textStartsWith("{}")'.format(fans_text))
        time.sleep(2)

        error_msg = "未找到" + fans_text + "关键字"
        self.assertTrue(self.tester.is_element_exist(follow_text), error_msg)
        self.tester.press_back()

    def test_02_tabs(self):
        self.common_ops()
        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().textStartsWith("{}")'.format("动态"))
        time.sleep(3)

        # 检查音乐tab显示用户创建的资源显示正确
        error_msg = "未找到分享button，请确认是否跳转正确"
        self.assertTrue(self.tester.is_element_exist("分享"), error_msg)

        # 检查动态tab显示用户的动态正确，点击进入动态详情页
        if self.tester.is_element_exist("com.netease.cloudmusic:id/trackDesc"):
            self.tester.find_element_by_id_and_tap(
                "com.netease.cloudmusic:id/trackDesc")
            time.sleep(2)
            error_msg = "未跳转到对应动态详情页"
            self.assertTrue(self.tester.is_element_exist("动态"), error_msg)
            self.tester.press_back()

    def test_03_edit_info(self):
        self.common_ops()

        # 检查个人主页自己可以编辑资料
        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().text("编辑")')
        time.sleep(3)
        self.tester.find_element_by_id_and_tap(
            "com.netease.cloudmusic:id/profileModifyDesc")

        mock_msg = "云中听哥" + str(datetime.datetime.now())
        input_res_id = "com.netease.cloudmusic:id/profileModifyAvatarContainer"
        self.tester.send_one_msg(input_res_id, mock_msg, "保存")
        self.tester.press_back(2)

    def common_ops(self):
        """
        进入我的个人主页公共操作
        """
        self.tester.wait_for_stable_main_page(10)
        if self.tester.is_element_exist("抽屉菜单"):
            self.tester.find_element_by_uiautomator_and_tap(
                'new UiSelector().description("抽屉菜单")')
            time.sleep(2)

            # 点击头像图标进入个人主页
            if self.tester.is_element_exist(
                    "com.netease.cloudmusic:id/drawerUserName"):
                self.tester.find_element_by_id_and_tap(
                    "com.netease.cloudmusic:id/drawerUserName")
            count = 0
            while not self.tester.is_element_exist("关注") and count < 10:
                time.sleep(2)
                count = count + 1
