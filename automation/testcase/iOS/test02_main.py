# -*- coding:utf-8 -*-
import sys
import time
from common.basetestcase import BaseTestCase
sys.path.append('../..')


class MainPageTest(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.tester.logger.info("Device: %s Start case: %s" % (
            self.tester.device.deviceName, self._testMethodName))
        time.sleep(4)

    def tearDown(self):
        self.tester.addfailscreenshot(self._testMethodName)
        self.tester.back_to_start()
    '''
    个性推荐/主播电台
    '''
    def test_MainPageTest_01_changeTag(self):
        try:
            self.tester.logger.info("个性推荐界面")
            self.tester.logger.info("点击切换到主播电台页面")
            self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="主播电台 未选定"]')
            time.sleep(1)
        except Exception:
            self.fail("设备: %s 切换标签出错" %(self.tester.device.deviceName))

    '''
    主页面内容加载正常
    '''
    def test_MainPageTest_02_recommendra(self):
        try:
            self.tester.logger.info("滑动个性推荐界面")
            self.tester.swipe_ios("down")
            self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="主播电台 未选定"]')
            self.tester.swipe_ios("down")
        except Exception:
            self.fail("设备: %s  加载内容出错" %(self.tester.device.deviceName))

    '''
    个性推荐龙珠测试
    '''
    def test_MainPageTest_recommendButton(self):
            # element_list = self.tester.find_element_by_xpath('/XCUIElementTypeScrollView/XCUIElementTypeTable/'
            #                                                  'XCUIElementTypeOther[3]/XCUIElementTypeButton')
            # for element in element_list:
            #     element.click()
            #     time.sleep(2)
            #     self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="返回"]')
            #     time.sleep(2)
            self.tester.logger.info("进入私人FM")
            self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="私人FM"]')
            time.sleep(2)
            if self.tester.is_element_exist_ios('xpath', '//XCUIElementTypeButton[@name="关闭"]'):
                self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="关闭"]')
                time.sleep(2)
            self.assertTrue('//XCUIElementTypeButton[@name="私人FM"]', "设备: %s 载入[私人FM]界面失败" %(self.tester.device.deviceName))
            self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="返回"]')
            self.tester.wait_element_xpath_display(self.tester.driver, '//XCUIElementTypeButton[@name="主播电台 未选定"]',
                                                   timeout=2)
            self.tester.logger.info("进入每日推荐")
            self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="每日推荐"]')
            self.tester.wait_element_xpath_display(self.tester.driver, '//XCUIElementTypeStaticText[@name="每日推荐"]',
                                                   timeout=2)
            self.assertTrue('//XCUIElementTypeStaticText[@name="每日推荐"]', "设备: %s 载入[每日推荐]界面失败" %(self.tester.device.deviceName))
            self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="返回"]')
            time.sleep(2)
            self.tester.logger.info("进入歌单")
            self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="歌单"]')
            self.tester.wait_element_xpath_display(self.tester.driver, '//XCUIElementTypeStaticText[@name="歌单"]',
                                                   timeout=2)
            self.assertTrue('//XCUIElementTypeStaticText[@name="歌单"]', "设备: %s 载入[歌单]界面失败 " %(self.tester.device.deviceName))
            self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="返回"]')
            time.sleep(2)

            self.tester.logger.info("进入排行榜")
            self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="排行榜"]')
            self.tester.wait_element_xpath_display(self.tester.driver, '//XCUIElementTypeStaticText[@name="排行榜"]',
                                                   timeout=2)
            self.assertTrue('//XCUIElementTypeStaticText[@name="排行榜"]', "设备: %s 载入[排行榜]界面失败" %(self.tester.device.deviceName))
            self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="返回"]')
            time.sleep(2)
    '''
    主播电台龙珠测试
    '''

    def test_MainPageTest_04_FmButton(self):
        try:
            self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="主播电台 未选定"]')
            time.sleep(1)
            self.tester.logger.info("进入电台分类")
            self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="电台分类"]')
            self.tester.logger.info("等待电台分类页面加载------")
            self.assertTrue('//XCUIElementTypeButton[@name="私人FM"]', "设备: %s 载入[电台分类]界面失败" %(self.tester.device.deviceName))
            self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="返回"]')
            time.sleep(1)
            #To be fix
            # self.tester.logger.info("进入电台排行")
            # self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="电台排行"]')
            # self.tester.logger.info("等待电台排行页面加载------")
            # self.tester.wait_element_xpath_display(self.tester.driver, '//XCUIElementTypeStaticText[@name="主播电台排行榜"]',
            #                                        timeout=2)
            # self.assertTrue('//XCUIElementTypeStaticText[@name="主播电台排行榜"]', "设备: %s 载入[电台排行]界面失败" %(self.tester.device.deviceName))
            # time.sleep(2)
            # #TODO 返回失败
            # self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="返回"]')
            # time.sleep(1)

            self.tester.logger.info("进入付费精品")
            self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="付费精品"]')
            self.tester.logger.info("等待付费精品加载------")
            self.tester.wait_element_xpath_display(self.tester.driver, '//XCUIElementTypeStaticText[@name="付费精品"]',
                                                   timeout=2)
            self.assertTrue('//XCUIElementTypeStaticText[@name="付费精品"]', "设备: %s 载入[付费精品]界面失败" %(self.tester.device.deviceName))
            self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="返回"]')
            time.sleep(1)

            self.tester.logger.info("进入小冰电台")
            self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="小冰电台"]')
            self.tester.logger.info("等待小冰电台页面加载------")
            time.sleep(2)
            if self.tester.is_element_exist("同意"):
                self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="同意"]')
            else:
                pass
            self.assertTrue('//XCUIElementTypeStaticText[@name="小冰电台"]', "设备: %s 载入[小冰电台]界面失败" %(self.tester.device.deviceName))
            self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="返回"]')
            time.sleep(1)
        except Exception:
            self.fail("设备: %s 主播电台龙珠测试有误" %(self.tester.device.deviceName))

    '''
    底部Tab测试
    '''
    def test_MainPageTest_05_bottomTag(self):
        try:
            self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="视频"]')
            time.sleep(1)
            self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="我的"]')
            time.sleep(1)
            # if self.tester.is_element_exist_ios('xpath', '//XCUIElementTypeButton[@name="好"]'):
            #     self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="好"]')
            #     time.sleep(1)
            # self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="朋友"]')
            # time.sleep(5)
            if self.tester.is_element_exist("好", timeout=2):
                self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="好"]')
                time.sleep(1)
            #TODO  视频播放的时候无法点击"账号"
            self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="帐号"]')
            time.sleep(1)
        except Exception:
            self.fail("设备: %s 底部tab切换异常" %(self.tester.device.deviceName))

    @classmethod
    def tearDownClass(cls):
        pass

