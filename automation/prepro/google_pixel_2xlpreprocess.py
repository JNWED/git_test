# -*- coding:utf-8 -*-

from basedevicepreprocess import BaseDevicePreProcess
from common.tester import Tester
from common.log import Log


class Pixel2XLPreProcess (BaseDevicePreProcess):

    def __init__(self, tester):
        super(Pixel2XLPreProcess, self).__init__(tester)

    def install_app(self):
        #cmd = "adb -s %s install -r %s" % (self.tester.device.deviceid, DataProvider.niceapk)
        #subprocess.call(cmd, shell=True)
        pass

    def pre_process(self):
        Log.logger.info(
            "Device: %s start prepare process..." %
            self.tester.device.deviceName)
        driver = self.tester.driver
        #print "Huawei preprocess done!\n"
        """
        try:
            if driver.is_app_installed('com.nice.main'):
                Log.logger.info(u"设备：%s 卸载老的nice包" % self.tester.device.devicename)
                driver.remove_app('com.nice.main')

            if self.tester.is_element_exist('android:id/button1',30):
                self.tester.find_element_by_id_and_tap('android:id/button1')

            Log.logger.info(u"设备：%s 开始安装测试的nice包" % self.tester.device.devicename)
            thread = threading.Thread(target=self.install_process)
            thread.start()
            self.install_app()
            thread.join()
            Log.logger.info(u"设备：%s 启动成功" % self.tester.device.devicename)
            self.login_process()
            Log.logger.info(u"设备：%s 登录成功" % self.tester.device.devicename)
            self.login_success_process()
            self.get_permission_process()
            time.sleep(3)
            self.tester.clean_mp4_file()  # 预处理时清除sd的mp4文件
            Log.logger.info(u"设备：%s 预处理成功，开始执行测试用例" % self.tester.device.devicename)
        except  Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)
            return False
        """
        return True

    def install_process(self):
        pass
