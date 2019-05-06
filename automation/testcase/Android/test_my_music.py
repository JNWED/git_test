# -*- coding:utf-8 -*-

import sys
import time
import re
from common.basetestcase import BaseTestCase

sys.path.append('../..')


class TestMyMusic(BaseTestCase):
    """
    我的音乐测试类
    """

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.tester.logger.info("Device: %s Start case: %s" % (
            self.tester.device.deviceName, self._testMethodName))
        self.tester.double_check_login()
        self.common_ops()
        if (self._testMethodName == "test_my_music_01_offline_musics"):
            self.tester.clean_local_files()
            time.sleep(20)
            self.mock_data()

    def tearDown(self):
        '''
        tearDown
        '''
        self.tester.addfailscreenshot(self._testMethodName)
        self.tester.back_to_start()

    @classmethod
    def tearDownClass(cls):
        pass

    def test_my_music_01_offline_musics(self):
        """
        检查点击本地音乐进入开始扫描（首次进入），本地音乐可以正常扫描成功
        """
        time.sleep(2)
        self.tester.wait_element_for_a_while("本地音乐", 10)
        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().text("本地音乐")')
        time.sleep(2)

        # first installation will popup scan process, wait 3 minutes in maximum
        # until scan complete
        count = 0
        first_install_scan_keyword = "取消扫描"
        while (self.tester.is_element_exist(
                first_install_scan_keyword) and count < 36):
            time.sleep(5)
            count = count + 1
        complete_flag_text = "回到我的音乐"
        if self.tester.is_element_exist(complete_flag_text):
            self.tester.find_element_by_uiautomator_and_tap(
                'new UiSelector().text("{}")'.format(complete_flag_text))
            time.sleep(2)

        # 点击第一首歌正常播放
        song_name_res_id = "com.netease.cloudmusic:id/songName"
        self.assertTrue(self.tester.is_element_exist(
            song_name_res_id), "本地音乐中必须要有歌曲")
        self.tester.find_element_by_id_and_tap(song_name_res_id)
        time.sleep(2)

        # 弹出播放页面
        like_heart_desc = "红心"
        if (self.tester.is_element_exist(like_heart_desc)):
            self.tester.press_back()
            time.sleep(3)

        playing_trumpet_mark = "com.netease.cloudmusic:id/playingMark"
        self.tester.wait_element_for_a_while(playing_trumpet_mark, 10)
        info_text = "没找到播放的小喇叭标志呢"
        self.assertTrue(self.tester.is_element_exist(
            playing_trumpet_mark), info_text)

        first_song_res_id = "com.netease.cloudmusic:id/songInfo"
        self.tester.wait_element_for_a_while(first_song_res_id, 10)
        self.assertTrue(self.tester.is_element_exist(
            first_song_res_id), "未找到本地音乐中找到songInfo控件")
        before_song_info_list = self.tester.find_elements_by_id(
            first_song_res_id)
        self.assertIsNotNone(before_song_info_list, "本地音乐中未发现歌曲")

        before_singer_list = []
        before_albums_list = []
        for cur_song_info in before_song_info_list:
            temp_list = cur_song_info.text.decode('utf-8').strip().split("-")
            before_singer_list.append(temp_list[0].strip())
            before_albums_list.append(temp_list[1].strip())

        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().text("歌手")')
        time.sleep(2)
        after_singers_list = []
        after_ele_singer_list = self.tester.find_elements_by_id(
            song_name_res_id)
        self.assertIsNotNone(after_ele_singer_list, "本地音乐-歌手tab中歌手不能为空")

        for each_ele in after_ele_singer_list:
            after_singers_list.append(each_ele.text.decode('utf-8').strip())
        if sorted(before_singer_list) != sorted(after_singers_list):
            info_text = "本地音乐-单曲和歌手页面的所有歌手应该相同呢"
            self.tester.logger.info(
                "Device: %s %s" %
                (self.tester.device.deviceName, info_text))

        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().text("专辑")')
        after_ele_albums_list = self.tester.find_elements_by_id(
            song_name_res_id)
        self.assertIsNotNone(after_ele_albums_list, "本地音乐-专辑tab中歌手不能为空")

        after_albums_list = []
        for each_ele in after_ele_albums_list:
            after_albums_list.append(each_ele.text.decode('utf-8').strip())
        if sorted(before_albums_list) != sorted(after_albums_list):
            info_text = "本地音乐-单曲和专辑页面的所有专辑应该相同呢"
            self.tester.logger.info(
                "Device: %s %s" %
                (self.tester.device.deviceName, info_text))
        self.tester.press_back()

    def test_my_music_02_recently_played(self):
        """
        检查点击最近播放进入最近播放页面
        """
        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().text("最近播放")')
        time.sleep(1)
        if not self.tester.is_element_exist(
                "com.netease.cloudmusic:id/songNameAndInfoArea"):
            info_text = "最近播放中应该有播放记录哦"
            self.tester.logger.info(
                "Device: %s %s" %
                (self.tester.device.deviceName, info_text))

        # 检查滑动和点击可以切换四个tab
        self.tester.swipe_left(1)
        self.tester.swipe_right(1)

        self.tester.press_back()

    def test_my_music_03_download_music(self):
        """
        检查点击下载管理进入页面正确，单曲、电台节目、视频、下载中可以切换显示
        """
        # 点击可以进入相应的页面，后返回列表，最后返回我的音乐
        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().text("下载管理")')
        download_ele_music_id = "com.netease.cloudmusic:id/songNameAndInfoArea"
        self.tester.wait_element_for_a_while(download_ele_music_id, 10)
        ele_all_music_counts = self.tester.find_elements_by_id(
            download_ele_music_id)
        self.assertTrue(len(ele_all_music_counts) >= 5,
                        "下载管理Mock了5条数据，当前数据为:" + str(len(ele_all_music_counts)))

        dl_mgmt_tabs = ['单曲', '电台节目', '视频', '下载中 0']
        # 检查滑动和点击可以切换四个tab
        self.tester.swipe_left(3)
        self.tester.swipe_right(3)
        if not self.tester.is_element_exist(dl_mgmt_tabs[0]):
            info_text = "诶，来回滑动后没回到" + dl_mgmt_tabs[0]
            self.tester.logger.info(
                "Device: %s %s" %
                (self.tester.device.deviceName, info_text))
        self.tester.press_back()

    def test_my_music_04_my_stations(self):
        """
        检查我的电台页面进入正常
        """
        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().text("我的电台")')
        if self.tester.is_element_exist("加载失败，请点击重试"):
            info_text = "服务端出错，电台用例执行被Block"
            self.tester.logger.info(
                "Device: %s %s" %
                (self.tester.device.deviceName, info_text))

        # 播放一个正确的电台后退出
        first_station_res_id = "com.netease.cloudmusic:id/name"
        info_text = "未找到预先订阅的电台"
        self.assertTrue(self.tester.is_element_exist(
            first_station_res_id), info_text)

        self.tester.find_element_by_id_and_tap(first_station_res_id)

        # 兼容弱网环境以及服务器端偶发性延迟，最大等待30s
        first_station_record_id = "com.netease.cloudmusic:id/rcmdText"
        self.tester.wait_element_for_a_while(first_station_record_id, 30)

        info_text = "找不到电台节目"
        self.assertTrue(self.tester.is_element_exist(
            first_station_record_id), info_text)
        self.tester.find_element_by_id_and_tap(first_station_record_id)
        time.sleep(2)
        if self.tester.is_element_exist(first_station_record_id):
            self.tester.press_back()
            info_text = "没跳转到电台播放页面，出问题了呢"
            self.tester.logger.info(
                "Device: %s %s" %
                (self.tester.device.deviceName, info_text))
        self.tester.press_back(2)
        time.sleep(2)

        self.tester.press_back()

    def test_my_music_05_my_faved(self):
        """
        检查我的收藏页面进入正常，专辑、歌手、视频、专栏可以切换；
        """
        self.tester.wait_element_for_a_while("我的收藏", 20)
        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().text("我的收藏")')
        time.sleep(2)
        # 检查滑动和点击可以切换四个tab
        self.tester.swipe_left(3)
        self.tester.swipe_right(3)

        # --点击我的数字专辑进入我的数字专辑页面，
        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().text("我的数字专辑")')
        if self.tester.is_element_exist("暂无数字专辑"):
            info_text = "我花2元血汗钱买的数字专辑去哪了？"
            self.tester.logger.info(
                "Device: %s %s" %
                (self.tester.device.deviceName, info_text))
        before_artist_name = self.tester.find_element_by_id(
            "com.netease.cloudmusic:id/artist").text
        self.tester.find_element_by_id_and_tap(
            "com.netease.cloudmusic:id/image")
        time.sleep(2)
        after_artist_name = self.tester.find_element_by_id(
            "com.netease.cloudmusic:id/musicCreatorName").text
        if before_artist_name not in after_artist_name:
            info_text = "我滴霉霉呢"
            self.tester.logger.info(
                "Device: %s %s" %
                (self.tester.device.deviceName, info_text))
        self.tester.press_back(2)

        # 点击专辑进入对应专辑页面
        album_name_res_id = "com.netease.cloudmusic:id/name"
        if self.tester.is_element_exist(album_name_res_id):
            ele_album_name = self.tester.find_element_by_id(
                album_name_res_id)
            ele_album_name_text = ele_album_name.text
            ele_album_name.click()
            time.sleep(3)
            ele_after_album_title = self.tester.find_element_by_id(
                "com.netease.cloudmusic:id/musicTitle").text
            if ele_after_album_title != ele_album_name_text:
                info_text = "进入专辑后，专辑名称发生了变化"
                self.tester.logger.info(
                    "Device: %s %s" %
                    (self.tester.device.deviceName, info_text))
            self.tester.press_back(2)

    def mock_data(self):
        self.tester.logger.info(
            "Device: %s %s" %
            (self.tester.device.deviceName, "****************Begin Mock data**************"))

        mock_mix = "00-showcase"
        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().text("{}")'.format(mock_mix))

        if self.tester.is_element_exist("播放全部"):
            self.tester.find_element_by_uiautomator_and_tap(
                'new UiSelector().text("{}")'.format("播放全部"))
            self.tester.press_back()
            time.sleep(2)
        if self.tester.is_element_exist("下载"):
            self.tester.find_element_by_uiautomator_and_tap(
                'new UiSelector().text("下载")')
        if self.tester.is_element_exist("com.netease.cloudmusic:id/title"):
            self.tester.find_element_by_uiautomator_and_tap(
                'new UiSelector().textStartsWith("标准")')
        if self.tester.is_element_exist(
                "com.netease.cloudmusic:id/buttonDefaultPositive"):
            self.tester.find_element_by_uiautomator_and_tap(
                'new UiSelector().text("下载")')
        self.tester.press_back()
        time.sleep(2)

        self.common_ops()
        self.tester.wait_element_for_a_while("下载管理", 10)
        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().text("下载管理")')
        time.sleep(3)

        # 若在下载中，点击回到单曲页面
        downloading_flag_text = "全部暂停"
        self.tester.wait_element_for_a_while(downloading_flag_text, 10)
        if self.tester.is_element_exist(
                downloading_flag_text) or self.tester.is_element_exist("暂时没有内容"):
            self.tester.wait_element_for_a_while("单曲", 10)
            self.tester.driver.find_element_by_android_uiautomator(
                'new UiSelector().text("单曲")').click()
            time.sleep(2)

        count = 0
        total_download_number_id = 'com.netease.cloudmusic:id/musicsCount'
        self.tester.wait_element_for_a_while(total_download_number_id, 10)
        total_number_text = self.tester.find_element_by_id(
            total_download_number_id).text
        total_number = int(re.findall(r'\d+', total_number_text)[0])

        while total_number != 5 and count < 90:
            info_text = "Wait until complete all downloads - 2 seconds passed"
            self.tester.logger.info(
                "Device: %s %s" %
                (self.tester.device.deviceName, info_text))
            time.sleep(2)
            total_number_text = self.tester.find_element_by_id(
                total_download_number_id).text
            total_number = int(re.findall(r'\d+', total_number_text)[0])
            count = count + 1
        self.tester.press_back()
        self.tester.logger.info(
            "Device: %s %s" %
            (self.tester.device.deviceName, "**********************Complete Mocking data************************"))

    def common_ops(self):
        """
        进入我的音乐页面公共操作
        """
        self.tester.wait_for_stable_main_page(10)
        self.tester.wait_element_for_a_while("我的音乐", 10)
        error_msg = "Opps, Maybe you don't login"
        self.assertTrue(self.tester.is_element_exist("我的音乐"), error_msg)
        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().description("我的音乐")')
        time.sleep(3)
