# -*- coding:utf-8 -*-

import sys
import time
import datetime
from common.basetestcase import BaseTestCase

sys.path.append('../..')


class TestMusicPlayer(BaseTestCase):
    """
    歌曲播放器页面测试类
    """
    m_play_n_paused_content_desc = "播放暂停"
    m_song_name = "爱要坦荡荡"
    m_like_content_desc = "红心"

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

    def common_ops(self):
        # 检查搜索单曲点击进入单曲播放页面

        self.tester.search_keyword(TestMusicPlayer.m_song_name)
        if self.tester.is_element_exist(
                "com.netease.cloudmusic:id/songNameAndInfoArea"):
            self.tester.find_element_by_id_and_tap(
                "com.netease.cloudmusic:id/songNameAndInfoArea")

        self.play_song_ops()

        self.assertTrue(self.tester.is_element_exist(
            TestMusicPlayer.m_play_n_paused_content_desc), "播放暂停控件必须存在")
        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().description("{}")'.format(TestMusicPlayer.m_play_n_paused_content_desc))
        time.sleep(3)
        guideline_text = "轻触以查看歌词"
        if (self.tester.is_element_exist(guideline_text)):
            album_res_id = "com.netease.cloudmusic:id/smallAlbumCover0"
            self.tester.find_element_by_id_and_tap(album_res_id)
            time.sleep(2)
            self.tester.find_element_by_id_and_tap(
                "com.netease.cloudmusic:id/lrc")
            time.sleep(2)

    def test_music_player_01_player(self):
        self.tester.wait_for_stable_main_page(10)
        self.tester.clean_local_files()
        self.gen_play_record()

        self.common_ops()

        # 检查单曲操作--分享
        if self.tester.is_element_exist("分享"):
            self.tester.find_element_by_uiautomator_and_tap(
                'new UiSelector().description("分享")')
            time.sleep(3)
            cloudmusic_moments_text = "云音乐动态"
            if not self.tester.is_element_exist(cloudmusic_moments_text):
                error_msg = "未在分享页面找到" + cloudmusic_moments_text
                self.tester.logger.info(
                    "Device: %s %s" %
                    (self.tester.device.deviceName, error_msg))
                self.fail(error_msg)
            self.tester.find_element_by_uiautomator_and_tap(
                'new UiSelector().text("{}")'.format(cloudmusic_moments_text))
            time.sleep(2)
            mock_msg = str(datetime.datetime.now()) + "--从播放页发来一条动态"
            input_res_id = 'com.netease.cloudmusic:id/status'
            self.tester.send_one_msg(input_res_id, mock_msg, "分享")
            time.sleep(5)
            self.tester.wait_element_for_a_while(
                TestMusicPlayer.m_play_n_paused_content_desc, 20)

            error_msg = "分享操作后未回到播放页面"
            self.assertTrue(
                self.tester.is_element_exist(
                    TestMusicPlayer.m_play_n_paused_content_desc),
                error_msg)

    def test_music_player_02_save_n_dl(self):
        self.common_ops()

        # 检查单曲操作--收藏
        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().description("{}")'.format(TestMusicPlayer.m_like_content_desc))

        # 检查单曲操作--下载
        dl_content_desc = "下载"
        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().description("{}")'.format(dl_content_desc))
        if self.tester.is_element_exist("com.netease.cloudmusic:id/title"):
            self.tester.find_element_by_uiautomator_and_tap(
                'new UiSelector().textStartsWith("标准")')
            time.sleep(3)

        if self.tester.is_element_exist("下载到歌单"):
            self.tester.find_element_by_uiautomator_and_tap(
                'new UiSelector().text("{}")'.format("我喜欢的音乐"))
            time.sleep(3)

        # 检查单曲操作--评论
        comment_btn_res_id = "com.netease.cloudmusic:id/commentBtn"
        self.tester.find_element_by_id_and_tap(comment_btn_res_id)

        # 兼容弱网环境
        comment_section_id = "com.netease.cloudmusic:id/sectionName"
        self.tester.wait_element_for_a_while(comment_section_id, 30)
        self.tester.press_back()

        # 检查单曲操作--切歌 检查切歌后歌名发生变化
        next_song_content_desc = "下一首"
        last_song_content_desc = "上一首"
        self.assertTrue(self.tester.is_element_exist(
            next_song_content_desc), "下一首控件必须存在")
        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().description("{}")'.format(next_song_content_desc))
        self.tester.wait_element_for_a_while(TestMusicPlayer.m_song_name, 60)
        error_msg = "切歌失败，仍然在" + TestMusicPlayer.m_song_name + "播放页面"
        self.assertTrue(
            self.tester.is_element_exist(
                TestMusicPlayer.m_song_name),
            error_msg)

        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().description("{}")'.format(last_song_content_desc))
        self.tester.press_back(2)
        self.verify_my_favorites()

    def test_music_player_03_vip_download(self):
        self.tester.wait_for_stable_main_page(10)

        # 检查付费歌曲点击下载会有付费弹框（音乐包单曲）
        song_name = "富士山下"
        self.tester.search_keyword(song_name)
        if self.tester.is_element_exist(
                "com.netease.cloudmusic:id/songNameAndInfoArea"):
            self.tester.find_element_by_id_and_tap(
                "com.netease.cloudmusic:id/songNameAndInfoArea")

        self.play_song_ops()
        if self.tester.is_element_exist(
                TestMusicPlayer.m_play_n_paused_content_desc):
            self.tester.find_element_by_uiautomator_and_tap(
                'new UiSelector().description("{}")'.format(TestMusicPlayer.m_play_n_paused_content_desc))
            time.sleep(3)

        dl_content_desc = "下载"
        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().description("{}")'.format(dl_content_desc))
        time.sleep(2)

        vip_flag_text = "网易云音乐会员"
        # Wait for VIP Webview Page
        self.tester.wait_element_for_a_while(vip_flag_text, 60)

        if not self.tester.is_element_exist("确认支付"):
            error_msg = "未发现会员歌曲付费弹窗"
            self.tester.logger.info(
                "Device: %s %s" %
                (self.tester.device.deviceName, error_msg))
            self.assertIsNotNone(
                self.tester.is_element_exist("确认支付"), error_msg)
        self.tester.press_back(3)
        self.tester.clean_local_files()

    def gen_play_record(self):
        mock_exist_mix_name = "00-showcase"
        if self.tester.is_element_exist("我的音乐"):
            self.tester.find_element_by_uiautomator_and_tap(
                'new UiSelector().description("我的音乐")')
            time.sleep(2)
            self.tester.wait_element_for_a_while(mock_exist_mix_name, 10)
            self.tester.find_element_by_uiautomator_and_tap(
                'new UiSelector().text("{}")'.format(mock_exist_mix_name))
            playall_text = "播放全部"
            count = 0
            while not self.tester.is_element_exist(
                    playall_text) and count < 10:
                time.sleep(2)
                count = count + 1
            if self.tester.is_element_exist(playall_text):
                self.tester.find_element_by_uiautomator_and_tap(
                    'new UiSelector().text("{}")'.format(playall_text))
                self.tester.press_back(2)

    def play_song_ops(self):
        self.tester.wait_element_for_a_while(
            TestMusicPlayer.m_like_content_desc, 10)
        if not self.tester.is_element_exist(
                TestMusicPlayer.m_like_content_desc):
            if self.tester.is_element_exist(
                    "com.netease.cloudmusic:id/songNameAndInfoArea"):
                self.tester.find_element_by_id_and_tap(
                    "com.netease.cloudmusic:id/songNameAndInfoArea")
                time.sleep(3)

    def verify_my_favorites(self):
        self.tester.logger.info(
            "Device: %s %s" %
            (self.tester.device.deviceName, "开始验证红心功能"))

        self.tester.wait_element_for_a_while("我的音乐", 30)
        if not self.tester.is_element_exist("我的音乐"):
            error_msg = "切歌失败，仍然在" + TestMusicPlayer.m_song_name + "播放页面"
            self.tester.logger.info(
                "Device: %s %s" %
                (self.tester.device.deviceName, error_msg))
            self.fail(error_msg)

        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().description("我的音乐")')
        my_favorite_mix_text = "我喜欢的音乐"
        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().text("{}")'.format(my_favorite_mix_text))
        time.sleep(3)
        if not self.tester.is_element_exist(TestMusicPlayer.m_song_name):
            error_msg = "红心失败, 未找到歌曲" + TestMusicPlayer.m_song_name
            self.tester.logger.info(
                "Device: %s %s" %
                (self.tester.device.deviceName, error_msg))
            self.fail(error_msg)
        self.tester.press_back()
