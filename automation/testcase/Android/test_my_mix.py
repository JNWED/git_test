# -*- coding:utf-8 -*-

import sys
import time
import re
from common.basetestcase import BaseTestCase

sys.path.append('../..')


class TestCreateMix(BaseTestCase):
    """
    我的歌单测试类
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
        self.tester.back_to_start()

    @classmethod
    def tearDownClass(cls):
        pass

    def common_ops(self):
        """
        进入我的音乐页面公共操作
        """
        self.tester.wait_for_stable_main_page(10)
        my_music_entry_text = "我的音乐"
        self.tester.wait_element_for_a_while(my_music_entry_text, 10)
        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().description("{}")'.format(my_music_entry_text))
        time.sleep(5)

    def test_01_check_mix_count(self):
        """
        检查我收藏和创建的歌单展示正确
        """

        #To compatible with different screen resolution
        self.tester.swipe_down()
        mix_list_collection = self.tester.find_elements_by_id(
            "com.netease.cloudmusic:id/myMusicSectionName")
        self.assertIsNotNone(mix_list_collection, "创建和收藏的歌单section控件必须存在")

        # dirty_data_list = ["Taylor Swift 热门50单曲"]
        all_mixes_name_list = self.tester.find_elements_by_id(
            "com.netease.cloudmusic:id/name")

        mixes_created_by_me = mix_list_collection[0].text
        if len(all_mixes_name_list) == 3:
            self.assertEqual(
                int(re.findall(r'\d+', mixes_created_by_me)[0]), 2, "测试帐号创建的歌单只Mock了2个哦")

        mixes_saved_by_me = mix_list_collection[1].text
        self.assertEqual(
            int(re.findall(r'\d+', mixes_saved_by_me)[0]), 2, "测试帐号收藏的歌单只Mock了2个哦")

    def test_02_create_mix(self):
        """
        检查创建新歌单正确
        """
        self.tester.find_element_by_id_and_tap(
            "com.netease.cloudmusic:id/myMusicSectionOverflowBtn")
        time.sleep(2)
        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().text("创建新歌单")')

        input_edit_id = "android:id/input"
        error_msg = "没找到输入框"
        self.assertTrue(self.tester.is_element_exist(input_edit_id), error_msg)

        mock_mix_name = "00-autotest-mix"
        self.tester.send_one_msg(input_edit_id, mock_mix_name, "提交")

        self.tester.wait_element_for_a_while(mock_mix_name, 30)
        self.assertTrue(
            self.tester.is_element_exist(mock_mix_name),
            "歌单貌似没有创建成功诶")

        # 检查点击歌单进入对应的歌单页面
        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().text("{}")'.format(mock_mix_name))
        time.sleep(2)
        self.tester.wait_element_for_a_while(
            "com.netease.cloudmusic:id/musicCover", 20)
        self.assertTrue(self.tester.is_element_exist(
            "com.netease.cloudmusic:id/musicCover"), "歌单Cover控件必须存在")

        mix_name_res_id_inside = "com.netease.cloudmusic:id/musicTitle"
        self.tester.wait_element_for_a_while(mix_name_res_id_inside, 10)
        if not self.tester.is_element_exist(mix_name_res_id_inside):
            more_content_desc = "更多"
            if self.tester.is_element_exist(more_content_desc):
                self.tester.find_element_by_uiautomator_and_tap(
                    'new UiSelector().description("{}")'.format(more_content_desc))
                time.sleep(2)
                self.tester.press_back()
                time.sleep(2)

        self.tester.wait_element_for_a_while(mix_name_res_id_inside, 10)
        ele_mix_title = self.tester.find_element_by_id(mix_name_res_id_inside)
        self.assertEqual(
            ele_mix_title.text,
            mock_mix_name,
            "歌单名称应该为：" +
            mock_mix_name)
        time.sleep(1)
        self.tester.press_back()

    def test_03_delete_mix(self):
        """
        检查可以删除创建的歌单
        """
        mock_mix_name = "00-autotest-mix"
        self.tester.wait_element_for_a_while(mock_mix_name, 10)
        error_msg = "未找到刚创建的歌单" + mock_mix_name
        self.assertTrue(self.tester.is_element_exist(mock_mix_name), error_msg)
        ele_mix_created_justnow = self.tester.find_element_by_uiautomator(
            'new UiSelector().text("{}")'.format(mock_mix_name))

        dot_3_res_id = "com.netease.cloudmusic:id/actionBtn"
        ele_target_3dot = self.tester.get_same_line_element(
            ele_mix_created_justnow, dot_3_res_id, 0, 30)

        error_msg = "未找到刚创建的歌单" + mock_mix_name + "右侧的点点点"
        self.assertIsNotNone(ele_target_3dot, error_msg)
        ele_target_3dot.click()
        time.sleep(2)

        delete_text = "删除"
        error_msg = "没有找到删除选项"
        self.assertTrue(
            self.tester.is_element_exist(delete_text),
            error_msg)

        ele_del_btn = self.tester.find_element_by_uiautomator(
            'new UiSelector().text("{}")'.format(delete_text))
        ele_del_btn.click()
        time.sleep(1)
        if self.tester.is_element_exist(delete_text):
            ele_del_btn.click()

    def test_04_check_mix_cover(self):
        """
        检查点击歌单封面可以查看大图和保存封面
        """
        #To compatible with different screen resolution
        self.tester.swipe_down()
        mock_exist_mix_name = "00-showcase"
        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().text("{}")'.format(mock_exist_mix_name))

        cover_res_id = "com.netease.cloudmusic:id/musicCover"
        self.tester.wait_element_for_a_while(cover_res_id, 20)
        error_msg = "封面控件不存在"
        self.assertTrue(self.tester.is_element_exist(cover_res_id), error_msg)
        self.tester.find_element_by_id_and_tap(cover_res_id)
        self.tester.wait_element_for_a_while("保存封面", 20)
        error_msg = "没找到保存封面按钮"
        self.assertTrue(self.tester.is_element_exist("保存封面"), error_msg)

        error_msg = "没找到封面大图控件"
        self.assertTrue(self.tester.is_element_exist, error_msg)
        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().text("{}")'.format("保存封面"))
        time.sleep(2)
