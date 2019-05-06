# -*- coding:utf-8 -*-
import sys
import time
from common.basetestcase import BaseTestCase
import random
sys.path.append('../..')

first_song = '//XCUIElementTypeStaticText[@name="目不转睛"]'
song_name = '//XCUIElementTypeStaticText[@name="Baby - Justin Bieber/Ludacris"]'
song_sheet_name = '//XCUIElementTypeStaticText[@name="Baby"]'


class SongSheetTest(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.tester.logger.info("Device: %s Start case: %s" % (
            self.tester.device.deviceName, self._testMethodName))
        time.sleep(5)
        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="我的"]')

        # 判断是否需要获取music权限
        if self.tester.is_element_exist_ios('xpath', '//*[@name="好"]'):
            self.tester.find_element_by_xpath_and_click('//*[@name="好"]')

        time.sleep(5)

    def tearDown(self):
        self.tester.addfailscreenshot(self._testMethodName)
        self.tester.back_to_start()

    '''
    资源内容详情页面-歌单-歌曲列表
    1. 点击列表中的某一单曲，则整个歌单都会被加入到播放列表
    '''
    def test_song_sheet_01_add_list(self):

        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeStaticText[@name="我喜欢的音乐"]')
        self.tester.wait_element_xpath_display(self.tester.driver, '//XCUIElementTypeOther[@name="我喜欢的音乐"]')

        self.tester.find_element_by_xpath_and_click(first_song)
        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="播放列表"]')

        time.sleep(3)
        self.assertIsNotNone(self.tester.driver.find_element_by_xpath(song_name),
                             "设备: %s 整个歌单都被加入列表中" % (self.tester.device.deviceName))

    '''
    2. 单曲项，点击...，检查更多操作菜单项可用，点击后进入对应的操作页面
        2.1 下一首播放
        2.2 收藏到歌单
        2.3 下载
        2.4 评论
    '''
    def test_song_sheet_02_single_song(self):

        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeStaticText[@name="我喜欢的音乐"]')
        self.tester.wait_element_xpath_display(self.tester.driver, '//XCUIElementTypeOther[@name="我喜欢的音乐"]')

        self.tester.find_element_by_xpath_and_click('(//XCUIElementTypeButton[@name="更多"])[2]')
        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeStaticText[@name="下一首播放"]')

        # 当前无歌曲播放，点击下一首播放会进入单曲播放页
        if self.tester.is_element_exist_ios('xpath', '//XCUIElementTypeButton[@name="暂停"]'):
            self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="返回"]')

        self.tester.logger.info("开始运行收藏到歌单的case")
        self.tester.find_element_by_xpath_and_click('(//XCUIElementTypeButton[@name="更多"])[2]')
        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeStaticText[@name="收藏到歌单"]')
        time.sleep(2)

        self.assertIsNotNone(self.tester.driver.find_element_by_xpath('//XCUIElementTypeStaticText[@name="新建歌单"]'),
                             "设备: %s 收藏到歌单的浮层弹起" % (self.tester.device.deviceName))
        # 需要将浮层点掉
        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeStaticText[@name="我喜欢的音乐"]')

        # 判断是否是第一次收藏，弹窗提示已收藏到歌单，需要点击掉
        if self.tester.is_element_exist_ios('xpath', '//*[@name="知道了"]'):
            self.tester.find_element_by_xpath_and_click('//*[@name="知道了"]')

        self.tester.logger.info("开始运行下载的case")
        self.tester.find_element_by_xpath_and_click('(//XCUIElementTypeButton[@name="更多"])[2]')
        # 判断是否已经下载过
        if self.tester.is_element_exist_ios('xpath', '//XCUIElementTypeStaticText[@name="删除下载文件"]'):
            self.assertFalse(self.tester.is_element_exist_ios('xpath', '//XCUIElementTypeStaticText[@name="下载"]'))

        else:
            self.tester.find_element_by_xpath_and_click('//XCUIElementTypeStaticText[@name="下载"]')

            # 判断是否是第一次下载，需要选择音质
            if self.tester.is_element_exist_ios('xpath', '//XCUIElementTypeStaticText[@name="标准 (128kbit/s)"]'):
                self.tester.find_element_by_xpath_and_click('//XCUIElementTypeStaticText[@name="标准 (128kbit/s)"]')

            self.tester.wait_element_xpath_display(self.tester.driver, '//XCUIElementTypeImage[@name="cm2_list_icn_dld_ok.png"]')
            self.assertIsNotNone(self.tester.driver.find_element_by_xpath('//XCUIElementTypeImage[@name="cm2_list_icn_dld_ok.png"]'),
                                 "设备: %s 下载成功" % (self.tester.device.deviceName))

            self.tester.find_element_by_xpath_and_click('(//XCUIElementTypeButton[@name="更多"])[2]')

        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeStaticText[contains(@name,"评论")]')
        time.sleep(3)
        self.assertIsNotNone(self.tester.driver.find_element_by_xpath('//XCUIElementTypeNavigationBar[contains(@name,"评论")]'),
                             "设备: %s 跳转到评论页面" % (self.tester.device.deviceName))

    '''
    3. 我创建的歌单
        3.1 点击歌单封面，点击编辑，则进入歌单编辑页面
        3.2 检查歌单封面可以更换成功
        3.3 检查歌单名可以更换成功
        3.4 检查标签可以更换成功，并且检查标签页，标签页显示正常
        3.5 检查介绍可以更换成功  --未完成
        3.6 修改完成后，回到歌单页，检查信息已更新  --未完成
    '''
    def test_song_sheet_03_my_create(self):

        self.tester.find_element_by_xpath_and_click(song_sheet_name)

        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeImage[@name="封面图片"]')

        # print self.tester.driver.page_source

        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="编 辑"]')
        self.assertIsNotNone(self.tester.driver.find_element_by_xpath('//XCUIElementTypeNavigationBar[@name="编辑歌单信息"]'),
                             "设备: %s 跳转到歌单编辑页面" % (self.tester.device.deviceName))

        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeStaticText[@name="更换封面"]')

        # 判断是否需要获取照片权限
        if self.tester.is_element_exist_ios('xpath', '//*[@name="好"]'):
            self.tester.find_element_by_xpath_and_click('//*[@name="好"]')

        # 判断是否需要获取相机权限
        if self.tester.is_element_exist_ios('xpath', '//*[@name="好"]'):
            self.tester.find_element_by_xpath_and_click('//*[@name="好"]')

        time.sleep(3)
        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeImage[contains(@name,"照片")][1]')
        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="选取"]')

        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeStaticText[@name="名称"]')
        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="清除文本"]')
        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeTextField[@value="歌单标题"]')
        song_sheet_title = random.choice(['apple', 'pear', 'peach', 'orange', 'lemon'])
        self.tester.find_element_by_xpath_and_send_keys('//XCUIElementTypeTextField[@value="歌单标题"]', song_sheet_title)
        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="完成"]')

        self.assertIsNotNone(self.tester.driver.find_element_by_xpath(
            '//XCUIElementTypeStaticText[@name="'+song_sheet_title+'"]'), "设备: %s 编辑名称成功" % (self.tester.device.deviceName))

        # 回置歌单标题
        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeStaticText[@name="名称"]')
        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="清除文本"]')
        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeTextField[@value="歌单标题"]')
        self.tester.find_element_by_xpath_and_send_keys('//XCUIElementTypeTextField[@value="歌单标题"]', 'Baby')
        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="完成"]')

        # 先判断是否已经有标签了
        if self.tester.is_element_exist_ios('xpath', '//XCUIElementTypeStaticText[@name="摇滚"]'):
            # 回置标签
            self.tester.find_element_by_xpath_and_click('//XCUIElementTypeStaticText[@name="标签"]')
            self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="摇滚"]')
            self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="完成"]')

        # 修改标签
        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeStaticText[@name="标签"]')
        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="摇滚"]')
        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="完成"]')

        self.assertIsNotNone(self.tester.driver.find_element_by_xpath('//XCUIElementTypeStaticText[@name="摇滚"]'),
                             "设备: %s 摇滚标签添加成功" % (self.tester.device.deviceName))
        # 回置标签
        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeStaticText[@name="标签"]')
        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="摇滚"]')
        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="完成"]')
        time.sleep(2)

        # 暂未找到ios清除文本框的方法，先搁置
        # self.tester.find_element_by_xpath_and_click('//XCUIElementTypeTextView')
        # self.tester.find_element_by_xpath_and_send_keys(
        #     '//XCUIElementTypeTextView', "like ")
        # self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="返回"]')

    '''
    4. 管理歌单
        4.1 新建歌单：输入歌单名后，新歌单新建成功
        4.2 隐私歌单可以创建成功

        4.3 进入歌单管理页面，检查可以删除歌单
        4.4 点击完成，可以退出编辑界面
    '''
    def test_song_sheet_04_manage_song_sheet(self):

        # 获取...坐标并点击
        x = int(self.tester.driver.find_element_by_xpath('(//XCUIElementTypeImage[@name="cm2_list_icn_arr.png"])[1]').location.get('x'))
        y = int(self.tester.driver.find_element_by_xpath('//XCUIElementTypeOther[contains(@name,"我创建的歌单")]').location.get('y'))

        self.tester.driver.tap([(x-10, y)], 100)
        time.sleep(2)

        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeStaticText[@name="新建歌单"]')

        self.tester.wait_element_xpath_display(self.tester.driver, '//XCUIElementTypeNavigationBar[@name="新建歌单"]')
        self.assertIsNotNone(self.tester.driver.find_element_by_xpath('//XCUIElementTypeNavigationBar[@name="新建歌单"]'),
                             "设备: %s 进入新建歌单页失败" %(self.tester.device.deviceName))

        song_sheet_title = random.choice(['exo', 'sj', 'ninepercent', 'tfboys'])
        self.tester.find_element_by_xpath_and_send_keys('//XCUIElementTypeTextField[@value="歌单标题"]', song_sheet_title)

        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeOther[@name="设置为隐私歌单"]')

        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="完成"]')
        time.sleep(2)

        self.assertIsNotNone(self.tester.driver.find_element_by_xpath('//XCUIElementTypeStaticText[@name="'+song_sheet_title+'"]'),
                             "设备: %s 新建歌单失败" % (self.tester.device.deviceName))

        self.assertIsNotNone(self.tester.driver.find_element_by_xpath('//XCUIElementTypeImage[@name="cm2_list_cover_icn_privacy.png"]'),
                             "设备: %s 隐私歌单创建失败" % (self.tester.device.deviceName))

        self.tester.driver.tap([(x-10, y)], 100)
        time.sleep(2)

        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeStaticText[@name="管理歌单"]')
        time.sleep(2)

        self.tester.wait_element_xpath_display(self.tester.driver, '//XCUIElementTypeButton[@name="删除“'+song_sheet_title+', 0首”"]')

        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="删除“'+song_sheet_title+', 0首”"]')

        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="删除“'+song_sheet_title+', 0首”"]/..//XCUIElementTypeButton[@name="删除"]')

        # print self.tester.driver.page_source

        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeStaticText[@name="确定删除歌单？"]/../../..//XCUIElementTypeButton[@name="删除"]')
        time.sleep(3)

        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="完成"]')
        time.sleep(2)

        self.assertFalse(self.tester.is_element_exist_ios('xpath', '//XCUIElementTypeStaticText[@name="'+song_sheet_title+'"]'),
                             "设备: %s 删除歌单失败" % (self.tester.device.deviceName))

        self.assertFalse(self.tester.is_element_exist_ios('xpath', '//XCUIElementTypeButton[contains(@name,"重新排序")]'),
                             "设备: %s 退出编辑模式失败" % (self.tester.device.deviceName))

    '''
    5. 删除：
        5.1 左划单曲，会显示删除，
        5.2 选择删除后，则该单曲会成功从歌单中删除
        5.3 删除已下载的单曲时，会给出是否同时删除下载文件的提示，选择删除，则下载文件会同时被删除
    '''
    def test_song_sheet_05_delete_song(self):

        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeStaticText[@name="我喜欢的音乐"]')
        self.tester.wait_element_xpath_display(self.tester.driver, '//XCUIElementTypeOther[@name="我喜欢的音乐"]')

        self.tester.logger.info("开始运行收藏到歌单的case")
        self.tester.find_element_by_xpath_and_click('(//XCUIElementTypeButton[@name="更多"])[2]')
        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeStaticText[@name="收藏到歌单"]')

        time.sleep(2)

        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeStaticText[@name="新建歌单"]')

        self.tester.wait_element_xpath_display(self.tester.driver, '//XCUIElementTypeNavigationBar[@name="新建歌单"]')
        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="清除文本"]')

        song_sheet_title = random.choice(['exo', 'sj', 'ninepercent', 'tfboys'])
        self.tester.find_element_by_xpath_and_send_keys('//XCUIElementTypeTextField[@value="歌单标题"]', song_sheet_title)

        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeOther[@name="设置为隐私歌单"]')

        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="完成"]')
        time.sleep(2)

        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="我的"]')

        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeStaticText[@name="'+song_sheet_title+'"]')
        time.sleep(2)

        self.tester.find_element_by_xpath_and_click('(//XCUIElementTypeButton[@name="更多"])[2]')

        # 判断是否已经下载过
        if self.tester.is_element_exist_ios('xpath', '//XCUIElementTypeStaticText[@name="删除下载文件"]'):
            self.assertFalse(self.tester.is_element_exist_ios('xpath', '//XCUIElementTypeStaticText[@name="下载"]'))

        else:
            self.tester.find_element_by_xpath_and_click('//XCUIElementTypeStaticText[@name="下载"]')

            # 判断是否是第一次下载，需要选择音质
            if self.tester.is_element_exist_ios('xpath', '//XCUIElementTypeStaticText[@name="标准 (128kbit/s)"]'):
                self.tester.find_element_by_xpath_and_click('//XCUIElementTypeStaticText[@name="标准 (128kbit/s)"]')

            self.tester.wait_element_xpath_display(self.tester.driver, '//XCUIElementTypeImage[@name="cm2_list_icn_dld_ok.png"]')
            self.assertIsNotNone(self.tester.driver.find_element_by_xpath('//XCUIElementTypeImage[@name="cm2_list_icn_dld_ok.png"]'),
                                 "设备: %s 下载成功" % (self.tester.device.deviceName))

        self.tester.find_element_by_xpath_and_click('(//XCUIElementTypeButton[@name="更多"])[2]')

        ele = self.tester.driver.find_element_by_xpath('//XCUIElementTypeStaticText[@name="收藏到歌单"]')

        self.tester.driver.swipe(ele.location.get('x'), ele.location.get('y')+200, 0, -200, duration=200)

        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeStaticText[@name="删除"]')

        time.sleep(2)

        self.tester.find_element_by_xpath_and_click(
            '(//XCUIElementTypeButton[@name="删除"])[2]')

        time.sleep(2)

        self.assertIsNotNone(
            self.tester.driver.find_element_by_xpath('//XCUIElementTypeStaticText[contains(@name,"收藏喜欢的音乐到歌单")]'),
            "设备: %s 删除歌曲成功" % (self.tester.device.deviceName))

        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="我的"]')

        # 获取...坐标并点击
        x = int(self.tester.driver.find_element_by_xpath('(//XCUIElementTypeImage[@name="cm2_list_icn_arr.png"])[1]').location.get('x'))
        y = int(self.tester.driver.find_element_by_xpath('//XCUIElementTypeOther[contains(@name,"我创建的歌单")]').location.get('y'))

        self.tester.driver.tap([(x-10, y)], 100)
        time.sleep(2)

        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeStaticText[@name="管理歌单"]')
        time.sleep(2)

        self.tester.wait_element_xpath_display(self.tester.driver, '//XCUIElementTypeButton[@name="删除“'+song_sheet_title+', 0首”"]')

        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="删除“'+song_sheet_title+', 0首”"]')

        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="删除“'+song_sheet_title+', 0首”"]/..//XCUIElementTypeButton[@name="删除"]')

        # print self.tester.driver.page_source

        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeAlert//XCUIElementTypeButton[@name="删除"]')
        time.sleep(3)

        self.tester.find_element_by_xpath_and_click('//XCUIElementTypeButton[@name="完成"]')
        time.sleep(2)

        self.assertFalse(self.tester.is_element_exist_ios('xpath', '//XCUIElementTypeStaticText[@name="'+song_sheet_title+'"]'),
                             "设备: %s 删除歌单失败" % (self.tester.device.deviceName))


    @classmethod
    def tearDownClass(cls):
        pass

