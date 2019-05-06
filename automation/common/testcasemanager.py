# -*- coding:utf-8 -*-
from common.basetestcase import BaseTestCase
from common.device import Device
import share
import unittest


class TestCaseManager(object):

    def __init__(self, tester):
        self.functional_suite = unittest.TestSuite()
        self.testcase_class = []
        self.tester = tester
        self.load_case()

    def load_case(self):
        testcase_array = []
        test_type = share.get_run_type()
        if (test_type == "stable"):
            testcase_folder = 'testcase/' + self.tester.device.platformName + '/'
        else:
            testcase_folder = 'testcase/' + self.tester.device.platformName + '/' + test_type + '/'
        testsuits = unittest.defaultTestLoader.discover(
            testcase_folder, pattern='test*.py')
        for testsuite in testsuits:
            for suite in testsuite._tests:
                for test in suite:
                    testcase_array.append(test.__class__)
        self.testcase_class = sorted(
            set(testcase_array),
            key=testcase_array.index)

    # function test
    def functional_testsuite(self):
        for testcase in self.testcase_class:
            self.functional_suite.addTest(
                BaseTestCase.parametrize(
                    testcase, tester=self.tester))
        return self.functional_suite

    def signal_case_suit(self, test_myclass):
        suite = unittest.TestSuite()
        suite.addTest(
            BaseTestCase.parametrize(
                test_myclass,
                tester=self.tester))
        return suite
