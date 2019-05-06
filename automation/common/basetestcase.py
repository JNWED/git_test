# -*- coding:utf-8 -*-

import unittest
import time
import os
import traceback
from common.log import Log


class BaseTestCase(unittest.TestCase):
    def __init__(self, methodName='runTest', tester=None):
        super(BaseTestCase, self).__init__(methodName)
        self.tester = tester

    @staticmethod
    def parametrize(testcase_klass, tester=None):
        testloader = unittest.TestLoader()#TestLoader是用来加载TestCase到TestSuite中的
                                          # 从各个地方寻找TestCase，创建它们的实例，然后add到TestSuite中，再返回一个TestSuite实例
        testnames = testloader.getTestCaseNames(testcase_klass)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(testcase_klass(name, tester=tester))
        return suite
