# -*- coding:utf-8 -*-
import os
import re
import requests
from common.dataprovider import DataProvider
from common.log import Log


class DeviceManager(object):
    connectdeviceid = []
    testdevices = {}
    serverdevices = {}
    disconnectdevices = {}
    connectimei = []
    logger = None

    @classmethod
    def get_connect_deviceid(cls):
        #for android devices
        p = os.popen('adb devices')
        outstr = p.read()
        android_deviceid = re.findall(r'(\w+)\s+device\s',outstr)
        if 0 == len(android_deviceid):
            Log.logger.warn('None android device has been detected')
        else:
            cls.connectdeviceid = list(android_deviceid)
        #start checking iOS
        p = os.popen('idevice_id -l')
        outstr = p.read()
        ios_deviceid = outstr.rstrip()
        if 0 == len(ios_deviceid):
            Log.logger.warn('None iOS device has been detected')
        else:
            ios_devices = ios_deviceid.split('\n')
            for device in ios_devices:
                cls.connectdeviceid.append(device)
        return cls.connectdeviceid

    @classmethod
    def get_test_device(cls):
        for deviceid in cls.connectdeviceid:
            if deviceid in DataProvider.devices:
                cls.testdevices[deviceid] = DataProvider.devices[deviceid]
            else:
                Log.logger.warn(
                    'device: %s does not in configure file' %
                    deviceid)

        if len(cls.testdevices) == 0:
            Log.logger.warn('No test devices')

    @classmethod
    def get_server_test_device(cls):
        for deviceid, device in DataProvider.devices.iteritems():
            url = "http://%s:%s/wd/hub" % (device.server, device.serverPort)
            response = None
            try:
                response = requests.request("get", url)
            except requests.RequestException:
                pass
            if response is not None:
                cls.serverdevices[deviceid] = device
            else:
                cls.disconnectdevices[deviceid] = device

    @classmethod
    def get_connect_device_imei(cls):
        # for android
        for device in cls.connectdeviceid:
            cmd = "adb -s %s shell service call iphonesubinfo 1 | awk -F \"'\" '{print $2}' | sed '1 d' | tr -d '.' | awk '{print}' ORS=" % device
            p = os.popen(cmd)
            outstr = p.read()
            Log.logger.info('device: ' % device)
            Log.logger.info('outStr:' % outstr)

    @classmethod
    def get_device_info(cls, deviceId):
        # for android
        mode = "ro.product.model"
        release = "ro.build.version.release"
        getmode = "adb -s %s shell cat /system/build.prop |grep %s" % (
            deviceId, mode)
        getrelease = "adb -s %s shell cat /system/build.prop |grep %s" % (
            deviceId, release)
        p1 = os.popen(getmode)
        p2 = os.popen(getrelease)
        modename = p1.read()
        releasename = p2.read()
        Log.logger.info('deviceId: ' % deviceId)
        Log.logger.info('modename:' % modename)
        Log.logger.info('releasename:' % releasename)


if __name__ == "__main__":
    DeviceManager.get_connect_deviceid()
