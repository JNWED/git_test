# -*- coding:utf-8 -*-
import sys
import time
from common.basetestcase import BaseTestCase
sys.path.append('../..')


class TestUpbill(BaseTestCase):
    """
    排行榜页面测试类
    """
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.tester.logger.info("Device: %s Start case: %s" % (
            self.tester.device.deviceName, self._testMethodName))
        time.sleep(5)
        self.tester.find_element_by_id_and_tap(
            'com.netease.cloudmusic:id/upBillIcon')

    # 打开排行榜页面并点击榜单可以正常进入排行榜页面
    def test_upbill_00_billboard_list(self):
        time.sleep(5)

        # 根据榜单图片获取官方榜单list（前5个左右）
        billboardimg_list = self.tester.driver.find_elements_by_id(
            'com.netease.cloudmusic:id/billboardImg')
        self.assertIsNotNone(billboardimg_list, "billboard list is empty, check env!")
        billboardimg_list.pop()
        # pop() 函数用于移除列表中的一个元素（默认最后一个元素），并且返回该元素的值。
        time.sleep(3)

        # 逐个点击榜单进入榜单页面
        for cur_ele in billboardimg_list:
            self.assertIsNotNone(cur_ele, "找不到排行榜榜单")
            cur_ele.click()
            time.sleep(2)
            if self.tester.is_element_exist(
                    'com.netease.cloudmusic:id/playAllArea'):
                self.tester.logger.info(
                    "设备: %s 成功进入榜单页面" %
                    (self.tester.device.deviceName))
                self.tester.driver.back()
                time.sleep(2)
            else:
                if self.tester.is_element_exist(
                        'com.netease.cloudmusic:id/billboardCoverContainer'):
                    self.tester.logger.info(
                        "设备: %s 成功进入榜单页面,此榜单暂无歌曲" %
                        (self.tester.device.deviceName))
                    self.tester.driver.back()
                    time.sleep(2)
                else:
                    # 兼容出现webview页面
                    if self.tester.is_element_exist(
                            'com.netease.cloudmusic:id/embedBrowserWebview'):
                        self.tester.logger.info("Device: %s 成功进入webview榜单页面"
                                                % (self.tester.device.deviceName))
                        self.tester.driver.back()
                        time.sleep(2)

        # 检查排行榜页面下滑正常
        self.tester.swipe_down_bottom()
        time.sleep(1)

        # 根据榜单图片获取排行榜页面最后一屏的榜单list（全球榜和用户榜），并点击进入
        billboardimg_list_bottom = self.tester.driver.find_elements_by_id(
            'com.netease.cloudmusic:id/billboardImg')
        for cur_ele in billboardimg_list_bottom:
            self.assertIsNotNone(cur_ele, "找不到榜单")
            cur_ele.click()
            time.sleep(1)

            # 如果榜单是全球榜单的点击判断
            if self.tester.is_element_exist(
                    'com.netease.cloudmusic:id/playlistCreatorContainer'):
                self.tester.logger.info("Device: %s 成功进入全球榜单页面"
                                        % (self.tester.device.deviceName))
                self.tester.driver.back()
                time.sleep(1)
            else:
                # 如果榜单是用户榜单的点击判断
                if self.tester.is_element_exist(
                        'com.netease.cloudmusic:id/playlistCreatorContainer'):
                    self.tester.logger.info("Device: %s 成功进入用户榜单页面"
                                            % (self.tester.device.deviceName))
                    self.tester.driver.back()
                    time.sleep(1)
                else:
                    # 兼容榜单出现webview页面
                    if self.tester.is_element_exist(
                            'com.netease.cloudmusic:id/toolbar'):
                        self.tester.logger.info("Device: %s 成功进入webview榜单页面"
                                                % (self.tester.device.deviceName))
                        self.tester.driver.back()
                        time.sleep(1)
                    else:
                        self.tester.logger.info("Device: %s 没有webview榜单页面"
                                                % (self.tester.device.deviceName))

    # 检查排行榜可以正常收藏后再取消收藏
    def test_upbill_01_sub(self):
        '''
        upbill subscribe
        '''
        self.tester.find_element_by_id_and_tap(
            'com.netease.cloudmusic:id/find_official_billboard_container')
        time.sleep(2)
        # 检查如果榜单是收藏的状态就取消收藏
        if self.tester.is_element_exist(
                'com.netease.cloudmusic:id/subscribedPlAlBtn'):
            time.sleep(2)
            self.tester.find_element_by_id_and_tap(
                'com.netease.cloudmusic:id/subscribedPlAlBtn')
            time.sleep(2)
            unsub_box = self.tester.find_element_by_uiautomator(
                'new UiSelector().text("不再收藏")')
            if unsub_box:
                self.tester.find_element_by_uiautomator_and_tap(
                    'new UiSelector().text("不再收藏")')
                time.sleep(2)
                subscribe_btn = self.tester.find_element_by_id(
                    'com.netease.cloudmusic:id/subscribePlAlBtn')
                self.assertIsNotNone(subscribe_btn, msg="取消收藏失败")
                self.tester.logger.info("Device: %s 榜单取消收藏成功"
                                        % (self.tester.device.deviceName))
            else:
                self.tester.logger.info("Device: %s 点击取消没有出现二次确认弹框"
                                        % (self.tester.device.deviceName))

        # 检查点击收藏按钮
        subscribe_btn = self.tester.find_element_by_id(
            'com.netease.cloudmusic:id/subscribePlAlBtn')
        self.tester.find_element_by_id_and_tap('com.netease.cloudmusic:id/subscribePlAlBtn')
        time.sleep(3)
        # 检查点击收藏后按钮变为已收藏
        subscribed_btn = self.tester.find_element_by_id(
            'com.netease.cloudmusic:id/subscribedPlAlBtn')
        self.assertIsNotNone(subscribed_btn, "榜单收藏失败")
        self.tester.logger.info(
            "设备: %s 榜单收藏成功" %
            (self.tester.device.deviceName))
        subscribed_btn.click()
        time.sleep(3)
        element = self.tester.find_element_by_uiautomator(
            'new UiSelector().text("不再收藏")')
        if element is None:
            subscribed_btn.click()
            time.sleep(2)
            element = self.tester.find_element_by_uiautomator('new UiSelector().text("不再收藏")')
            self.assertIsNotNone(element, "Failed to find 不再收藏")
        else:
            element.click()

        time.sleep(2)
        subscribe_btn = self.tester.find_element_by_id(
            'com.netease.cloudmusic:id/subscribePlAlBtn')
        self.assertIsNotNone(subscribe_btn, msg="取消收藏失败")
        self.tester.logger.info(
            "设备: %s 榜单取消收藏成功" %
            (self.tester.device.deviceName))

    # 检查排行榜可以正常分享
    def test_upbill_02_share(self):
        self.tester.find_element_by_id_and_tap(
            'com.netease.cloudmusic:id/find_official_billboard_container')
        time.sleep(2)
        self.tester.find_element_by_id_and_tap(
            'com.netease.cloudmusic:id/shareBlock')
        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().text("云音乐动态")')
        time.sleep(1)
        resource_name = self.tester.find_element_by_id(
            'com.netease.cloudmusic:id/name')
        self.tester.find_element_by_id_and_send_keys(
            'com.netease.cloudmusic:id/status', "排行榜单分享到动态")
        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().text("分享")')
        time.sleep(1)
        share_btn = self.tester.find_element_by_id(
            'com.netease.cloudmusic:id/shareBlock')
        self.assertIsNotNone(share_btn, "分享失败")
        self.tester.logger.info("Device: %s 榜单分享后成功返回榜单页面"
                                % (self.tester.device.deviceName))

    def tearDown(self):
        self.tester.addfailscreenshot(self._testMethodName)
        self.tester.back_to_start()

    @classmethod
    def tearDownClass(cls):
        pass
