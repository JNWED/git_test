# -*- coding:utf-8 -*-
import sys
import time
from common.basetestcase import BaseTestCase
sys.path.append('../..')

feed = '//XCUIElementTypeCell[contains(@name,"云中酒哥")]'

class FriendTest(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.tester.logger.info("Device: %s Start case: %s" % (
            self.tester.device.deviceName, self._testMethodName))

        time.sleep(5)
        self.close_auto_play()
        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="朋友"]')
        time.sleep(5)

    def tearDown(self):
        self.tester.addfailscreenshot(self._testMethodName)
        self.tester.back_to_start()

    def close_auto_play(self):
        # 首先关闭自动播放
        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="帐号"]')
        time.sleep(2)
        self.tester.wait_element_xpath_display(self.tester.driver, '//XCUIElementTypeStaticText[@name="设置"]')
        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeStaticText[@name="设置"]')

        # 判断是否在动态页中wifi下自动播放视频，如果自动播放，关闭
        if self.tester.is_element_exist_ios('xpath', '//XCUIElementTypeStaticText[@name="动态页中WiFi下自动播放视频"]/../XCUIElementTypeButton[@name="打开"]'):
            self.tester.find_element_by_xpath_and_click('//XCUIElementTypeStaticText[@name="动态页中WiFi下自动播放视频"]/../XCUIElementTypeButton[@name="打开"]')

        # 判断是否在视频页wifi下连续播放，如果自动播放，关闭
        if self.tester.is_element_exist_ios('xpath', '//XCUIElementTypeStaticText[@name="视频页中WiFi下连续播放"]/../XCUIElementTypeButton[@name="打开"]'):
            self.tester.find_element_by_xpath_and_click('//XCUIElementTypeStaticText[@name="视频页中WiFi下连续播放"]/../XCUIElementTypeButton[@name="打开"]')

        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="返回"]')

    def delete_all_feed(self):
        # 删除发布的动态
        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="帐号"]')
        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[contains(@name,"动态")]')

        while self.tester.is_element_exist_ios('xpath', feed):

            if self.tester.is_element_exist_ios('xpath', feed+'[1]/XCUIElementTypeButton[3]'):
                self.tester.find_element_by_xpath_and_click(feed+'[1]/XCUIElementTypeButton[3]')
            else:
                self.tester.find_element_by_xpath_and_click(feed + '/XCUIElementTypeButton[3]')
            self.tester.find_element_by_xpath_and_click('//XCUIElementTypeStaticText[@name="删除"]')
            self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="删除"]')
            time.sleep(2)

        time.sleep(3)

    '''
    发布动态
    1. 在动态列表页，点击发表动态，进入动态编辑界面，检查页面正常
    2. 检查不带图（纯文字）的动态可以发送成功
    3. 动态详情页，点赞，评论，转发
    '''
    def test_friend_01_feed(self):

        self.skipTest('发表动态元素无法定位')

        i = 0
        while i < 5:
            if self.tester.is_element_exist_ios('xpath', '//XCUIElementTypeNavigationBar[@name="NMFriendsView"]'):
                ele = self.tester.driver.find_element_by_xpath('//XCUIElementTypeNavigationBar[@name="NMFriendsView"]')
                y = int(ele.location.get('y'))
                height = int(ele.size.get('height'))
                self.tester.driver.tap([(10, y+height+1)], 100)

                if self.tester.is_element_exist_ios('xpath', '//XCUIElementTypeNavigationBar[@name="分享"]'):
                    break
                else:
                    self.tester.driver.tap([(10, y+height+1)], 100)
                    i += 1

        self.tester.wait_element_xpath_display(self.tester.driver, '//XCUIElementTypeNavigationBar[@name="分享"]')

        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeStaticText[@name="一起聊聊吧~"]')
        self.tester.find_element_by_xpath_and_send_keys('//XCUIElementTypeStaticText[@name="一起聊聊吧~"]', '听歌ing')

        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="发送"]')
        time.sleep(3)
        self.tester.wait_element_xpath_display(self.tester.driver, '//XCUIElementTypeCell[contains(@name,"云中酒哥")]')
        self.assertIsNotNone(self.tester.driver.find_element_by_xpath('//XCUIElementTypeCell[contains(@name,"云中酒哥")]'),
                             "设备: %s 发表动态成功" % (self.tester.device.deviceName))

        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeCell[contains(@name,"云中酒哥")]')
        self.tester.wait_element_xpath_display(self.tester.driver, '//XCUIElementTypeButton[@name="cm4 edit share"]')
        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="cm4 edit share"]/../XCUIElementTypeButton[1]')
        time.sleep(2)
        self.assertIsNotNone(self.tester.driver.find_element_by_xpath('//XCUIElementTypeStaticText[@name="赞: "]'),
                             "设备: %s 点赞成功" % (self.tester.device.deviceName))

        edit_xpath = '//XCUIElementTypeWindow[1]/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther[4]/XCUIElementTypeTextView'

        self.tester.find_element_by_xpath_and_send_keys(edit_xpath, '和你一样\n')

        time.sleep(3)
        if self.tester.is_element_exist_ios('xpath', '//*[@name="取消"]'):
            self.tester.find_element_by_xpath_and_click('//*[@name="取消"]')

        self.assertIsNotNone(self.tester.driver.find_element_by_xpath('//XCUIElementTypeStaticText[@name="和你一样"]'),
                             "设备: %s 评论成功" % (self.tester.device.deviceName))

        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="cm4 edit share"]')

        self.assertIsNotNone(self.tester.driver.find_element_by_xpath('//XCUIElementTypeStaticText[@name="转发到云音乐："]'),
                             "设备: %s 吊起分享成功" % (self.tester.device.deviceName))

        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeStaticText[@name="转发到云音乐："]/../XCUIElementTypeScrollView/XCUIElementTypeButton')
        time.sleep(2)

        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="发送"]')
        time.sleep(2)

        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="返回"]')

        self.assertIsNotNone(self.tester.driver.find_element_by_xpath('(//XCUIElementTypeStaticText[@name="1"])[1]'),
                             "设备: %s 转发成功" % (self.tester.device.deviceName))

        self.delete_all_feed()


    '''
    1. 检查可以增加图片资源，选择1-9张照片
    2. 检查发布带图的动态可以发送成功
    '''

    def test_friend_02_send_photo(self):

        self.skipTest('发表动态元素无法定位')

        i = 0
        while i < 5:
            if self.tester.is_element_exist_ios('xpath', '//XCUIElementTypeNavigationBar[@name="NMFriendsView"]'):
                ele = self.tester.driver.find_element_by_xpath('//XCUIElementTypeNavigationBar[@name="NMFriendsView"]')
                y = int(ele.location.get('y'))
                height = int(ele.size.get('height'))
                self.tester.driver.tap([(10, y+height+1)], 100)

                if self.tester.is_element_exist_ios('xpath', '//XCUIElementTypeNavigationBar[@name="分享"]'):
                    break
                else:
                    self.tester.driver.tap([(10, y+height+1)], 100)
                    i += 1

        self.tester.wait_element_xpath_display(self.tester.driver, '//XCUIElementTypeNavigationBar[@name="分享"]')

        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="上传照片"]')

        # 判断是否需要获取照片权限
        if self.tester.is_element_exist_ios('xpath', '//*[@name="好"]'):
            self.tester.find_element_by_xpath_and_click('//*[@name="好"]')

        # 判断是否需要获取相机权限
        if self.tester.is_element_exist_ios('xpath', '//*[@name="好"]'):
            self.tester.find_element_by_xpath_and_click('//*[@name="好"]')

        self.tester.wait_element_xpath_display(self.tester.driver, '//XCUIElementTypeNavigationBar[@name="相机胶卷"]')
        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeImage[contains(@name,"照片")][1]')

        # 用于添加多余1张照片的步骤
        # self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="cm2 act choose"]')
        # self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="cm2 act view btn back"]')
        # self.tester.find_element_by_xpath_and_click('//XCUIElementTypeImage[contains(@name,"照片")][2]')
        # self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="cm2 act choose"]')

        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[contains(@name,"完成")]')

        self.assertIsNotNone(self.tester.driver.find_element_by_xpath('///XCUIElementTypeButton[@name="cm2 act btn del"]'),
                             "设备: %s 添加图片资源成功" % (self.tester.device.deviceName))

        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="发送"]')
        time.sleep(3)

        self.tester.wait_element_xpath_display(self.tester.driver, '//XCUIElementTypeStaticText[@name="云中酒哥"][1]')
        self.assertIsNotNone(self.tester.driver.find_element_by_xpath('//XCUIElementTypeStaticText[@name="云中酒哥"][1]'),
                             "设备: %s 发表动态成功" % (self.tester.device.deviceName))

        self.delete_all_feed()

    @classmethod
    def tearDownClass(cls):
        pass

