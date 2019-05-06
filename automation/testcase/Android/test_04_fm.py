# -*- coding:utf-8 -*-

import sys
import time
from common.basetestcase import BaseTestCase
sys.path.append('../..')


class TestFm(BaseTestCase):
    """
    FM页面测试类
    """
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.tester.logger.info("Device: %s Start case: %s" % (
            self.tester.device.deviceName, self._testMethodName))
        time.sleep(5)

    def test_fm_00_play(self):

        self.tester.find_element_by_id_and_tap(
            'com.netease.cloudmusic:id/mainPageHeaderFm')
        time.sleep(2)
        
        # 首次进入的提示弹框，检查点击知道了
        if self.tester.is_element_exist(
                "com.netease.cloudmusic:id/commonIntroducationBtnTrySecond"):
            self.tester.find_element_by_id_and_tap(
                'com.netease.cloudmusic:id/commonIntroducationBtnTrySecond')
            time.sleep(2)
        else:
            self.tester.logger.info(
                "设备: %s FM页面没有出现提示弹框" % (self.tester.device.deviceName))

        #兼容FM页面获取不到数据的情况
        i = 0
        while i < 3:
            self.tester.find_element_by_id_and_tap(
            'com.netease.cloudmusic:id/nextBtn')
            time.sleep(5)
            if self.tester.is_element_exist(
                'com.netease.cloudmusic:id/musicName'):
                break
        fm_music_name = self.tester.find_element_by_id(
            'com.netease.cloudmusic:id/musicName')
        self.assertIsNotNone(fm_music_name, "fm页面加载歌曲失败")

        # 评论上滑引导(第一次进入不出现)
        if self.tester.is_element_exist(
                "com.netease.cloudmusic:id/commentGuideText"):
            time.sleep(1)
            self.tester.find_element_by_id_and_tap(
                'com.netease.cloudmusic:id/commentGuideText')
            time.sleep(2)
        else:
            self.tester.logger.info(
                "设备: %s FM页面没有出现上滑引导弹框" % (self.tester.device.deviceName))

        fm_musicname_ele = self.tester.find_element_by_id(
            'com.netease.cloudmusic:id/musicName')
        self.assertIsNotNone(fm_musicname_ele, msg="FM歌曲播放失败")
        self.tester.driver.back()

        # FM返回主页面会有添加添加快捷方式的弹框(只弹一次),弹框消失后直接返回主页
        if self.tester.is_element_exist(
                "com.netease.cloudmusic:id/buttonDefaultNegative"):
            time.sleep(1)
            self.tester.find_element_by_id_and_tap(
                'com.netease.cloudmusic:id/buttonDefaultNegative')
            self.tester.logger.info(
                "设备: %s FM页面点击添加快捷方式弹框" % (self.tester.device.deviceName))
        else:
            self.tester.logger.info(
                "设备: %s FM页面没有出现添加快捷方式弹框" % (self.tester.device.deviceName))

        # 检查首页mini播放条播放的单曲与FM一致
        # self.tester.is_element_exist('com.netease.cloudmusic:id/mainPageHeaderFm')
        mini_name = self.tester.find_element_by_id(
            'com.netease.cloudmusic:id/musicName')
        if mini_name:
            self.assertIsNotNone(mini_name, "FM播放歌曲失败，首页无mini播放条")
            self.assertEqual(
                mini_name.text,
                fm_musicname_ele.text,
                msg="FM歌曲与mini播放条不一致")
            time.sleep(2)
            # 点击mini进入FM页面
            self.tester.find_element_by_id_and_tap(
                'com.netease.cloudmusic:id/musicName')
            self.tester.logger.info(
                "设备: %s FM播放单曲正常" % (self.tester.device.deviceName))
        else:
            self.tester.logger.info(
                "设备: %s 首页没有出现mini播放条" % (self.tester.device.deviceName))

    # 检查FM进入歌手页正确
    def test_fm_01_fmartist(self):
        self.tester.find_element_by_id_and_tap(
            'com.netease.cloudmusic:id/mainPageHeaderFm')
        time.sleep(2)
        i = 0
        while i < 3:
            self.tester.find_element_by_id_and_tap(
            'com.netease.cloudmusic:id/nextBtn')
            time.sleep(5)
            if self.tester.is_element_exist(
                'com.netease.cloudmusic:id/artistName'):
                break
        fm_music_name = self.tester.find_element_by_id(
            'com.netease.cloudmusic:id/musicName')
        self.assertIsNotNone(fm_music_name, "fm页面加载歌曲失败")
        artistname = self.tester.find_element_by_id(
            'com.netease.cloudmusic:id/artistName')
        self.assertIsNotNone(artistname, "进入歌手页失败")
        artistname.click()
        time.sleep(2)
        # 多歌手情况需要选择
        if self.tester.is_element_exist("请选择要查看的歌手"):
            self.tester.logger.info(
                "设备: %s FM播放的单曲是多歌手歌曲" % (self.tester.device.deviceName))
            time.sleep(2)
            artists = self.tester.driver.find_elements_by_id(
                'com.netease.cloudmusic:id/menuTitle')
            artists[0].click()
            time.sleep(2)
        else:
            self.tester.logger.info(
                "设备: %s FM播放的单曲是单歌手歌曲" % (self.tester.device.deviceName))

        # 歌手页暂时无法获取歌手名
        if self.tester.is_element_exist("热门演唱"):
            self.tester.logger.info(
                 "设备: %s 打开歌手页成功" % (self.tester.device.deviceName))
            time.sleep(2)
            self.tester.driver.back()
        else:
            self.tester.logger.info(
                "设备: %s 找不到：歌手页热门演唱" % (self.tester.device.deviceName))

    # 检查FM进入评论页
    def test_fm_02_fmcomment(self):
        self.skipTest("skip fm_02_fmcomment due to stablity issue")
        self.tester.find_element_by_id_and_tap(
            'com.netease.cloudmusic:id/mainPageHeaderFm')
        time.sleep(3)
        i = 0
        while i < 3:
            self.tester.find_element_by_id_and_tap(
            'com.netease.cloudmusic:id/nextBtn')
            time.sleep(5)
            if self.tester.is_element_exist(
                'com.netease.cloudmusic:id/musicName'):
                break
        musicname = self.tester.find_element_by_id(
            'com.netease.cloudmusic:id/musicName')
        music_name = musicname.text
        commentbtn = self.tester.find_element_by_id(
            'com.netease.cloudmusic:id/commentBtn')
        self.assertIsNotNone(commentbtn, "FM没有找到评论按钮")
        self.tester.logger.info(
            "设备: %s FM找到评论按钮" %
            (self.tester.device.deviceName))
        self.tester.find_element_by_id_and_tap(
            'com.netease.cloudmusic:id/commentBtn')
        # 兼容点击不跳转就再多点击一次
        if self.tester.is_element_exist('com.netease.cloudmusic:id/commentBtn'):
            self.tester.find_element_by_id_and_tap(
            'com.netease.cloudmusic:id/commentBtn')
            self.tester.logger.info(
            "设备: %s FM第二次找到评论按钮并点击" %
            (self.tester.device.deviceName))
        try:
            self.tester.wait_element_id_display(self.tester.driver, 
            'com.netease.cloudmusic:id/commentResName', "没有找到评论页面的资源名", 10)
            self.tester.logger.info(
                "设备: %s FM进入评论页面找到评论资源名" %
                (self.tester.device.deviceName))
            comm_resname = self.tester.find_element_by_id(
                'com.netease.cloudmusic:id/commentResName')
        except:
            self.tester.wait_element_id_display(self.tester.driver, 
            'com.netease.cloudmusic:id/commentResName', "没有找到评论页面的资源名", 10)
            comm_resname = self.tester.find_element_by_id(
                'com.netease.cloudmusic:id/commentResName')
            self.tester.logger.info(
                "设备: %s FM进入评论页面找到评论资源名" %
                (self.tester.device.deviceName))
        self.assertIsNotNone(comm_resname, "可能没有进入评论页面")
        self.assertEqual(
            comm_resname.text,
            music_name,
            msg="FM评论资源不匹配")
        self.tester.logger.info(
            "设备: %s FM正常打开评论页面" %
            (self.tester.device.deviceName))
        time.sleep(2)
        self.tester.driver.back()

    # 检查FM页面切歌成功
    def test_fm_03_playnext(self):
        self.tester.find_element_by_id_and_tap(
            'com.netease.cloudmusic:id/mainPageHeaderFm')
        fm_cur_musicname = self.tester.find_element_by_id(
            'com.netease.cloudmusic:id/musicName')
        self.tester.find_element_by_id_and_tap(
            'com.netease.cloudmusic:id/nextBtn')
        time.sleep(2)
        fm_nex_musicname = self.tester.find_element_by_id(
            'com.netease.cloudmusic:id/musicName')
        if not self.assertEqual(fm_cur_musicname.text, fm_nex_musicname.text):
            self.tester.logger.info(
                "设备: %s FM页面切歌成功" %
                (self.tester.device.deviceName))
        else:
            self.tester.logger.info(
                "设备: %s FM下一首歌曲获取失败" %
                (self.tester.device.deviceName))

    def tearDown(self):
        self.tester.addfailscreenshot(self._testMethodName)
        self.tester.back_to_start()

    @classmethod
    def tearDownClass(cls):
        pass
