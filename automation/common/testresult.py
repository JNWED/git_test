# -*- coding:utf-8 -*-
import re
import sys
import os

import unittest
import share
import collections
from datetime import datetime
from pyh import * #使用它在python程序中生成HTML内容
                  # 第三方库安装，python setup.py install
import traceback
from common.drivermanager import DriverManager
from common.dataprovider import DataProvider
from common.log import Log

#生成htlm测试报告
class TestResult(unittest.TestResult):

    detailresults = {}  # {"5HUC9S6599999999":{},"":{}}
    totalresults = {}
    device = {}
    testresultpath = ""
    filecss = ""
    filejs = ""

    def __init__(self, stream=None, descriptions=None, verbosity=None):
        unittest.TestResult.__init__(
            self, stream=None, descriptions=None, verbosity=None)
        self.logger = Log.logger
        self._testcasedict = collections.OrderedDict()
        self.if_write_starttime = False

    def startTest(self, test):
        self.tester = test.tester
        self.deviceid = self.tester.device.deviceUdid
        testcase_starttime = share.get_format_currenttime()
        self.logger.debug(
            "Device: %s Start Run %s" %
            (self.tester.device.deviceName, test))
        print test.id()

        if self.deviceid in self.__class__.totalresults:
            pass
        else:
            self.__class__.totalresults[self.deviceid] = collections.OrderedDict(
            )
            self.__class__.totalresults[self.deviceid]['totalrun'] = 0
            self.__class__.totalresults[self.deviceid]['startime'] = 0
            self.__class__.totalresults[self.deviceid]['stoptime'] = 0
            self.__class__.totalresults[self.deviceid]['errortestcase'] = 0
            self.__class__.totalresults[self.deviceid]['failtestcase'] = 0
            self.__class__.totalresults[self.deviceid]['skiptestcase'] = 0
            self.__class__.totalresults[self.deviceid]['successtestcase'] = 0

        self.__class__.totalresults[self.deviceid]['totalrun'] = self.__class__.totalresults[self.deviceid]['totalrun'] + 1

        if self.if_write_starttime:
            pass
        else:
            self.__class__.totalresults[self.deviceid]['starttime'] = testcase_starttime
            self.if_write_starttime = True

        self._testcasedict[test] = collections.OrderedDict()
        if self.deviceid in self.__class__.detailresults:
            pass
        else:
            self.__class__.device[self.deviceid] = self.tester.device
            self.__class__.detailresults[self.deviceid] = self._testcasedict
        self.__class__.detailresults[self.deviceid][test]['startime'] = testcase_starttime

    def stopTest(self, test):
        testcase_stoptime = share.get_format_currenttime()
        self.logger.debug(
            'Device: %s Stop Run %s' %
            (self.tester.device.deviceName, test))
        self.__class__.detailresults[self.deviceid][test]['stoptime'] = testcase_stoptime
        testcase_consumingtime = self.__class__.get_time_consuming(
            self.__class__.detailresults[self.deviceid][test]['startime'], self.__class__.detailresults[self.deviceid][test]['stoptime'])
        self.__class__.detailresults[self.deviceid][test]['consumingtime'] = testcase_consumingtime
        self.__class__.totalresults[self.deviceid]['stoptime'] = testcase_stoptime

    def startTestRun(self):
        self.logger.debug('start test')
        pass

    def stopTestRun(self):
        self.logger.debug('finish test')
        pass

    def addError(self, test, err):
        info = '************      - %s -!(Error)    ***************' % self.tester.device.deviceName
        self.logger.warning(info)
        # traceback.print_tb(err[2])
        traceback.print_exc()
        info = 'Error device:%s Run TestCase %s, Error info:%s' % (
            self.tester.device.deviceName, test, traceback.format_exception(err[0], err[1], err[2]))
        self.logger.error(info)
        info = '************************************************'
        self.logger.warning(info)

        mytest = str(test)
        simplename = share.clean_brackets_from_str(mytest).replace(' ', '')
        myscr = "Error_%s" % simplename
        self.tester.screenshot(myscr)

        list = traceback.format_exception(err[0], err[1], err[2])
        list_err = []
        list_err.append(list[-1])
        list_err.append(list[2])

        if self.deviceid in self.__class__.totalresults:
            self.__class__.totalresults[self.deviceid]['errortestcase'] = self.__class__.totalresults[self.deviceid]['errortestcase'] + 1
        else:
            self.__class__.totalresults[self.deviceid]['errortestcase'] = 0

        try:
            self.__class__.detailresults[self.deviceid][test]['result'] = 'Error'
            self.__class__.detailresults[self.deviceid][test]['reason'] = list_err
        except Exception as e:
            info = Exception, ":", e
            self.logger.error(info)

    def addFailure(self, test, err):
        info = '************      - %s -!(Fail)    ***************' % self.tester.device.deviceName
        self.logger.warning(info)
        info = 'Fail device:%s Run TestCase %s, Fail info:%s' % (
            self.tester.device.deviceName, test, err[1].message)
        self.logger.warning(info)
        info = '***********************************************'
        self.logger.warning(info)

        mytest = str(test)
        simplename = share.clean_brackets_from_str(mytest).replace(' ', '')
        myscr = "Failure_%s" % simplename
        self.tester.screenshot(myscr)

        list = traceback.format_exception(err[0], err[1], err[2])
        list_fail = []
        list_fail.append(list[-1])
        list_fail.append(list[2])

        self.__class__.totalresults[self.deviceid]['failtestcase'] = self.__class__.totalresults[self.deviceid]['failtestcase'] + 1

        self.__class__.detailresults[self.deviceid][test]['result'] = 'Fail'
        self.__class__.detailresults[self.deviceid][test]['reason'] = list_fail

    def addSuccess(self, test):
        self.__class__.totalresults[self.deviceid]['successtestcase'] = self.__class__.totalresults[self.deviceid]['successtestcase'] + 1

        self.__class__.detailresults[self.deviceid][test]['result'] = 'Success'
        self.__class__.detailresults[self.deviceid][test]['reason'] = 'None'

    def addSkip(self, test, reason):
        info = 'Skip Run TestCase %s, Skip reason:%s' % (test, reason)
        self.logger.debug(info)
        self.__class__.totalresults[self.deviceid]['skiptestcase'] = self.__class__.totalresults[self.deviceid]['skiptestcase'] + 1

        self.__class__.detailresults[self.deviceid][test]['result'] = 'Skip'
        self.__class__.detailresults[self.deviceid][test]['reason'] = reason

    @classmethod
    def get_time_consuming(cls, starttime, endtime):
        starttime = datetime.strptime(starttime, "%Y_%m_%d_%H_%M_%S")
        endtime = datetime.strptime(endtime, "%Y_%m_%d_%H_%M_%S")
        timeconsuming = endtime - starttime

        if timeconsuming.seconds <= 0:
            timestr = '<1s'
        else:
            timestr = '%s s' % timeconsuming.seconds
        return timestr

    @classmethod
    def create_result_folder(cls):
        cls.testresultpath = os.getcwd() + '/testresult/%s' % share.get_format_currenttime()
        os.mkdir(cls.testresultpath)

    filecss = os.getcwd() + '/testresult/result.css'
    filejs = os.getcwd() + '/testresult/result.js'
    sorttablejs = os.getcwd() + '/testresult/sorttable.js'

    @classmethod
    def generate_html_testresult(cls):
        page = PyH('Test Report')
        result_title = "Auto Test Report"

        page.addCSS(cls.filecss)
        page.addJS(cls.filejs)
        page.addJS(cls.sorttablejs)
        homediv = page << div(id='nice_report', cl='nice_header_passed')
        reporttitle = homediv << div(result_title, id='title')

        reportsummary = homediv << div(id='summary')
        # TO be fix
        reportsummary << p("com.netease.cloudmusic")
        reportsummary << p("5.3")
        reportsummary << p("haha")

        tabdiv = page << div(id="Tab1")
        menuboxdiv = tabdiv << div(cl="Menubox")
        contentdiv = tabdiv << div(cl="Contentbox")

        tabul = menuboxdiv << ul()
        index = 1
        size = len(cls.detailresults)
        for deviceid, testresult in cls.detailresults.iteritems():
            tabstr = "setTab('one',%s, %s)" % (index, size)
            liid = "one%s" % index
            if index == 1:
                tabul << li(
                    cls.device[deviceid].deviceName,
                    id=liid,
                    onmouseover=tabstr,
                    cl="hover")
            else:
                tabul << li(
                    cls.device[deviceid].deviceName,
                    id=liid,
                    onmouseover=tabstr)

            content_div_id = "con_one_%s" % index
            if index == 1:
                detaildiv = contentdiv << div(id=content_div_id, cl="hover")
            else:
                detaildiv = contentdiv << div(
                    id=content_div_id, style="display:none")

            totaldiv = detaildiv << div(id='Total')
            totallabel = totaldiv << p('Device result summary:', align="left")
            totalresulttable = totaldiv << table(
                cl='totalResult', border="1", cellpadding="15")
            # totalresulttable.attributes['class'] = 'totalResult'
            result_title_tr = totalresulttable << tr()
            result_value_tr = totalresulttable << tr()
            ordertitle = collections.OrderedDict()
            timeconsuming = cls.get_time_consuming(
                cls.totalresults[deviceid]['starttime'],
                cls.totalresults[deviceid]['stoptime'])
            ordertitle['Start time'] = DataProvider.starttime[deviceid]
            try:
                ordertitle['End time'] = DataProvider.stoptime[deviceid]
            except BaseException:
                ordertitle['End time'] = ordertitle['Start time']
                Log.logger.debug(
                    '%s stoptime: connect error, use default time instead' %
                    cls.device[deviceid].deviceName)

            ordertitle['Total time'] = timeconsuming
            ordertitle['Total cases'] = cls.totalresults[deviceid]['totalrun']
            ordertitle['Passed cases'] = cls.totalresults[deviceid]['successtestcase']
            ordertitle['Failed cases'] = cls.totalresults[deviceid]['failtestcase']
            ordertitle['Wrong cases'] = cls.totalresults[deviceid]['errortestcase']
            ordertitle['Skipped cases'] = cls.totalresults[deviceid]['skiptestcase']

            for title, value in ordertitle.iteritems():
                result_title_tr << td(title)
                temp = result_value_tr << td(value)
                temp.attributes['class'] = title

            detaillabel = detaildiv << p('Detailed report:', align="left")
            detail_table_title = (
                'test case',
                'start time',
                'end time',
                'time',
                'test result',
                'reason')
            detailresulttable = detaildiv << table(
                cl='sortable',
                width="100%",
                border="1",
                cellpadding="2",
                cellspacing="1",
                style="table-layout:fixed")
            detail_title_tr = detailresulttable << tr()
            for title in detail_table_title:
                detail_title_tr << td(title)
            for key, values in cls.detailresults[deviceid].iteritems():
                testcasetr = detailresulttable << tr()
                mykey = str(key)
                final_key = share.clean_brackets_from_str(mykey)
                testcasetr << td(
                    final_key,
                    align='left',
                    width="100%",
                    style="word-break:break-all")
                testcasetr << td(values['startime'])
                testcasetr << td(values['stoptime'])
                testcasetr << td(values['consumingtime'])
                try:
                    testcasetr << td(values['result'])
                except BaseException:
                    testcasetr << td('device connect error')
                    Log.logger.debug(
                        '%s result: device connect error, use default values instead' %
                        cls.device[deviceid].deviceName)
                try:
                    testcasetr << td(
                        values['reason'],
                        width="100%",
                        style="word-break:break-all")
                except BaseException:
                    testcasetr << td('session error')
                    Log.logger.debug(
                        '%s reason: device connect error, use default values instead' %
                        cls.device[deviceid].deviceName)

            screencaplable = detaildiv << div(id='screencap')

            screencapdiv = detaildiv << p('screen cap:', align="left")

            screecap_path = "%s/%s/" % (cls.testresultpath,
                                        cls.device[deviceid].deviceName)
            screencap_table_title = share.get_file_name_from_path(
                screecap_path, 'png')
            screencap_img_src = share.get_fullfile_from_path(
                screecap_path, 'png')

            screencapresulttable = screencapdiv << table(
                width="auto",
                border="1",
                cellpadding="2",
                cellspacing="1",
                style="table-layout:fixed")

            screencap_title_tr = screencapresulttable << tr()

            screencap = screencapresulttable << tr()

            for title in screencap_table_title:
                screencap_title_tr << td(title)
            for path in screencap_img_src:
                screencap << td(
                    "<img src=%s alt=%s width='170' height='300'> " %
                    (path, title))

            screenrecordlable = detaildiv << div(id='screenrecord')
            screenrecorddiv = detaildiv << p('video:', align="left")

            screerecord_path = "%s/%s/" % (cls.testresultpath,
                                           cls.device[deviceid].deviceName)
            screenrecord_table_title = share.get_file_name_from_path(
                screerecord_path, 'mp4')
            screenrecord_video_src = share.get_fullfile_from_path(
                screerecord_path, 'mp4')

            screenrecordresulttable = screenrecorddiv << table(
                width="auto",
                border="1",
                cellpadding="2",
                cellspacing="1",
                style="table-layout:fixed")

            screenrecord_title_tr = screenrecordresulttable << tr()

            screenrecord = screenrecordresulttable << tr()

            for title_video in screenrecord_table_title:
                screenrecord_title_tr << td(title_video)
            for path_video in screenrecord_video_src:
                screenrecord << td(
                    "<video width='240' height='320' controls='controls'> "
                    "<source src=%s type='video/mp4' /></video>" %
                    path_video)

            errorlable = detaildiv << div(id='errorrecord')
            errordiv = detaildiv << p('wrong screen capture:', align="left")

            error_path = "%s/%s/" % (cls.testresultpath,
                                     cls.device[deviceid].deviceName)
            error_table_title = share.get_file_name_from_path(
                error_path, 'jpg')
            error_src = share.get_fullfile_from_path(screerecord_path, 'jpg')

            errorresulttable = errordiv << table(
                width="auto",
                border="1",
                cellpadding="2",
                cellspacing="1",
                style="table-layout:fixed")

            error_title = errorresulttable << tr()
            error_valus = errorresulttable << tr()

            for title_error in error_table_title:
                error_title << td(title_error)
            for path_error in error_src:
                error_valus << td(
                    "<img src=%s alt=%s width='170' height='300'> " %
                    (path_error, title))

            index = index + 1

        htmltestresultfile = '%s/%s.html' % (
            cls.testresultpath, share.get_format_currenttime())
        try:
            page.printOut(htmltestresultfile)
        except IOError:
            Log.logger.error('file %s not exist' % htmltestresultfile)
            DriverManager.quit_all_driver()

        else:
            Log.logger.debug(
                'Finshed test report Path:%s' %
                htmltestresultfile)

        pass


if __name__ == '__main__':
    TestResult().generate_html_testresult()
