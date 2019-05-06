# -*- coding:utf-8 -*-

import sys
import datetime
import time
import os
from common.basetestcase import BaseTestCase

sys.path.append('../..')
print os.getcwd()


class TestResourceComments(BaseTestCase):
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
        self.tester.wait_for_stable_main_page(10)
        song_res_text = "两只老虎"
        self.tester.search_keyword(song_res_text)
        time.sleep(2)
        if self.tester.is_element_exist(
                "com.netease.cloudmusic:id/songNameAndInfoArea"):
            # 点击点点点
            self.tester.find_element_by_id_and_tap(
                "com.netease.cloudmusic:id/actionBtn")
            time.sleep(3)
            self.tester.find_element_by_uiautomator_and_tap(
                'new UiSelector().textStartsWith("评论")')
            self.tester.wait_element_for_a_while(
                "com.netease.cloudmusic:id/sectionName", 10)
        time.sleep(2)

    def test_comment_01_send_comment(self):
        # 检查可以正常发布评论、回复评论
        edit_res_id = "com.netease.cloudmusic:id/edit"
        mock_msg = "唯一会唱的歌"
        self.tester.send_one_msg(edit_res_id, mock_msg)
        self.tester.press_back()

    def test_comment_02_single_comment(self):
        # 检查评论页头部资源显示正确：--资源封面、名称、歌手/用户名
        # 检查点击头部资源跳转对应资源页
        # 检查评论点赞
        thumbs_up_id = "com.netease.cloudmusic:id/commentLikedContainer"
        self.tester.wait_element_for_a_while(thumbs_up_id, 10)
        error_msg = "未找到点赞按钮"
        self.assertTrue(self.tester.is_element_exist(thumbs_up_id), error_msg)
        ele_thumbs_up = self.tester.find_element_by_id(
            thumbs_up_id)
        like_count_before = ele_thumbs_up.text.strip()
        ele_thumbs_up.click()
        time.sleep(5)
        like_count_ater = ele_thumbs_up.text.strip()
        self.assertEqual(
            int(like_count_before) + 1,
            int(like_count_ater),
            "点赞后点赞数据应该+1")

        # 恢复环境,避免下次执行出错
        ele_thumbs_up.click()
        time.sleep(1)
    
    def test_comment_03_check_comment(self):
        # 滑动到最新评论
        lastest_comment_flag = "最新评论"
        ele_lastest_comment = self.tester.scroll_to_exact_element(
            lastest_comment_flag)

        # 最新评论位于页面最底端，评论块显示不全
        just_now_str = "分钟前"
        if not self.tester.is_element_exist(just_now_str):
            self.tester.swipe_down()

        error_msg = "没有找到" + lastest_comment_flag
        self.assertIsNotNone(ele_lastest_comment, error_msg)

        mock_msg = "唯一会唱的歌"
        self.assertTrue(
            self.tester.is_element_exist(mock_msg),
            "最新评论的内容应该为" + mock_msg)

        # 删除测试中间数据
        del_list = [mock_msg, "Inbox-AtMe-at我干嘛,想我了吗"]
        for cur_msg in del_list:
            if self.tester.is_element_exist(cur_msg):
                self.tester.find_element_by_uiautomator_and_tap(
                    'new UiSelector().text("{}")'.format(cur_msg))
                time.sleep(2)

                std_comments_list = ['回复评论', '举报评论', '删除评论', '查看详情']
                if self.tester.is_element_exist(std_comments_list[2]):
                    self.tester.find_element_by_uiautomator_and_tap(
                        'new UiSelector().text("{}")'.format(std_comments_list[2]))
                    time.sleep(2)
            else:
                self.tester.logger.info("Device: %s 当前页面不存在测试中间数据 %s" % (
                    self.tester.device.deviceName, cur_msg))

        self.tester.press_back(2)
        time.sleep(2)
