# -*- coding:utf-8 -*-
import os
import sys
import time
from datetime import datetime
import tempfile
import traceback
import hashlib
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

reload(sys)#这是python2中的写法
sys.setdefaultencoding('utf-8')


def PATH(p): return os.path.abspath(p)


TEMP_FILE = PATH(tempfile.gettempdir() + "/temp_screen.png")


class Tester(object):
    #根据appium与webdriver自定义功能函数
    def __init__(self, driver):#构造函数？
        self._driver = driver
        self._user = None
        self._device = None
        self._logger = None
        self.action = TouchAction(self._driver)#TouchAction，appium中的辅助类，模拟各种屏幕事件，参数为一个driver对象
        self._screenshot_path = ""
        self.device_width = self._driver.get_window_size()['width']
        self.device_height = self._driver.get_window_size()['height']#调用get_window_size（）获取屏幕长和宽

    @property
    def driver(self):
        return self._driver

    @driver.setter
    def driver(self, value):
        self._driver = value

    @property
    def screenshot_path(self):
        return self._screenshot_path

    @screenshot_path.setter
    def screenshot_path(self, value):
        self._screenshot_path = value

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        self._user = value

    @property
    def device(self):
        return self._device

    @device.setter
    def device(self, value):
        self._device = value

    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, value):
        self._logger = value

    def swipe_screen(self, startx, starty, endx, endy, duration=500):#模拟滑动屏幕
        self.logger.info(
            "Device:%s swipe from point x:%s y:%s to x:%s y:%s" %
            (self.device.deviceName, startx, starty, endx, endy))
        self.driver.swipe(startx, starty, endx, endy, duration=500)

    def tap_screen(self, x, y):#模拟点击屏幕操作
        self.logger.info("Device:%s tap screen point at x:%s y:%s"
                         % (self.device.deviceName, x, y))
        self.action.tap(None, x, y).perform()

    def long_press_screen(self, eleid, duration):#模拟通过id找到元素，长时间按压屏幕操作

        el = self.driver.find_element_by_id(eleid)
        time.sleep(1)
        self.logger.info("Device:%s long-pressed element %s %s ms"
                         % (self.device.deviceName, eleid, duration))
        self.action.long_press(el).wait(duration).release().perform()
        #relese()结束的行动取消屏幕上的指针
        #wait（）暂停操作，参数以毫秒为单位

    def find_ele_by_au_and_long_press(self, uiselector, duration=1):#模拟使用uiautomator定位元素，长时间按压屏幕操作
        """
        Find element by uiautomator and long press on the element once find
        :Args:
            - uiselector, eg. 'new UiSelector().description("demo")'
        :Usage:
            self.tester.find_ele_by_au_and_long_press(uiselector, duration)
        """

        el = self.driver.find_element_by_android_uiautomator(uiselector)
        time.sleep(1)
        self.logger.info("Device:%s long-pressed element %s %s ms"
                         % (self.device.deviceName, uiselector, duration))
        self.action.long_press(el).wait(duration).release().perform()

    def screenshot(self, casename):#自动截屏，存储，并为图片按时间命名
        """
        image name = caseName + timestamp + ".png"
        """
        now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')
        image_name = casename + str(now)
        path = "%s/%s.png" % (self.screenshot_path, image_name)
        self.driver.save_screenshot(path)
        self.logger.info("Device:%s screen shot at path:%s"
                         % (self.device.deviceName, path))

    def addfailscreenshot(self, casename):#如果用例执行失败，调用screenshot函数
        """
        After test case failed, it will capture the screen
        """
        if sys.exc_info()[0]:
            self.screenshot(casename)
            self.logger.error("Device:%s Case Name: %s Failed"
                              % (self.device.deviceName, casename))

    def find_element_by_id(self, eleid, timeout=20):
        self.logger.info("Device:%s start find :%s"
                         % (self.device.deviceName, eleid))
        try:
            element = self.wait_element_id_display(
                self.driver, eleid, eleid, timeout)
            return element
        except Exception:
            self.logger.info(
                "Device:%s detected abormal!" %
                self.device.deviceName)
            traceback.print_exc()
            return None

    def find_elements_by_id(self, eleid, timeout=20):
        self.logger.info("Device:%s start find :%s"
                         % (self.device.deviceName, eleid))
        try:
            element = self.wait_elements_id_display(
                self.driver, eleid, eleid, timeout)
            return element
        except Exception:
            self.logger.info(
                "Device:%s detected abormal!" %
                self.device.deviceName)
            traceback.print_exc()
            return None

    def find_element_by_id_and_tap(self, eleid, timeout=20, taptimes=1):
        self.logger.info(
            "Device:%s start tap :%s" %
            (self.device.deviceName, eleid))#向log中输出信息
        try:
            element = self.wait_element_id_display(
                self.driver, eleid, eleid, timeout)
            if element is not None:
                if taptimes == 1:
                    self.action.tap(element).perform()
                    self.logger.info(
                        "Device:%s tap success :%s " %
                        (self.device.deviceName, eleid))
                elif taptimes > 1:
                    for taptime in range(taptimes):
                        self.action.tap(element).perform()
                        self.logger.info(
                            "Device:%s tap %s times success :%s " %
                            (self.device.deviceName, taptime, eleid))
        except TimeoutException:
            self.logger.info(
                "Device:%s detected abormal!" %
                self.device.deviceName)
            traceback.print_exc()

    def find_element_by_uiautomator(self, uiselector, timeout=20):
        self.logger.info("Device:%s start find element uiselector:%s"
                         % (self.device.deviceName, uiselector))
        element = self.wait_element_uiautormator_display(
            self.driver, uiselector, uiselector, timeout)
        return element

    def find_element_by_uiautomator_and_tap(self, uiselector, timeout=20):
        self.logger.info("Device:%s start tap element uiselector:%s"
                         % (self.device.deviceName, uiselector))
        element = self.wait_element_uiautormator_display(
            self.driver, uiselector, uiselector, timeout)
        if element is not None:
            self.action.tap(element).perform()
            self.logger.info(
                "Device:%s tap success :%s " %
                (self.device.deviceName, uiselector))

    def find_element_by_xpath_and_click(self, xpath):
        self.logger.info(
            "Device:%s find by xpath:%s" %
            (self.device.deviceName, xpath))
        element = self.driver.find_element_by_xpath(xpath)
        if element is not None:
            element.click()
            self.logger.info(
                "Device:%s click success :%s " %
                (self.device.deviceName, xpath))
        else:
            self.logger.info(
                "Device:%s 没找到元素 :%s " %
                (self.device.deviceName, xpath))

    def find_element_by_id_and_send_keys(self, eleid, text, timeout=20):
        self.logger.info("Device:%s start send_key %s to element id:%s"
                         % (self.device.deviceName, text, eleid))
        element = self.wait_element_id_display(
            self.driver, eleid, eleid, timeout)
        if element is not None:
            element.send_keys(unicode(text))
            self.logger.info(
                "Device:%s send_key text:%s to element id:%s success " %
                (self.device.deviceName, text, eleid))

    def find_element_by_xpath_and_send_keys(self, xpath, text, timeout=20):
        self.logger.info("Device:%s start send_key %s to element id:%s"
                         % (self.device.deviceName, text, xpath))
        element = self.wait_element_xpath_display(
            self.driver,  xpath, timeout)
        if element is not None:
            element.send_keys(unicode(text))
            self.logger.info(
                "Device:%s send_key text:%s to element id:%s success " %
                (self.device.deviceName, text, xpath))

    def find_element_by_class_name_and_tap(self, class_name, timeout=20):
        self.logger.info("Device:%s start tap element class name:%s"
                         % (self.device.deviceName, class_name))
        element = self.wait_element_id_display(
            self.driver, class_name, class_name, timeout)
        if element is not None:
            self.action.tap(element).perform()
            self.logger.info("Device:%s tap element id:%s success"
                             % (self.device.deviceName, class_name))

    def wait_element_id_display(self, driver, idstr, msg, timeout=20):
        try:
            return WebDriverWait( driver, timeout).until(EC.presence_of_element_located((By.ID, idstr)), msg)
        # WebDriverWait 默认情况下会每500毫秒调用一次until中的方法直到结果成功返回
        #若超过timeout中总时长，将抛出TimeoutException
        #作用：缓冲代码执行速度与页面加载速度
        except TimeoutException:
            raise

    def wait_elements_id_display(self, driver, resource_id, msg, timeout=20):
        try:
            return WebDriverWait(
                driver, timeout).until(lambda dr: dr.find_elements_by_id(resource_id))
        #lambda：创建一个匿名方法
        except TimeoutException:
            raise

    def wait_element_xpath_display(self, driver, xpath,  timeout=20):
        try:
            return WebDriverWait(
                driver, timeout).until(lambda dr: dr.find_element_by_xpath(xpath))
        except TimeoutException:
            raise

    def wait_element_uiautormator_display(
            self, driver, uiselector, msg, timeout=20):
        try:
            return WebDriverWait(
                driver, timeout).until(
                lambda dr: dr.find_element_by_android_uiautomator(uiselector))
        except TimeoutException:
            raise

    def wait_element(self, eleid, timeout=20):
        self.logger.info(
            "Device:%s wait element: %s" %
            (self.device.deviceName, eleid))
        if self.wait_element_id_display(self.driver, eleid, eleid, timeout):
            self.logger.info("Device:%s element id have displayed:%s"
                             % (self.device.deviceName, eleid))
        else:
            self.logger.info("Device:%s Timeout: wait element %s"
                             % (self.device.deviceName, eleid))

    def press_keycode(self, keycode):#输入指定键（keycode代码：数字）
        self.logger.info("Device:%s [action]press key:(keycode='%s')"
                         % (self.device.deviceName, keycode))
        self.driver.press_keycode(keycode)

    def swipe_left(self, times=1):
        for count in range(times):
            self.logger.info(
                "Device:%s [action]swipe left " %
                self.device.deviceName)
            startx = self.device_width - 10
            starty = self.device_height / 2
            endx = 10
            endy = self.device_height / 2
            self.driver.swipe(startx, starty, endx, endy)
            time.sleep(2)

    def swipe_right(self, times=1):
        for count in range(times):
            self.logger.info(
                "Device:%s [action]swipe right " %
                self.device.deviceName)
            startx = 10
            starty = self.device_height / 2
            endx = self.device_width - 10
            endy = self.device_height / 2
            self.driver.swipe(startx, starty, endx, endy)
            time.sleep(2)

    def swipe_right_ios(self, times=1):
        for count in range(times):
            self.logger.info(
                "Device:%s [action]swipe right " %
                self.device.deviceName)
            startx = self.device_width * 0.43
            starty = self.device_height * 0.75
            endx = self.device_width * 0.54
            endy = 0
            self.driver.swipe(startx, starty, endx, endy)
            time.sleep(2)

    def swipe_down(self, times=1):
        """Perform a swipe down full screen width
        :Args:
            - None
        :Usage:
            self.tester.swipe_down()
        """
        self.logger.info(
            "Device:%s [action]swipe up " %
            self.device.deviceName)
        startx = self.device_width / 2
        starty = self.device_height / 3
        endx = self.device_width / 2
        endy = 10

        print startx, starty
        print endx, endy

        for i in range(times):
            self.driver.swipe(startx, starty, endx, endy)
            time.sleep(2)

    def swipe_ios(self, name):
        try:
            if name == "down":
                self.driver.execute_script("mobile: scroll", {"direction": "down"})
            elif name == "up":
                self.driver.execute_script("mobile: scroll", {"direction": "up"})
            elif name == "left":
                self.driver.execute_script("mobile: scroll", {"direction": "left"})
            elif name == "right":
                self.driver.execute_script("mobile: scroll", {"direction": "right"})
        except Exception as e:
            pass

    def swipe_up(self, times=1):
        """Perform a swipe up full screen width
        :Args:
            - None
        :Usage:
            self.tester.swipe_up()
        """
        self.logger.info(
            "Device:%s [action]swipe up " %
            self.device.deviceName)
        startx = self.device_width / 2
        starty = self.device_height * 3 / 5
        endx = self.device_width / 2
        endy = self.device_height * 4 / 5
        for i in range(times):
            self.driver.swipe(startx, starty, endx, endy)
            time.sleep(2)

    def swipe_down_bottom(self):
        """swipe down to bottom
        :Args:
            - None
        :Usage:
            self.tester.swipe_down()
        """
        self.logger.info(
            "Device:%s [action]swipe down to bottom " %
            self.device.deviceName)
        is_bottom = False
        try:
            while not is_bottom:
                start_page = self.driver.page_source#获取页面源码
                start_md5 = hashlib.md5(start_page.encode('utf-8')).hexdigest()
                # use md5 to compare the huge string/利用md5来比较大型字符串
                self.swipe_down()
                end_page = self.driver.page_source
                end_md5 = hashlib.md5(end_page.encode('utf-8')).hexdigest()
                if start_md5 == end_md5:
                    is_bottom = True
                    return is_bottom
        except Exception:
            self.logger.error("Device:%s [action]swipe down to bottom failed"
                              % self.device.deviceName)
            return is_bottom

    def swipe_to_page_top(self):
        """swipe up to page top
        :Args:
            - None
        :Usage:
            self.tester.swipe_up_page_top()
        """
        self.logger.info(
            "Device:%s [action]swipe up to page top" %
            self.device.deviceName)
        is_top = False
        try:
            while not is_top:
                start_page = self.driver.page_source
                start_md5 = hashlib.md5(start_page.encode('utf-8')).hexdigest()
                # use md5 to compare the huge string
                self.swipe_up()
                end_page = self.driver.page_source
                end_md5 = hashlib.md5(end_page.encode('utf-8')).hexdigest()
                if start_md5 == end_md5:
                    is_top = True
                    return is_top
        except Exception:
            self.logger.error("Device:%s [action]swipe down to page top failed"
                              % self.device.deviceName)
            return is_top

    def is_element_exist(self, element, timeout=3):#查找源码中是否有此元素，默认尝试3此
        count = 0
        while count < timeout:
            source = self.driver.page_source
            if element in source:
                self.logger.info("Device:%s find the element: %s"
                                 % (self.device.deviceName, element))
                return True
            else:
                count += 1
                time.sleep(1)
        self.logger.info("Device:%s can't find the required element: %s"
                         % (self.device.deviceName, element))
        return False

    def get_verify_code(self):
        """get the message to login
        :Usage:
            self.tester.get_verify_code()
        TBD
        """
        pass

    def back_to_start(self):#重启APP
        try:
            self.driver.close_app()
            self.logger.info("back_to_start:close app")
            self.driver.launch_app()
            self.logger.info("back_to_start:start app")
            time.sleep(2)
        except Exception:
            self.logger.info("back_to_start:close app fail,try again")
            self.driver.launch_app()
            time.sleep(2)
            self.driver.close_app()
            self.driver.launch_app()
            time.sleep(2)

    def send_one_msg(self, ele_res_id, mock_msg, action="发送"):#模拟发送，找到元素send_key，找到发送键click
        """
        Post one comment

        Args:
        ele_res_id: element resource id
        mock_msg: mock comment message string
        """
        if self.is_element_exist(ele_res_id):
            self.find_element_by_id_and_tap(ele_res_id)
            time.sleep(1)
            self.driver.find_element_by_id(ele_res_id).clear()
            time.sleep(2)
            self.find_element_by_id_and_send_keys(
                ele_res_id, mock_msg.decode('utf-8'))
            time.sleep(1)
            if self.is_element_exist(action):
                self.driver.find_element_by_android_uiautomator(
                    'new UiSelector().text("{}")'.format(action)).click()
                time.sleep(2)
            else:
                return False
        else:
            return False
        return True

    def press_back(self, times=1):#键back
        """
        Press back button on DUT

        times: Repeat pressing back button specified times
        """
        for count in range(times):
            # KEYCODE_BACK Constant Value: 4(0x00000004)
            self.driver.press_keycode(4)
            # self.driver.back()
            self.logger.info("Device: %s %s" %
                             (self.device.deviceName, "Press back button"))
            time.sleep(1)

    def press_home(self, times=1):#键home
        """
        Press home button on DUT

        times: Press HOME button
        """
        # KEYCODE_BACK Constant Value: 3(0x00000003)
        self.driver.press_keycode(3)
        time.sleep(1)

    def get_same_line_element(
            self, src_ele, dest_res_id_str, up_offset, down_offset):
        """
        Return element which at the same line of src_ele

        src_ele: source element
        dest_res_id_str: Resource id of Android element
        """
        dest_elements_list = self.driver.find_elements_by_id(dest_res_id_str)
        if not dest_elements_list:
            return None
        upper_left_location = src_ele.location
        src_ele_size = src_ele.size
        y_top_max = upper_left_location['y'] + up_offset
        y_bottom_max = upper_left_location['y'] + \
            src_ele_size['height'] + down_offset
        for i in range(len(dest_elements_list)):
            cur_ele = dest_elements_list[i]
            center_y = cur_ele.location['y'] + cur_ele.size['height'] / 2
            if (center_y < y_bottom_max and center_y > y_top_max):
                return cur_ele

    def search_keyword(self, str_search_keyword):
        time.sleep(5)

        ele_res_id = "com.netease.cloudmusic:id/search_src_text"
        if self.is_element_exist("搜索") and not self.is_element_exist(ele_res_id):
            self.find_element_by_uiautomator_and_tap('new UiSelector().description("搜索")')
            time.sleep(2)
        if self.is_element_exist(str_search_keyword):
            self.find_element_by_uiautomator_and_tap(
                'new UiSelector().text("{}")'.format(str_search_keyword))
            time.sleep(2)
        else:
            self.find_element_by_id_and_tap(ele_res_id)
            self.find_element_by_id_and_send_keys(
                ele_res_id, str_search_keyword.decode('utf-8'))
            time.sleep(2)
            x = int(self.device_width / 2)
            y = int(self.device_height * 3 / 20)
            self.driver.tap([(x, y)])
            info_text = "click cordinates" + str(x) + " " + str(y)
            self.logger.info(
                "Device: %s %s" %
                (self.device.deviceName, info_text))

        count = 0
        while not self.is_element_exist(
                "com.netease.cloudmusic:id/songNameAndInfoArea") and count < 6:
            time.sleep(5)
            count = count + 1

    def clean_local_files(self):
        self.logger.info(
            "Device: %s %s" %
            (self.device.deviceName, "Start Clean items under My Music"))
        try:
            if self.is_element_exist("我的音乐"):
                self.find_element_by_uiautomator_and_tap(
                    'new UiSelector().description("我的音乐")')
                time.sleep(2)
                self.wait_element_for_a_while("下载管理", 10)

            # 删除本地音乐
            self.find_element_by_uiautomator_and_tap(
                'new UiSelector().text("下载管理")')
            time.sleep(2)
            dl_mgmt_tabs = ['单曲', '电台节目', '视频']
            for cur_tab in dl_mgmt_tabs:
                self.find_element_by_uiautomator_and_tap(
                    'new UiSelector().text("{}")'.format(cur_tab))
                time.sleep(2)
                if not self.is_element_exist("暂时没有内容"):
                    self.find_element_by_uiautomator_and_tap(
                        'new UiSelector().text("多选")')
                    self.find_element_by_uiautomator_and_tap(
                        'new UiSelector().text("全选")')
                    time.sleep(3)

                    self.find_element_by_uiautomator_and_tap(
                        'new UiSelector().text("删除")')
                    time.sleep(3)
                del_btn_id = 'com.netease.cloudmusic:id/buttonDefaultPositive'
                if self.is_element_exist(del_btn_id):
                    self.find_element_by_id_and_tap(del_btn_id)
                    time.sleep(2)
                    # Swipe down workaround of appium not respond
                    self.swipe_up(2)
            self.press_back()
            time.sleep(2)

            self.find_element_by_uiautomator_and_tap(
                'new UiSelector().text("我喜欢的音乐")')

            # 兼容弱网环境
            music_cover_res_id = "com.netease.cloudmusic:id/musicCover"
            self.wait_element_for_a_while(music_cover_res_id, 30)

            song_res_id = "com.netease.cloudmusic:id/songName"
            self.wait_element_for_a_while(music_cover_res_id, 20)
            if self.is_element_exist(song_res_id):
                self.find_element_by_uiautomator_and_tap(
                    'new UiSelector().text("多选")')
                time.sleep(2)
                self.find_element_by_uiautomator_and_tap(
                    'new UiSelector().text("全选")')
                time.sleep(2)
                self.find_element_by_uiautomator_and_tap(
                    'new UiSelector().text("删除")')
                del_btn_id = 'com.netease.cloudmusic:id/buttonDefaultPositive'
                if self.is_element_exist(del_btn_id):
                    if self.is_element_exist("同时删除下载文件"):
                        self.find_element_by_uiautomator_and_tap(
                            'new UiSelector().text("同时删除下载文件")')
                    time.sleep(2)
                    self.find_element_by_id_and_tap(del_btn_id)
                    time.sleep(2)
                    # Swipe down workaround of appium not respond
                    self.swipe_up(2)
                    self.wait_element_for_a_while("该歌单暂无歌曲", 20)
                self.press_back()
                time.sleep(3)
            self.press_back()
            time.sleep(3)

            self.wait_element_for_a_while("最近播放", 30)
            self.find_element_by_uiautomator_and_tap(
                'new UiSelector().text("最近播放")')
            time.sleep(3)
            empty_str = "清空"
            recently_played_list = ["歌曲", "视频"]
            for cur_tab in recently_played_list:
                if self.is_element_exist(cur_tab):
                    self.find_element_by_uiautomator_and_tap(
                        'new UiSelector().textStartsWith("{}")'.format(cur_tab))
                    time.sleep(2)
                    is_exist = self.is_element_exist("暂无播放记录")
                    if is_exist:
                        self.logger.info(
                            "Device: %s %s" %
                            (self.device.deviceName, "无最近播放记录，无需进行清除操作"))
                    else:
                        self.find_element_by_uiautomator_and_tap(
                            'new UiSelector().text("{}")'.format(empty_str))
                        time.sleep(2)
                        confirm_res_id = "com.netease.cloudmusic:id/buttonDefaultPositive"
                        if self.is_element_exist(confirm_res_id):
                            self.find_element_by_id_and_tap(confirm_res_id)
                            time.sleep(1)
                            # Swipe down workaround of appium not respond
                            self.swipe_up(2)
            self.press_back()
            self.logger.info(
                "Device: %s %s" %
                (self.device.deviceName, "End Clean items under My Music"))
        except Exception:
            self.logger.error("Device:%s [action]meet exception when cleaning dirty test data"
                % self.device.deviceName)


    def wait_element_for_a_while(self, ele_locator, max_time_in_secs):
        """
        Wait element for a while (time specified by max_time_in_secs)

        Args:
        ele_locator: resource id, text or content description of element
        max_time_in_secs: max time in seconds of waiting
        """
        count = 0
        if ele_locator:
            while not self.is_element_exist(
                    ele_locator) and count < int(max_time_in_secs / 2):
                time.sleep(2)
                count = count + 1
        else:
            self.logger.info(
                "Device: %s %s" %
                (self.device.deviceName, "Can't deal with None type"))

    def wait_for_stable_main_page(self, max_time_in_secs):
        """
        Wait for stable main page, incase AD (time specified by max_time_in_secs)

        Args:
        max_time_in_secs: max time in seconds of waiting
        """
        count = 0
        while not self.is_element_exist(
                "抽屉菜单") and count < int(max_time_in_secs / 2):
            time.sleep(2)
            count = count + 1

    def scroll_to_exact_element(self, ele_text):#自动向下滚动页面，通过text找到目标元素（最多尝试20次）
        self.logger.info(
            "Device: %s %s" %
            (self.device.deviceName, "Start Scroll to target element"))
        time.sleep(2)
        count = 0
        while not self.is_element_exist(ele_text) and count < 20:
            time.sleep(4)
            self.swipe_down()
            count = count + 1

        if self.is_element_exist(ele_text):
            ele_target = self.find_element_by_uiautomator(
                'new UiSelector().textStartsWith("{}")'.format(ele_text))
            time.sleep(5)
            self.logger.info(
                "Device: %s %s" %
                (self.device.deviceName, "Text of target element is: " + ele_target.text))
            self.logger.info(
                "Device: %s %s" %
                (self.device.deviceName, "Scroll and Found target element"))
            return ele_target

    def scroll_to_exact_ele_res_id(self, ele_res_id):#自动向下滚动页面，通过res_id找到目标元素（最多尝试20次）
        self.logger.info(
            "Device: %s %s" %
            (self.device.deviceName, "Start Scroll to target element with specific resource id"))
        time.sleep(2)
        count = 0
        self.swipe_down()
        while not self.is_element_exist(ele_res_id) and count < 20:
            time.sleep(4)
            self.swipe_down()
            count = count + 1

        if self.is_element_exist(ele_res_id):

            ele_target = self.driver.find_element_by_id(ele_res_id)
            time.sleep(3)
            self.logger.info(
                "Device: %s %s" %
                (self.device.deviceName, "Scroll and Found target element with specific resource id"))
            return ele_target

    def grant_permission_xiaomi(self, per_list):
        self.driver.start_activity(
            "com.miui.securitycenter",
            "com.miui.permcenter.MainAcitivty")
        time.sleep(2)
        entry_text = "应用权限管理"
        self.find_element_by_uiautomator_and_tap(
            'new UiSelector().text("{}")'.format(entry_text))
        time.sleep(2)
        app_name_chinese = "网易云音乐"
        ele_target = self.scroll_to_exact_element(app_name_chinese)
        if ele_target:
            ele_target.click()
            time.sleep(2)
            for cur_perm in per_list:
                ele_specific_perm = self.scroll_to_exact_element(cur_perm)
                if ele_specific_perm:
                    ele_specific_perm.click()
                    time.sleep(1)
                    if (self.is_element_exist("允许")):
                        self.find_element_by_uiautomator_and_tap(
                            'new UiSelector().text("允许")')
                        time.sleep(2)
                else:
                    error_msg = "在小米手机中未找到指定权限" + cur_perm
                    self.logger.error(
                        "Device: %s %s" %
                        (self.device.deviceName, error_msg))
                # self.swipe_to_page_top()
                self.swipe_up(3)
                time.sleep(2)
            self.press_back(3)

    def grant_permission_huawei(self, per_list):
        """
        Grant permission in advance, support Android P and O
        """
        self.driver.start_activity(
            "com.huawei.systemmanager",
            "com.huawei.permissionmanager.ui.MainActivity")
        time.sleep(2)
        app_name_chinese = "网易云音乐"
        ele_target = self.scroll_to_exact_element(app_name_chinese)
        if ele_target:
            ele_target.click()
            time.sleep(2)
            for cur_perm in per_list:
                if self.is_element_exist(cur_perm):
                    perm_switch_res_id = "android:id/switch_widget"
                    src_ele = self.driver.find_element_by_android_uiautomator(
                        'new UiSelector().text("{}")'.format(cur_perm))
                    self.check_checkbox_beside_ele(src_ele, perm_switch_res_id)
                else:
                    self.find_element_by_uiautomator_and_tap(
                        'new UiSelector().text("设置单项权限")')
                    time.sleep(2)
                    if self.is_element_exist(cur_perm):
                        src_ele = self.driver.find_element_by_android_uiautomator(
                            'new UiSelector().text("{}")'.format(cur_perm))
                        perm_switch_res_id = "com.huawei.systemmanager:id/PermissionCfgSwitch"
                        self.check_checkbox_beside_ele(
                            src_ele, perm_switch_res_id)
                        self.press_back()
                    else:
                        error_msg = "在华为手机中未找到指定权限" + cur_perm
                        self.logger.info(
                            "Device: %s %s" %
                            (self.device.deviceName, error_msg))
            self.press_back(2)
            time.sleep(2)

    def check_checkbox_beside_ele(self, src_ele, cb_res_id):
        """
        Click checkbox in sameline with specified element
        Args:
            src_ele: specified appium element
            cb_res_id: resource id of target checkbox
        """
        ele_target_switch = self.get_same_line_element(
            src_ele, cb_res_id, 0, 0)
        if ele_target_switch:
            is_checked = ele_target_switch.get_attribute('checked')
            if is_checked != "true":
                ele_target_switch.click()
                time.sleep(2)

    def grant_contants_access_ahead(self, dut_brand):
        """
        在小米和华为机器上预先赋予访问通讯录权限
        """
        if dut_brand.lower() == "xiaomi":
            self.grant_permission_xiaomi(["读取联系人", "桌面快捷方式"])
        elif dut_brand.lower() == "huawei":
            self.grant_permission_huawei(["通讯录", "创建桌面快捷方式"])
        else:
            info_text = "目前预配置权限功能仅支持小米与华为"
            self.logger.info(
                "Device: %s %s" %
                (self.device.deviceName, info_text))
            return False

    def double_check_login(self):
        '''
        login in with email
        '''
        # app站内登录--邮箱登录
        self.find_element_by_id_and_tap(
            'com.netease.cloudmusic:id/mainDrawerIcon')
        time.sleep(1)
        if (self.is_element_exist("立即登录")):
            info_text = "Opps, Somehow you need to login again"
            self.logger.info(
                "Device: %s %s" %
                (self.device.deviceName, info_text))
            self.find_element_by_uiautomator_and_tap(
                'new UiSelector().text("立即登录")')
            time.sleep(2)
            self.find_element_by_id_and_tap(
                'com.netease.cloudmusic:id/mail')
            self.find_element_by_id_and_send_keys(
                'com.netease.cloudmusic:id/email', self.user.email)
            self.find_element_by_id_and_send_keys(
                'com.netease.cloudmusic:id/password', self.user.epassword)
            self.find_element_by_id_and_tap(
                'com.netease.cloudmusic:id/login')
            time.sleep(2)

            # Check login status
            self.find_element_by_id_and_tap(
                'com.netease.cloudmusic:id/mainDrawerIcon')
            time.sleep(1)
            if not self.is_element_exist(
                    'com.netease.cloudmusic:id/drawerUserName'):
                error_msg = "Double login failed, God bless :-("
                self.logger.error(
                    "Device: %s %s" %
                    (self.device.deviceName, error_msg))
        # Back to mainpage
        self.press_back()
    def is_element_exist_ios(self, identifyBy, c):
        time.sleep(1)
        flag = False
        try:
            if identifyBy == "id":
                self.driver.find_element_by_id(c)
                flag = True
            elif identifyBy == "xpath":
                self.driver.find_element_by_xpath(c)
                flag = True
            elif identifyBy == "class":
                self.driver.find_element_by_class_name(c)
                flag = True
            elif identifyBy == "name":
                self.driver.find_element_by_name(c)
                flag = True
            elif identifyBy == "tag name":
                self.driver.find_element_by_tag_name(c)
                flag = True
            else:
                pass
            return flag
        except Exception as e:
            return flag
