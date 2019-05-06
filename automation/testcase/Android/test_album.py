# -*- coding:utf-8 -*-
import sys
import time
import re
from common.basetestcase import BaseTestCase

sys.path.append('../..')


class TestAlbum(BaseTestCase):
    """
    专辑测试类
    """
    m_singer = "Goose house"
    m_mock_search_album = "笑顔の花"

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.tester.logger.info("Device: %s Start case: %s" % (
            self.tester.device.deviceName, self._testMethodName))
        self.tester.wait_for_stable_main_page(10)
        self.tester.double_check_login()

    def tearDown(self):
        '''
        tearDown
        '''
        self.tester.addfailscreenshot(self._testMethodName)

        # 清除测试中间数据
        if (self._testMethodName == "test_album_03_download_album"):
            self.cancel_subscribe()
            self.tester.clean_local_files()

        self.tester.back_to_start()

    @classmethod
    def tearDownClass(cls):
        pass

    def test_album_01_basic_function(self):
        """
        专辑页
        """
        self.common_ops()

        self.assertTrue(self.tester.is_element_exist(
            "com.netease.cloudmusic:id/musicCreatorName"))
        self.tester.find_element_by_id_and_tap(
            "com.netease.cloudmusic:id/musicCreatorName")
        time.sleep(2)

        # 检查点击歌手跳转到歌手页面
        self.assertTrue(self.tester.is_element_exist(
            'com.netease.cloudmusic:id/subscribeBtn'))
        self.tester.press_back()

        # 检查歌曲有视频的点击视频跳转视频页面
        self.assertTrue(self.tester.is_element_exist(
            "com.netease.cloudmusic:id/songItemVideoBtn"), "专辑中应至少存在一个视频按钮")
        self.tester.find_element_by_id_and_tap(
            "com.netease.cloudmusic:id/songItemVideoBtn")

        popup_window_text = "相关视频"
        video_icon_res_id = "com.netease.cloudmusic:id/videoTitle"
        if self.tester.is_element_exist(popup_window_text):
            self.tester.find_element_by_id_and_tap(video_icon_res_id)
            time.sleep(2)

        # 兼容首次加载视频无缓存情况
        mv_name_res_id = "com.netease.cloudmusic:id/mvName"
        self.tester.wait_element_for_a_while(
            "com.netease.cloudmusic:id/mvName", 30)

        error_msg = "未找到MV名称字段,请确认是否跳转到视频播放界面"
        self.assertTrue(
            self.tester.is_element_exist(mv_name_res_id),
            error_msg)
        self.tester.press_back(2)

        # 检查查看专辑评论
        self.tester.find_element_by_id_and_tap(
            "com.netease.cloudmusic:id/commentBlock")
        time.sleep(3)
        if self.tester.is_element_exist(
                "com.netease.cloudmusic:id/commentResInfo"):
            ele_singer_name = self.tester.find_element_by_id(
                "com.netease.cloudmusic:id/commentResInfo")
            self.assertEqual(
                ele_singer_name.text.strip(),
                TestAlbum.m_singer,
                "MV视频页中找不到歌手" + TestAlbum.m_singer)
            self.tester.press_back()

        # 检查点击专辑多选跳转多选页面
        error_msg = "没有多选按钮"
        self.assertTrue(self.tester.is_element_exist("多选"), error_msg)

        before_total_musics = self.tester.find_element_by_id(
            "com.netease.cloudmusic:id/musicsCount").text
        before_total_musics_count = int(
            re.findall(r'\d+', before_total_musics)[0])
        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().text("多选")')
        time.sleep(2)
        after_total_musics = len(self.tester.find_elements_by_id(
            "com.netease.cloudmusic:id/checkedImage"))
        error_msg = "多选页面存在问题"
        self.assertTrue(self.tester.is_element_exist(
            "全选") or before_total_musics_count != after_total_musics, error_msg)
        self.tester.press_back()

    def test_album_02_subscribe_album(self):
        """
        检查专辑--收藏下载
        """
        self.common_ops()
        time.sleep(5)
        subsribe_btn_res_id = "com.netease.cloudmusic:id/subscribePlAlBtn"
        subsribed_btn_res_id = "com.netease.cloudmusic:id/subscribedPlAlBtn"
        if self.tester.is_element_exist(subsribed_btn_res_id):
            self.tester.logger.info(
                "Device: %s %s" %
                (self.tester.device.deviceName, TestAlbum.m_mock_search_album + "专辑已被收藏，进行取消收藏操作"))
            self.tester.find_element_by_id_and_tap(subsribed_btn_res_id)
            if (self.tester.is_element_exist("不再收藏")):
                self.tester.find_element_by_uiautomator_and_tap(
                    'new UiSelector().text("不再收藏")')
                time.sleep(2)

        self.assertTrue(self.tester.is_element_exist(subsribe_btn_res_id)
                        or self.tester.is_element_exist(subsribed_btn_res_id), "收藏或取消收藏控件必须存在")

        if self.tester.is_element_exist(subsribe_btn_res_id):
            self.tester.find_element_by_id_and_tap(subsribe_btn_res_id)
            time.sleep(3)
            confirm_text_res_id = "com.netease.cloudmusic:id/buttonDefaultPositive"
            try:
                ele_confirm_btn = self.tester.driver.find_element_by_id(
                    confirm_text_res_id)
                if ele_confirm_btn:
                    ele_confirm_btn.click()
                    time.sleep(2)
            except Exception:
                self.tester.logger.info(
                    "Device: %s %s" %
                    (self.tester.device.deviceName, "非首次运行，不会提示知道了"))
            self.tester.press_back(2)
            time.sleep(2)

        # 收藏成功后在我的收藏可以找到
        self.enter_my_music_page()
        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().text("我的收藏")')
        self.tester.wait_element_for_a_while("专辑", 20)
        self.assertTrue(self.tester.is_element_exist("专辑"), "未找到专辑Tab")
        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().textStartsWith("专辑")')
        time.sleep(2)
        error_msg = "未找到收藏的专辑: " + TestAlbum.m_mock_search_album
        self.tester.wait_element_for_a_while(TestAlbum.m_mock_search_album, 10)
        self.assertTrue(self.tester.is_element_exist(
            TestAlbum.m_mock_search_album), error_msg)
        self.tester.press_back()
        time.sleep(2)

        self.cancel_subscribe()

    def test_album_03_download_album(self):
        self.common_ops()

        dl_keyword = "下载"
        self.assertTrue(
            self.tester.is_element_exist(dl_keyword),
            "专辑页面下载控件必须存在")
        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().text("{}")'.format(dl_keyword))
        time.sleep(2)
        if self.tester.is_element_exist("com.netease.cloudmusic:id/title"):
            self.tester.find_element_by_uiautomator_and_tap(
                'new UiSelector().textStartsWith("标准")')
        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().text("{}")'.format(dl_keyword))

        # 等待下载完成，若下载未完成，我的音乐页面->下载管理会不断刷新下载进度导致appium找到元素后不点击,最后TimeoutException
        count = 0
        while count < 16 and self.tester.is_element_exist("播放全部"):
            time.sleep(5)
            count = count + 1
        self.tester.press_back(2)

        # 下载后在下载管理能找到专辑全部单曲
        self.enter_my_music_page()
        dl_mgmt_keyword = "下载管理"
        self.tester.wait_element_for_a_while(dl_mgmt_keyword, 30)
        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().text("{}")'.format(dl_mgmt_keyword))
        time.sleep(2)

        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().text("单曲")')
        self.tester.wait_element_for_a_while(TestAlbum.m_singer, 60)
        error_msg = "没能找到刚才下载的" + TestAlbum.m_singer + "的歌曲"
        self.assertTrue(TestAlbum.m_singer, error_msg)

        self.tester.press_back()
        time.sleep(2)

    def common_ops(self):
        self.tester.wait_for_stable_main_page(15)

        # 检查搜索XX专辑，专辑tab搜索结果点击进入专辑页面
        self.tester.search_keyword(TestAlbum.m_mock_search_album)

        self.assertTrue(self.tester.is_element_exist("专辑"), "未找到专辑TAB")
        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().text("专辑")')
        time.sleep(3)

        # 点击专辑列表中第一个专辑
        error_msg = "专辑列表为空"
        self.assertTrue(self.tester.is_element_exist(
            "com.netease.cloudmusic:id/albumName"), error_msg)
        self.tester.find_element_by_id_and_tap(
            "com.netease.cloudmusic:id/albumName")
        time.sleep(3)

    def cancel_subscribe(self):
        self.tester.logger.info(
            "Device: %s %s" %
            (self.tester.device.deviceName, "Start Cancel album subscribtion"))

        # 收藏成功和下载后在我的收藏可以找到
        self.enter_my_music_page()
        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().text("我的收藏")')
        self.tester.wait_element_for_a_while("专辑", 20)
        self.assertTrue(self.tester.is_element_exist("专辑"), "未找到专辑Tab")
        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().textStartsWith("专辑")')
        time.sleep(2)

        # 清除操作痕迹，能够重复运行收藏专辑用例
        if (self.tester.is_element_exist(TestAlbum.m_mock_search_album)):
            ele_target_album = self.tester.find_element_by_uiautomator(
                'new UiSelector().text("{}")'.format(TestAlbum.m_mock_search_album))
            dot_3_res_id = "com.netease.cloudmusic:id/action"
            ele_target_3dot = self.tester.get_same_line_element(
                ele_target_album, dot_3_res_id, 0, 40)
            self.assertIsNotNone(ele_target_3dot, "没能找到点点点控件")
            ele_target_3dot.click()
            time.sleep(2)
            delete_text = "删除"
            if self.tester.is_element_exist(delete_text):
                self.tester.find_element_by_uiautomator_and_tap(
                    'new UiSelector().text("{}")'.format(delete_text))
                time.sleep(1)
                if self.tester.is_element_exist("同时删除下载文件"):
                    self.tester.find_element_by_uiautomator_and_tap(
                        'new UiSelector().text("同时删除下载文件")')
                    time.sleep(2)
                if self.tester.is_element_exist(delete_text):
                    self.tester.find_element_by_uiautomator_and_tap(
                        'new UiSelector().text("{}")'.format(delete_text))
        self.tester.press_back()
        self.tester.logger.info(
            "Device: %s %s" %
            (self.tester.device.deviceName, "End Cancel album subscribtion"))

    def enter_my_music_page(self):
        """
        进入我的音乐页面
        """
        self.tester.wait_for_stable_main_page(10)
        my_music_content_desc = "我的音乐"
        error_msg = "Opps, Maybe you don't login"
        self.assertTrue(self.tester.is_element_exist(
            my_music_content_desc), error_msg)
        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().description("{}")'.format(my_music_content_desc))
        time.sleep(2)
