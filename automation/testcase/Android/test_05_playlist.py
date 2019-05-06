# -*- coding:utf-8 -*-
import sys
import time
from common.basetestcase import BaseTestCase
sys.path.append('../..')


class TestPlaylist(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.tester.logger.info("Device: %s Start case: %s" % (
            self.tester.device.deviceName, self._testMethodName))
        self.tester.wait_for_stable_main_page(10)
        myrcmd_ele = self.tester.driver.find_element_by_accessibility_id(
            "我的推荐")
        self.assertIsNotNone(myrcmd_ele, "没有找到我的推荐按钮")
        myrcmd_ele.click()
        time.sleep(2)
        self.tester.driver.find_element_by_android_uiautomator(
            'new UiSelector().text("推荐")').click()
        time.sleep(2)

    # 检查首页推荐龙珠操作正常
    def test_playlist_00_open(self):
        # 打开推荐歌单页面
        time.sleep(2)
        music_list = self.tester.find_element_by_uiautomator(
            'new UiSelector().text("歌单")')
        self.assertIsNotNone(music_list, "未能找到歌单")
        music_list.click()
        time.sleep(1)
        if self.tester.is_element_exist(
                'com.netease.cloudmusic:id/playlistHeaderTitle'):
            self.tester.logger.info(
                "设备: %s 打开推荐歌单列表页" % (self.tester.device.deviceName))
        else:
            self.tester.logger.info(
                    "设备: %s 没有找到推荐歌单页面的playlistHeaderTitle" % (self.tester.device.deviceName))
        time.sleep(1)
        rcmdtag1_ele = self.tester.find_element_by_id(
            'com.netease.cloudmusic:id/rcmdTag1')
        self.assertIsNotNone(rcmdtag1_ele, "未能找到ID:rcmdTag1")
        rcmdtag1_name = rcmdtag1_ele.text
        rcmdtag1_ele.click()
        self.tester.logger.info(
            "设备: %s 点击 %s 歌单类别" % (self.tester.device.deviceName, rcmdtag1_name))
        time.sleep(1)
        chooseclass_ele = self.tester.find_element_by_id(
            'com.netease.cloudmusic:id/chooseClass')

        self.assertIsNotNone(chooseclass_ele, "未能找到ID:chooseClass")
        chooseclass_name = chooseclass_ele.text
        self.assertEqual(chooseclass_name, rcmdtag1_name, msg="分类显示错误")
        time.sleep(1)
        playlistcover_1 = self.tester.find_element_by_id(
            'com.netease.cloudmusic:id/playListCover')

        playlistname_ele = self.tester.find_element_by_id(
            'com.netease.cloudmusic:id/findPlayListName')
        self.assertIsNotNone(playlistcover_1, "未能找到ID:playListCover")
        self.assertIsNotNone(playlistname_ele, "未能找到ID:findPlayListName")
        playlistname = playlistname_ele.text
        playlistcover_1.click()
        self.tester.logger.info(
            "设备: %s 点击进入 %s 歌单" % (self.tester.device.deviceName, playlistname))
        time.sleep(2)
        playlistmusictitle_ele = self.tester.find_element_by_id(
            'com.netease.cloudmusic:id/musicTitle')
        self.assertIsNotNone(playlistmusictitle_ele, "歌单页面打开失败")
        playlistmusictitle_name = playlistmusictitle_ele.text

        self.tester.logger.info(
            "设备: %s %s 歌单页面打开" % (self.tester.device.deviceName, playlistname))
        self.assertEqual(
            playlistmusictitle_name,
            playlistname,
            msg="歌单名不匹配")


    def tearDown(self):
        self.tester.addfailscreenshot(self._testMethodName)
        self.tester.back_to_start()

    @classmethod
    def tearDownClass(cls):
        pass
