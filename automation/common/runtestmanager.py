# -*- coding:utf-8 -*-
import traceback
import time
import datetime
import os
import sys
import threading
#from pyunitreport import HTMLTestRunner
import xmlrunner
import unittest
from appium import webdriver
from common.devicemanager import DeviceManager
from common.testcasemanager import TestCaseManager
from common.testresult import TestResult
from common.dataprovider import DataProvider
from common.drivermanager import DriverManager
from common.prepromanager import PreProManager
from common.tester import Tester
import share
from common.log import Log
from server.servermanager import ServerManager


class RunTestManager(object):

    def __init__(self, mode):
        self.count_testcases = 0
        self.task_id = int(time.time())
        self.logger = Log.logger
        self.mode = mode

    def start_run(self):
        try:
            self.logger.debug('Start run %s...' % self.mode)
            if self.mode == "autotest":
                TestResult.create_result_folder()

            if self.mode == "other":
                # TBD
                pass

            Log.logger.info("Start running task...")
            self.start_run_test()

            if self.mode == "autotest":
                Log.logger.debug("Start creating test report...")
                TestResult.generate_html_testresult()

            if self.mode == "other":
                # TBD
                pass
            Log.logger.info("Finish the task")
            DriverManager.quit_all_driver()
            self.stop_run()
        except Exception:
            traceback.print_exc()
            self.stop_run()

    def stop_run(self):
        share.set_if_run(False)
        #for jenkins support
        share.kill_with_port(8886)
        sys.exit()

    def run(self, tester):
        try:
            startTime = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            DataProvider.starttime[tester.device.deviceUdid] = startTime
            PreProManager(tester).device().pre_process()
            if self.mode == "autotest":
                Log.logger.info(
                    "Device:%s ---Start to run autotest---" %
                    tester.device.deviceName)
                Log.logger.info(
                    "Device:%s Start to Load test case..." %
                    tester.device.deviceName)
                suite = TestCaseManager(tester).functional_testsuite()
                Log.logger.info(
                    "Device:%s Loaded test cases" %
                    tester.device.deviceName)
                Log.logger.info(
                    "Device:%s Start to run cases..." %
                    tester.device.deviceName)
                """
                # Use HTMLTestRunner to generate HTML report
                kwargs = {
                    "output": "testresult",
                    "report_name": "NetMusic_UI_Test_Report",
                    "failfast": False
                }
                runner = HTMLTestRunner(**kwargs)
                """
                #Use XMLTestRunner to generate XML report
                runner = xmlrunner.XMLTestRunner(output='testresult')
                runner.run(suite)
                """
                runner = unittest.TextTestRunner(
                    verbosity=2, resultclass=TestResult)
                runner.run(suite)
                """
                Log.logger.info(
                    "Device:%s Finshed all the cases" %
                    tester.device.deviceName)
            endTime = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            DataProvider.stoptime[tester.device.deviceUdid] = endTime
        except Exception:
            Log.logger.info(
                "Device:%s is abormal, please double check" %
                tester.device.deviceName)
            traceback.print_exc()

    def init_tester_data(self, device, which_user):
        try:
            desired_caps = {}
            desired_caps['app'] = device.app
            if device.appPackage:
                desired_caps['appPackage'] = device.appPackage
            if device.appActivity:
                desired_caps['appActivity'] = device.appActivity
            desired_caps['platformName'] = device.platformName
            desired_caps['platformVersion'] = device.platformVersion
            desired_caps['deviceName'] = device.deviceName
            desired_caps['autoLaunch'] = True
            desired_caps['udid'] = device.deviceUdid
            desired_caps['noReset'] = True
            desired_caps['fullReset'] = False
            desired_caps['unicodeKeyboard'] = False
            desired_caps['resetKeyboard'] = False
            #workaround solution for iOS crash issue with appium
            if device.platformName == "iOS":
                desired_caps['autoAcceptAlerts'] = True
                desired_caps['processArguments'] = {"args": ["appium"], "env": {"ui": "test"}}
                desired_caps['automationName'] = "XCUITest"
                which_user = which_user + 1
                #for iOS, it uses another user info
            else:
                #for Android
                desired_caps['autoGrantPermissions'] = True

            #desired_caps['newCommandTimeout'] = 3000
            url = "http://%s:%s/wd/hub" % (device.server, device.serverPort)
            driver = webdriver.Remote(url, desired_caps)

            if self.mode == "autotest":
                folderpath = '%s/%s' % (TestResult.testresultpath,
                                        device.deviceName)
                os.mkdir(folderpath)

            testerobject = Tester(driver)
            testerobject.device = device
            testerobject.user = DataProvider.users[which_user]
            testerobject.logger = Log.logger
            if self.mode == "autotest":
                testerobject.screenshot_path = folderpath
            DriverManager.drivers[device.deviceUdid] = driver
            return testerobject
        except Exception:
            Log.logger.info("Device:%s is abormal!" % device.deviceName)
            traceback.print_exc()

    def start_run_test(self):
        which_user = 0
        threads = []
        for deviceUdid, device in DeviceManager.testdevices.iteritems():
            testerobject = self.init_tester_data(device, which_user)
            DataProvider.testers[device.deviceUdid] = testerobject
            try:
                thread = threading.Thread(
                    target=self.run, args=(testerobject,))
                thread.start()
                #first use one user account
                #which_user = which_user + 1
                threads.append(thread)
            except Exception:
                traceback.print_exc()
                DataProvider.testers[deviceUdid].driver.quit()

        for thread in threads:
            thread.join()
