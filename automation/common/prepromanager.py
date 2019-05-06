# -*- coding:utf-8 -*-
from prepro.huawei10preprocess import HuaWei10PreProcess
from prepro.iphone7preprocess import Iphone7PreProcess
from prepro.minote2preprocess import MiNote2PreProcess
from prepro.google_pixel_2xlpreprocess import Pixel2XLPreProcess
from prepro.huaweip20preprocess import HuaWeiP20PreProcess
from prepro.xiaomi6preprocess import Xiaomi6PreProcess
from prepro.huaweinova3epreprocess import HuaWeiNova3ePreProcess

class PreProManager(object):

    def __init__(self, tester):
        self.tester = tester
        self.deviceid = self.tester.device.deviceUdid

    def device(self):
        current_test_device = self.tester.device.deviceName
        current_test_platform = self.tester.device.platformName
        if current_test_platform == "iOS":
            return Iphone7PreProcess(self.tester)
        elif current_test_device == "Huawei_10":
            return HuaWei10PreProcess(self.tester)
        elif current_test_device == "Xiaomi_Note2":
            return MiNote2PreProcess(self.tester)
        elif current_test_device == "Google_Pixel2_XL":
            return Pixel2XLPreProcess(self.tester)
        elif current_test_device == "Huawei_P20":
            return HuaWeiP20PreProcess(self.tester)
        elif current_test_device == "Xiaomi_6":
            return Xiaomi6PreProcess(self.tester)
        elif current_test_device == "Huawei_Nova3e":
            return HuaWeiNova3ePreProcess(self.tester)
        elif current_test_device == "Xiaomi_8":
            return MiNote2PreProcess(self.tester)
        else:
            print "No matched preprocess model!"
