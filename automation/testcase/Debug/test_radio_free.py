# -*- coding:utf-8 -*-

import sys
import time
from common.basetestcase import BaseTestCase

sys.path.append('../..')

class Radiotest1(BaseTestCase):
    """
    电台
    """
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.tester.logger.info("Device: %s Start case: %s" % (
            self.tester.device.deviceName, self._testMethodName))
        time.sleep(5)

    def setup_env(self, index):
        # 电台分类  
        ele_radio = self.tester.driver.find_element_by_android_uiautomator(
            'new UiSelector().text("电台")')
        if ele_radio:
            ele_radio.click()
            time.sleep(2)
        else:
            self.fail("没有找到电台按钮")
        #检查四个龙珠
        content_list = ["电台排行", "电台分类", "节目", "小冰电台"]
        if not self.tester.is_element_exist(content_list[index]):
            self.fail("没有" + content_list[index] + "玩不下去了")
            time.sleep(3)

    def test_radio_01(self):
        self.skipTest("skip test_radio due to stability issue")
        print "test case 1*****"
        self.setup_env(0)
        radio_id = "com.netease.cloudmusic:id/entry1"
        self.tester.wait_element_for_a_while(radio_id, 10)
        find_element_rank = self.tester.find_element_by_id(radio_id)
        self.assertIsNotNone(find_element_rank,'找不到电台排行按钮,Fail')
        find_element_rank.click()

        content_list = ["最热节目", "最热电台", "主播赞赏榜"]
        for cur_tab in content_list:
            if not self.tester.is_element_exist(cur_tab):
                self.fail("没找到"+cur_tab)
                time.sleep(4)
        #检查按钮之间的切换
        self.tester.swipe_left(2)
        time.sleep(2)
        self.tester.swipe_right(2)
        if not self.tester.is_element_exist(content_list[1]):
            self.fail("诶，来回滑动后没回到" + content_list[0])

    def test_radio_02(self):
        self.skipTest("skip test_radio due to stability issue")
        print "test case 2*****"
        self.setup_env(1)
        radio_rank_id = "com.netease.cloudmusic:id/entry2"
        self.tester.wait_element_for_a_while(radio_rank_id, 10)
        find_element_rank = self.tester.find_element_by_id(radio_rank_id)
        self.assertIsNotNone(find_element_rank,'电台分类,Fail')
        find_element_rank.click()
        self.tester.swipe_down_bottom()

    def test_radio_03(self):
        self.skipTest("skip test_radio due to stability issue")
        print "test case 3*****"
        self.setup_env(2)
        radio_show_id = "com.netease.cloudmusic:id/entry3"
        self.tester.wait_element_for_a_while(radio_show_id, 10)
        find_element_show = self.tester.find_element_by_id(radio_show_id)
        self.assertIsNotNone(find_element_show,'节目,Fail')
        time.sleep(3)
        find_element_show.click()
        time.sleep(1)

        radio_open_id = 'com.netease.cloudmusic:id/playBtn'
        self.tester.wait_element_for_a_while(radio_open_id, 10)
        find_element_open = self.tester.find_element_by_id(radio_open_id)
        self.assertIsNotNone(find_element_open,'播放,Fail')

    def test_radio_04(self):
        self.skipTest("skip test_radio due to stability issue")
        print "test case 4*****"   
        self.setup_env(3) 
        radio_ice_id = "com.netease.cloudmusic:id/entry4"
        self.tester.wait_element_for_a_while(radio_ice_id, 10)
        find_element_ice = self.tester.find_element_by_id(radio_ice_id)
        self.assertIsNotNone(find_element_ice,'小冰电台,Fail')
        find_element_ice.click()

    def test_radio_05(self):
        print "test case 5*****"
        '''
        swipe down
        '''
        self.skipTest("skip test_radio due to stability issue")
        ele_radio_skip = self.tester.driver.find_element_by_android_uiautomator(
            'new UiSelector().text("电台")')
        if ele_radio_skip:
            ele_radio_skip.click()
            time.sleep(2) 
            self.tester.swipe_down_bottom()
        else:
            self.fail("不能滑动")

    def tearDown(self):
        '''
        tearDown
        '''
        self.tester.addfailscreenshot(self._testMethodName)
        self.tester.back_to_start()
        
    @classmethod
    def tearDownClass(cls):
        pass
