# -*- coding:utf-8 -*-

import sys
import time
import datetime
from common.basetestcase import BaseTestCase

sys.path.append('../..')


class TestInbox(BaseTestCase):
    """
    我的消息页面测试类
    """
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.tester.logger.info("Device: %s Start case: %s" % (
            self.tester.device.deviceName, self._testMethodName))

    def tearDown(self):
        '''
        tearDown
        '''
        self.tester.addfailscreenshot(self._testMethodName)
        self.tester.back_to_start()
        pass

    def common_ops(self, index):
        """
        进入我的消息页面公共操作
        """
        self.tester.wait_for_stable_main_page(15)

        error_msg = "Opps, Maybe you don't login"
        self.assertTrue(self.tester.is_element_exist("抽屉菜单"), error_msg)
        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().description("抽屉菜单")')
        time.sleep(3)
        my_msg_keyword = "我的消息"
        self.tester.wait_element_for_a_while(my_msg_keyword, 10)
        self.assertTrue(
            self.tester.is_element_exist(my_msg_keyword),
            "侧边栏我的消息必须存在")

        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().text("{}")'.format(my_msg_keyword))

        # 检查@我tab列表显示正确
        content_list = ["私信", "评论", "@我", "通知"]
        self.tester.wait_element_for_a_while(content_list[1], 20)
        error_msg = "没有" + content_list[index] + "玩不下去了"
        self.assertTrue(
            self.tester.is_element_exist(
                content_list[index]),
            error_msg)

        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().text("{}")'.format(content_list[index]))
        time.sleep(2)
        self.check_server_side_env()

    def test_inbox_01_entry(self):
        """
        Run test under "私信"　Tab
        """
        self.common_ops(0)

        # 检查我的消息页面下私信，评论，＠我，通知显示正确
        content_list = ["私信", "评论", "@我", "通知"]
        for cur_tab in content_list:
            error_msg = "诶，没找到" + cur_tab
            self.assertTrue(self.tester.is_element_exist(cur_tab), error_msg)

        # 检查滑动和点击可以切换四个tab
        self.tester.swipe_left(3)
        self.tester.swipe_right(3)
        error_msg = "诶，来回滑动后没回到" + content_list[0]
        self.assertTrue(
            self.tester.is_element_exist(
                content_list[0]), error_msg)
        time.sleep(2)

        # 检查私信页面点击进入聊天室
        self.assertTrue(
            self.tester.is_element_exist("云音乐多多和西西"),
            "云音乐多多和西西不存在于当前页面")
        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().text("{}")'.format("云音乐多多和西西"))
        time.sleep(2)
        self.tester.wait_element_for_a_while("写私信", 10)

        placeholder_flag = ["云音乐多多", "云音乐西西"]
        self.assertTrue(
            self.tester.is_element_exist(placeholder_flag[0]) or
            self.tester.is_element_exist(placeholder_flag[1]), "诶，为什么多多西西没有和你聊天呢")
        time.sleep(3)

        mock_msg = "到此一游"
        input_res_id = 'com.netease.cloudmusic:id/edit'
        self.tester.send_one_msg(input_res_id, mock_msg)
        time.sleep(2)
        self.tester.wait_element_for_a_while(mock_msg, 10)

        # 删除测试中间数据,避免污染DUT执行环境
        info_text = "开始-长按-删除刚mock的私信数据"
        self.tester.logger.info(
            "Device: %s %s" %
            (self.tester.device.deviceName, info_text))
        uiselector_target = 'new UiSelector().text("{}")'.format(mock_msg)
        self.tester.find_ele_by_au_and_long_press(uiselector_target)
        time.sleep(2)
        delete_text = "删除"
        if self.tester.is_element_exist(delete_text):
            self.tester.find_element_by_uiautomator_and_tap(
                'new UiSelector().text("{}")'.format(delete_text))
            time.sleep(1)

        self.tester.press_back(2)

    def test_inbox_02_comments(self):
        """
        Run test under "评论"　Tab
        """
        self.common_ops(1)

        # 检查评论tab列表显示正确--点击用户头像进入用户个人主页
        self.cmp_nickname("com.netease.cloudmusic:id/userCommentNickname",
                          "com.netease.cloudmusic:id/userCommentAvatar")

        # 检查点击评论提示回复、举报、删除、查看详情
        first_comment_id = "com.netease.cloudmusic:id/userCommentContent"
        self.tester.find_element_by_id_and_tap(first_comment_id)
        time.sleep(1)
        el_menu_list = self.tester.find_elements_by_id(
            "com.netease.cloudmusic:id/menuTitle")
        self.assertEqual(len(el_menu_list), 3)

        # 检查点击回复评论可以正常回复
        std_comments_list = ['回复评论', '举报评论', '删除评论', '查看详情']
        self.assertTrue(self.tester.is_element_exist(
            std_comments_list[0]))

        self.tester.find_element_by_uiautomator_and_tap(
            'new UiSelector().text("{}")'.format(std_comments_list[0]))
        time.sleep(2)
        mock_msg = "分享你的故事"
        id_edit_content = "com.netease.cloudmusic:id/editCommentContent"
        self.tester.send_one_msg(id_edit_content, mock_msg)

        # 检查点击查看详情进入评论详情页
        ele_before_view_more = self.tester.find_element_by_id(first_comment_id)
        ele_before_view_more_text = ele_before_view_more.text.strip()
        if ":" in ele_before_view_more_text:
            ele_before_view_more_text = ele_before_view_more_text.split(
                ':', 1)[-1].strip()
        self.tester.find_element_by_id_and_tap(first_comment_id)
        time.sleep(2)

        error_msg = "寻人通知：" + std_comments_list[3] + "你去哪里了"
        self.assertTrue(
            self.tester.is_element_exist(
                std_comments_list[3]),
            error_msg)
        uiselector_smst = 'new UiSelector().text("{}")'.format(
            std_comments_list[3])
        self.tester.find_element_by_uiautomator_and_tap(uiselector_smst)
        time.sleep(8)
        ele_after_view_more = self.tester.find_element_by_id(
            "com.netease.cloudmusic:id/commentContent")
        self.assertEqual(ele_before_view_more_text,
                         ele_after_view_more.text.strip(), "点击前后的评论内容应该一样一样滴")
        self.tester.press_back(2)

    def test_inbox_03_at_me(self):
        """
        Run test under "@我"　Tab
        """
        self.common_ops(2)

        # 点击用户头像进入用户个人主页
        self.cmp_nickname("com.netease.cloudmusic:id/trackUserName",
                          "com.netease.cloudmusic:id/trackCreatorAvatar")

        # @我消息点击跳转资源页
        res_id = "com.netease.cloudmusic:id/trackResContainer"
        error_msg = "找不到资源页诶,没法玩了"
        self.assertTrue(self.tester.is_element_exist(res_id), error_msg)

        # 点击资源
        # self.tester.find_element_by_id_and_tap(res_id)
        self.tester.find_element_by_id_and_tap(
            "com.netease.cloudmusic:id/trackResName")
        time.sleep(3)
        like_content_desc = "红心"
        if not self.tester.is_element_exist(like_content_desc):
            self.tester.find_element_by_id_and_tap(
                "com.netease.cloudmusic:id/musicName")
        self.tester.wait_element_for_a_while(like_content_desc, 10)
        error_msg = "你没有跳转，遇到什么困难了"
        self.assertTrue(
            "self.tester.is_element_exist(like_content_desc)",
            error_msg)

        self.tester.press_back()
        time.sleep(2)

        self.tester.wait_element_for_a_while(
            "com.netease.cloudmusic:id/trackDesc", 20)
        self.tester.find_element_by_id_and_tap(
            "com.netease.cloudmusic:id/trackDesc")
        time.sleep(3)
        if self.tester.is_element_exist("回复评论"):
            self.tester.find_element_by_uiautomator_and_tap(
                'new UiSelector().text("回复评论")')
            time.sleep(3)
        edit_res_id = "com.netease.cloudmusic:id/editCommentContent"
        mock_msg = "Inbox-AtMe-at我干嘛,想我了吗"
        self.tester.send_one_msg(edit_res_id, mock_msg)
        time.sleep(1)
        self.tester.press_back()

    def test_inbox_04_notification(self):
        """
        Run test under "通知"　Tab
        """
        self.common_ops(3)
        self.cmp_nickname("com.netease.cloudmusic:id/noticeNickName",
                          "com.netease.cloudmusic:id/userFaceImage")
        self.tester.press_back(1)

    def cmp_nickname(self, nickname_res_id, avatar_res_id):
        """
        点击用户头像进入用户个人主页，判断点击前后昵称是否一致
        """
        ele_first_track_name = self.tester.find_element_by_id(
            nickname_res_id)
        ele_first_track_name_text = ele_first_track_name.text
        count = 0
        self.tester.find_element_by_id_and_tap(avatar_res_id)
        time.sleep(2)

        # 兼容弱网环境
        after_nickname_id = "com.netease.cloudmusic:id/nickname"
        while not self.tester.is_element_exist(
                after_nickname_id) and count < 30:
            count = count + 1
            time.sleep(2)
        ele_personal_nickname = self.tester.find_element_by_id(
            after_nickname_id)
        self.assertEqual(ele_first_track_name_text,
                         ele_personal_nickname.text, "点击前后的昵称应该一样一样滴")
        self.tester.press_back()
        time.sleep(3)

    def check_server_side_env(self):
        """
        Check if server side env is stable
        """
        server_error_waring = "加载失败，请点击重试"
        uiselector_error = 'new UiSelector().text("{}")'.format(server_error_waring)
        count = 0
        while count < 5:
            if self.tester.is_element_exist(server_error_waring) is None:
                break
            else:
                self.tester.swipe_up()
                time.sleep(2)
                count = count + 1
        if self.tester.is_element_exist(server_error_waring):
            self.tester.screenshot(
                str(datetime.datetime.now()) + server_error_waring)
        try:
            ele_server_error = self.tester.driver.find_element_by_android_uiautomator(
                uiselector_error)
            error_msg = "服务器发生错误，请检查测试环境是否稳定"
            self.assertIsNone(ele_server_error, error_msg)
        except Exception:
            info_text = "当前server环境稳定"
            self.tester.logger.info(
                "Device: %s %s" %
                (self.tester.device.deviceName, info_text))
