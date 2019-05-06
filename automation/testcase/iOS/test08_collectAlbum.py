# -*- coding:utf-8 -*-
import sys
import time
from common.basetestcase import BaseTestCase
sys.path.append('../..')


class CollectAlbum(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.tester.logger.info("Device: %s Start case: %s" % (
            self.tester.device.deviceName, self._testMethodName))
        time.sleep(4)
    '''
    收藏专辑并检查是否收藏成功
    '''
    def test_CollectAlbum_01_searchTag(self):
            self.skipTest('收藏按钮暂时无法定位')
            time.sleep(4)
            self.tester.find_element_by_xpath_and_click('//XCUIElementTypeStaticText[1]')
            self.tester.find_element_by_xpath_and_send_keys('//XCUIElementTypeStaticText[1]', "baby", timeout=20)
            self.tester.find_element_by_xpath_and_click('// XCUIElementTypeButton[@name="Search"]')
            time.sleep(2)
            '''点击进入"专辑"界面'''
            self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="专辑 未选定"]')
            time.sleep(2)
            self.tester.find_element_by_xpath_and_click('/XCUIElementTypeTable/XCUIElementTypeCell[last]')
            time.sleep(2)
            self.tester.find_element_by_id_and_tap('多DailyTest选')
            time.sleep(1)
            self.tester.find_element_by_name_and_tap('cm4 list checkbox')
            self.tester.find_element_by_xpath_and_click('//XCUIElementTypeApplication[@name="云音乐测试"]/XCUIElementTypeWindow[1]'
                                                        '/XCUIElementTypeOther[2]/XCUIElementTypeOther[3]/XCUIElementTypeButton[2]')

            self.tester.find_element_by_name_and_tap('新建歌单')
            self.tester.find_element_by_name_and_tap('完成')
            time.sleep(4)


    def tearDown(self):
        self.tester.addfailscreenshot(self._testMethodName)
        self.tester.back_to_start()

    @classmethod
    def tearDownClass(cls):
            pass