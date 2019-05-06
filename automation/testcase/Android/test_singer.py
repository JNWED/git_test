# -*- coding:utf-8 -*-

import sys
import time
from common.basetestcase import BaseTestCase

sys.path.append('../..')


class TestSingerPage(BaseTestCase):
    """
    歌手页测试类
    """

    m_singer = "G.E.M.邓紫棋"

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
        self.tester.wait_element_for_a_while("我的音乐", 10)
        if self.tester.is_element_exist("我的音乐"):
            self.tester.find_element_by_uiautomator_and_tap(
                'new UiSelector().description("我的音乐")')
            time.sleep(2)
            mock_mix_name = TestSingerPage.m_singer + " 热门50单曲"
            self.click_3dots_and_delete(mock_mix_name)
            time.sleep(2)
        self.tester.back_to_start()

    @classmethod
    def tearDownClass(cls):
        pass

    def test_singer_01_artist(self):
        # Unsubscribe first, incase redundant operation case failer
        self.unsubscribe_artist()

        # 检查歌手可以点击收藏
        subscribe_artist_text = "收 藏"
        personal_page_text = "个人主页"

        self.tester.wait_element_for_a_while(personal_page_text, 10)
        self.assertTrue(self.tester.is_element_exist(
            personal_page_text), "没能跳转到歌手页面")
        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().text("{}")'.format(subscribe_artist_text))
        time.sleep(2)
        positive_text = "知道了"
        if self.tester.is_element_exist(positive_text):
            self.tester.find_element_by_uiautomator_and_tap(
                'new UiSelector().text("{}")'.format(positive_text))
            time.sleep(2)

        # 检查top50歌曲点击可以播放
        self.assertTrue(self.tester.is_element_exist(
            "com.netease.cloudmusic:id/songName"), "歌曲列表中必须有至少一首单曲")
        self.tester.find_element_by_id_and_tap(
            "com.netease.cloudmusic:id/songName")
        time.sleep(2)

        # 弹出播放页面
        like_heart_desc = "红心"
        minibar_song_title_res_id = "com.netease.cloudmusic:id/musicName"
        if not self.tester.is_element_exist(like_heart_desc):
            self.tester.find_element_by_id_and_tap(minibar_song_title_res_id)
            time.sleep(3)

        error_msg = "播放歌曲后未在播放界面中找到红心控件"
        self.assertTrue(
            self.tester.is_element_exist(like_heart_desc),
            error_msg)
        self.tester.press_back()
        time.sleep(2)

        # Unsubscribe, incase redundant operation case failer
        self.unsubscribe_artist()
        time.sleep(2)
        self.tester.press_back(2)

    def test_singer_02_ui(self):

        # 检查歌手页top50、专辑、视频、歌手信息四个tab显示正确
        artist_tab_list = ["热门演唱", "专辑", "视频", "艺人信息"]
        self.tester.swipe_left(3)
        self.tester.swipe_right(3)
        wifi_or_server_warning = "加载失败，请点击重试"
        if self.tester.is_element_exist(wifi_or_server_warning):
            self.tester.find_element_by_uiautomator_and_tap(
                'new UiSelector().text("{}")'.format(wifi_or_server_warning))
            time.sleep(2)
        self.tester.wait_element_for_a_while(artist_tab_list[0], 10)
        error_msg = "诶，来回滑动后没回到" + artist_tab_list[0]
        self.assertTrue(
            self.tester.is_element_exist(
                artist_tab_list[0]),
            error_msg)
        time.sleep(3)

        # 检查收藏热门50单曲
        save_hotest_50_songs = "收藏热门50单曲"
        if self.tester.is_element_exist(save_hotest_50_songs):
            self.tester.find_element_by_uiautomator_and_tap(
                'new UiSelector().text("{}")'.format(save_hotest_50_songs))
            time.sleep(2)
            create_as_new_mix = "创建为新歌单"
            if self.tester.is_element_exist(create_as_new_mix):
                self.tester.find_element_by_uiautomator_and_tap(
                    'new UiSelector().text("{}")'.format(create_as_new_mix))
                time.sleep(2)

        # 检查点击歌曲相关视频跳转视频页面
        first_video_btn_res_id = "com.netease.cloudmusic:id/songItemVideoBtn"
        self.tester.wait_element_for_a_while(first_video_btn_res_id, 10)
        if self.tester.is_element_exist(first_video_btn_res_id):
            self.tester.find_element_by_id_and_tap(first_video_btn_res_id)
            time.sleep(2)

        popup_window_text = "相关视频"
        video_icon_res_id = "com.netease.cloudmusic:id/videoTitle"
        self.tester.wait_element_for_a_while(popup_window_text, 10)
        if self.tester.is_element_exist(popup_window_text):
            self.tester.find_element_by_id_and_tap(video_icon_res_id)
            time.sleep(2)

        # 兼容首次加载视频无缓存情况
        mv_name_res_id = "com.netease.cloudmusic:id/mvName"
        self.tester.wait_element_for_a_while(mv_name_res_id, 20)
        error_msg = "未找到MV名称字段"
        self.assertTrue(
            self.tester.is_element_exist(mv_name_res_id),
            error_msg)
        self.tester.press_back(2)

        # 检查点击视频跳转MV/视频详情页
        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().textStartsWith("{}")'.format(artist_tab_list[2]))
        time.sleep(2)
        error_msg = "未找到MV名称字段"
        self.assertTrue(self.tester.is_element_exist(
            "com.netease.cloudmusic:id/mvImage"), error_msg)

        # 检查歌手信息tab显示歌手简介
        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().text("{}")'.format(artist_tab_list[3]))
        time.sleep(2)
        exist_flag = TestSingerPage.m_singer + "简介"
        ele_brief_intro = self.tester.find_element_by_id(
            "com.netease.cloudmusic:id/artistIntroTitle")
        self.assertEqual(
            exist_flag,
            ele_brief_intro.text,
            artist_tab_list[3] +
            "页的简介标题应该为" +
            exist_flag)

        self.tester.press_back(2)

    def common_ops(self):
        self.tester.wait_for_stable_main_page(15)
        self.tester.search_keyword(TestSingerPage.m_singer)

        # 检查点击歌手跳转到歌手页面
        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().text("歌手")')
        time.sleep(2)
        self.tester.wait_element_for_a_while(
            "com.netease.cloudmusic:id/artistName", 10)
        self.tester.find_element_by_id_and_tap(
            "com.netease.cloudmusic:id/artistName")
        time.sleep(2)

    def unsubscribe_artist(self):
        already_subscribe = "已收藏"
        if self.tester.is_element_exist(already_subscribe):
            self.tester.find_element_by_uiautomator_and_tap(
                'new UiSelector().text("{}")'.format(already_subscribe))
            time.sleep(3)

    def click_3dots_and_delete(self, mock_mix_name):
        if self.tester.is_element_exist(mock_mix_name):
            ele_mix_created_justnow = self.tester.find_element_by_uiautomator(
                'new UiSelector().text("{}")'.format(mock_mix_name))
            dot_3_res_id = "com.netease.cloudmusic:id/actionBtn"
            ele_target_3dot = self.tester.get_same_line_element(
                ele_mix_created_justnow, dot_3_res_id, 0, 30)

            if ele_target_3dot:
                ele_target_3dot.click()
                time.sleep(2)

                delete_text = "删除"
                error_msg = "没有找到删除选项"
                self.assertTrue(
                    self.tester.is_element_exist(delete_text), error_msg)

                self.tester.find_element_by_uiautomator_and_tap(
                    'new UiSelector().text("{}")'.format(delete_text))
                time.sleep(2)
                if self.tester.is_element_exist(delete_text):
                    self.tester.find_element_by_uiautomator_and_tap(
                        'new UiSelector().text("{}")'.format(delete_text))
                    time.sleep(2)
            else:
                self.tester.logger.info("Device: %s Failed get the 3dot in same line with mix: %s" % (
                    self.tester.device.deviceName, self._testMethodName))
