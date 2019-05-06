# -*- coding:utf-8 -*-

import sys
import time
import datetime
import hashlib
from common.basetestcase import BaseTestCase

sys.path.append('../..')


class TestDynamicStatus(BaseTestCase):
    """
    检查发布文字动态测试类
    """

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.tester.logger.info("Device: %s Start case: %s" % (
            self.tester.device.deviceName, self._testMethodName))
        self.tester.double_check_login()
        self.common_ops()

    def tearDown(self):
        '''
        tearDown
        '''
        self.tester.addfailscreenshot(self._testMethodName)
        if (self._testMethodName == "test_dynamic_status_06_follow_user"):
            self.double_insurance_del()
        self.tester.back_to_start()

    @classmethod
    def tearDownClass(cls):
        pass

    def test_dynamic_status_01_post_status(self):
        '''
        检查发布文字动态
        '''
        self.tester.find_element_by_id_and_tap(
            "com.netease.cloudmusic:id/sendNewTrack")
        time.sleep(2)

        send_text_keyword = "发动态"
        error_msg = "未找到发动态按钮"
        self.tester.wait_element_for_a_while(send_text_keyword, 10)
        self.assertTrue(self.tester.is_element_exist(
            send_text_keyword), error_msg)
        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().text("{}")'.format(send_text_keyword))
        time.sleep(2)
        res_id = "com.netease.cloudmusic:id/status"
        self.tester.wait_element_for_a_while(res_id, 10)
        mock_msg = str(datetime.datetime.now()) + "-发条普通文字动态记录当下的想法"
        self.tester.send_one_msg(res_id, mock_msg)
        time.sleep(5)
        self.del_status()
        time.sleep(2)

    def test_dynamic_status_02_post_video_status(self):
        """
        动态发布-检查发布视频动态发布成功
        """
        self.tester.find_element_by_id_and_tap(
            "com.netease.cloudmusic:id/sendNewTrack")
        time.sleep(2)

        publish_video_text = "发布视频"
        self.assertTrue(self.tester.is_element_exist(
            publish_video_text), "未找到发布视频Button")
        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().text("{}")'.format(publish_video_text))
        time.sleep(2)
        self.assertTrue(self.tester.is_element_exist(
            "com.netease.cloudmusic:id/videoImage"), "Opps，请先在待测机器上准备视频文件")

        # 选择一个本地视频
        self.tester.find_element_by_id_and_tap(
            "com.netease.cloudmusic:id/videoImage")
        time.sleep(3)
        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().text("下一步")')
        time.sleep(3)
        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().text("完成")')
        time.sleep(3)

        self.tester.find_element_by_id_and_tap(
            "com.netease.cloudmusic:id/musics")
        time.sleep(3)
        mock_song_name = "南方姑娘"
        self.tester.search_keyword(mock_song_name)
        self.assertTrue(self.tester.is_element_exist(
            "com.netease.cloudmusic:id/songName"))
        self.tester.find_element_by_id_and_tap(
            "com.netease.cloudmusic:id/songName")
        time.sleep(3)
        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().description("收起")')
        time.sleep(3)

        mock_video_title_text = str(datetime.datetime.now()) + "-Show一个好玩的视频"
        self.tester.send_one_msg(
            "com.netease.cloudmusic:id/title",
            mock_video_title_text)
        self.tester.wait_element_for_a_while(mock_video_title_text, 40)
        self.assertTrue(self.tester.is_element_exist(
            mock_video_title_text), "未找到刚才发送的视频")

        self.del_status()
        time.sleep(3)

    def test_dynamic_status_03_dynamic_feeds(self):
        # 动态流-检查动态可以点赞操作

        thumbs_up_id = "com.netease.cloudmusic:id/trackLikeBtn"
        ele_lastest_share = self.tester.scroll_to_exact_ele_res_id(
            thumbs_up_id)
        self.assertIsNotNone(ele_lastest_share, "未在当前页面找到点赞控件")
        ele_thumbs_up = self.tester.driver.find_element_by_id(thumbs_up_id)
        like_count_before = ele_thumbs_up.text.strip()
        ele_thumbs_up.click()
        time.sleep(5)
        like_count_after = ele_thumbs_up.text.strip()
        if like_count_before == "赞":
            self.assertEqual(int(like_count_after), 1, "第一个点赞过后点赞数目应该为1")
        else:
            self.assertEqual(
                int(like_count_before) + 1,
                int(like_count_after),
                "点赞后点赞数据应该+1")

            # 恢复环境,避免下次执行出错
            ele_thumbs_up.click()
            time.sleep(1)

    def test_dynamic_status_04_share_2_feeds(self):
        """
        动态流-检查点击分享可以分享到动态
        """
        info_text = "开始测试-动态流-检查点击分享可以分享到动态"
        self.tester.logger.info(
            "Device: %s %s" %
            (self.tester.device.deviceName, info_text))
        share_res_id = "com.netease.cloudmusic:id/trackRepostBtn"
        ele_lastest_share = self.tester.scroll_to_exact_ele_res_id(
            share_res_id)
        self.assertIsNotNone(ele_lastest_share, "未在当前页面找到分享控件")

        self.tester.find_element_by_id_and_tap(share_res_id)
        self.tester.wait_element_for_a_while("云音乐动态", 10)

        self.assertTrue(self.tester.is_element_exist("云音乐动态"), "点击分享后未发现云音乐动态")
        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().text("{}")'.format("云音乐动态"))
        time.sleep(2)
        res_id = "com.netease.cloudmusic:id/editForwardContent"
        mock_msg = str(datetime.datetime.now()) + "-还蛮有意思的"
        self.tester.send_one_msg(res_id, mock_msg)

        count = 0
        while not self.tester.is_element_exist(mock_msg) and count < 6:
            self.tester.swipe_up()
            count = count + 1
            time.sleep(2)
        self.assertTrue(
            self.tester.is_element_exist(mock_msg),
            "找不到转发动态内容： " + mock_msg)
        self.del_status()

    def test_dynamic_status_05_check_detail_information(self):
        """
        动态流-检查点击动态进入动态详情页正确
        """
        self.assertTrue(self.tester.is_element_exist(
            "com.netease.cloudmusic:id/trackDesc"), "未找到动态")
        self.tester.find_element_by_id_and_tap(
            "com.netease.cloudmusic:id/trackDesc")
        time.sleep(2)
        self.assertTrue(self.tester.is_element_exist(
            "com.netease.cloudmusic:id/sectionName"), "未在动态详情页面找到section")
        self.tester.press_back()
        self.del_status()

    def test_dynamic_status_06_follow_user(self):
        self.skipTest("skip test_dynamic_status_06_follow_user due to stablity issue")
        remd_user_res_id = "com.netease.cloudmusic:id/trackNewTrackUserName"
        self.assertTrue(self.tester.is_element_exist(
            remd_user_res_id), "推荐直通车中必须有用户")
        remd_username = self.tester.driver.find_element_by_id(
            remd_user_res_id).text
        self.cmp_nickname(
            remd_user_res_id,
            "com.netease.cloudmusic:id/userFaceImage")

        follow_btn_res_id = "com.netease.cloudmusic:id/followBtn"
        self.tester.wait_element_for_a_while(follow_btn_res_id, 10)
        if not self.tester.is_element_exist(follow_btn_res_id):
            self.tester.swipe_up(2)
        self.assertTrue(self.tester.is_element_exist(
            follow_btn_res_id), "关注或取消关注Button必须存在")
        ele_follow_btn = self.tester.driver.find_element_by_id(
            follow_btn_res_id)
        if ele_follow_btn.text:
            info_text = "点击关注按钮关注用户: " + remd_username
            self.tester.logger.info(
                "Device: %s %s" %
                (self.tester.device.deviceName, info_text))
            ele_follow_btn.click()
            time.sleep(2)
        self.tester.press_back()
        time.sleep(5)

        self.enter_my_homepage()
        follow_text = "关注"
        self.assertTrue(self.tester.is_element_exist(follow_text), "未找到关注关键字")
        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().textStartsWith("{}")'.format(follow_text))
        time.sleep(2)
        allow_res_id = "com.netease.cloudmusic:id/buttonDefaultPositive"
        if self.tester.is_element_exist(allow_res_id):
            self.tester.find_element_by_id_and_tap(allow_res_id)
            time.sleep(2)

        self.assertTrue(
            self.tester.is_element_exist(remd_username),
            "未在我的好友中找到刚刚关注的用户" + remd_username)
        self.tester.press_back(2)
        time.sleep(2)

        self.del_status()

    def cmp_nickname(self, nickname_res_id, after_avatar_res_id):
        """
        点击用户头像进入用户个人主页，判断点击前后昵称是否一致
        """
        ele_first_track_name = self.tester.find_element_by_id(
            nickname_res_id)
        ele_first_track_name_text = ele_first_track_name.text
        ele_first_track_name.click()

        # 兼容弱网环境
        self.tester.wait_element_for_a_while(after_avatar_res_id, 20)

        # 特定情况下点击头像后会遮盖顶部，直接显示动态，需要手动上滑刷新
        self.tester.swipe_up(2)
        after_user_name_res_id = "com.netease.cloudmusic:id/nickname"
        ele_personal_nickname = self.tester.find_element_by_id(
            after_user_name_res_id)
        self.assertEqual(ele_first_track_name_text,
                         ele_personal_nickname.text, "点击前后的昵称应该一样一样滴")
        time.sleep(3)

    def del_status(self):
        """
        恢复环境,避免下次执行出错
        """
        today_date = datetime.datetime.today().strftime('%Y-%m-%d')
        status_content_res_id = "com.netease.cloudmusic:id/trackDesc"
        ele_status_content = self.tester.find_element_by_id(
            status_content_res_id)
        count = 0
        while ele_status_content and today_date in ele_status_content.text and count < 50:
            count = count + 1
            if today_date in ele_status_content.text:
                if self.tester.is_element_exist(
                        "com.netease.cloudmusic:id/trackMoreBtn"):
                    self.tester.find_element_by_id_and_tap(
                        "com.netease.cloudmusic:id/trackMoreBtn")
                    time.sleep(2)
                    delete_text = "删除"
                    if self.tester.is_element_exist(delete_text):
                        self.tester.find_element_by_uiautomator_and_tap(
                            'new UiSelector().text("{}")'.format(delete_text))
                        time.sleep(2)
                        if self.tester.is_element_exist(delete_text):
                            self.tester.find_element_by_uiautomator_and_tap(
                                'new UiSelector().text("{}")'.format(delete_text))
                            time.sleep(2)
                    else:
                        # 不同测试帐号生成的动态
                        self.tester.press_back()
                        self.tester.swipe_down()
            else:
                self.tester.swipe_down()

    def common_ops(self):
        self.tester.wait_for_stable_main_page(10)

        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().description("我的推荐")')
        self.tester.wait_element_for_a_while("朋友", 10)

        error_msg = "入口朋友不在当前界面中，玩不下去了"
        self.assertTrue(self.tester.is_element_exist("朋友"), error_msg)

        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().text("朋友")')
        time.sleep(2)

    def enter_my_homepage(self):
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
                time.sleep(2)
            count = 0
            while not self.tester.is_element_exist("关注") and count < 10:
                time.sleep(2)
                count = count + 1

    def double_insurance_del(self):
        self.enter_my_homepage()
        moment = "动态"
        if (self.tester.is_element_exist(moment)):
            self.tester.find_element_by_uiautomator_and_tap(
                'new UiSelector().textStartsWith("{}")'.format(moment))
            time.sleep(2)
            is_bottom = False
            try:
                while not is_bottom:
                    start_page = self.tester.driver.page_source
                    # use md5 to compare the huge string
                    start_md5 = hashlib.md5(
                        start_page.encode('utf-8')).hexdigest()

                    if self.tester.is_element_exist(
                            "com.netease.cloudmusic:id/trackMoreBtn"):
                        self.tester.find_element_by_id_and_tap(
                            "com.netease.cloudmusic:id/trackMoreBtn")
                        time.sleep(2)
                        delete_text = "删除"
                        if self.tester.is_element_exist(delete_text):
                            self.tester.find_element_by_uiautomator_and_tap(
                                'new UiSelector().text("{}")'.format(delete_text))
                            time.sleep(2)
                            if self.tester.is_element_exist(delete_text):
                                self.tester.find_element_by_uiautomator_and_tap(
                                    'new UiSelector().text("{}")'.format(delete_text))
                                time.sleep(2)
                        else:
                            # 不同测试帐号生成的动态
                            self.tester.press_back()
                    else:
                        # 上滑
                        self.tester.swipe_down()
                    end_page = self.tester.driver.page_source
                    end_md5 = hashlib.md5(end_page.encode('utf-8')).hexdigest()
                    if start_md5 == end_md5:
                        is_bottom = True
            except Exception:
                self.tester.logger.error("Device:%s [action]swipe down to bottom failed"
                                         % self.tester.device.deviceName)
