# -*- coding:utf-8 -*-
import sys
import os
import yaml
import platform
from common.log import Log
from common.device import Device
from common.user import User

# YAML被很多人认为是可以超越xml和json的文件格式。
# 对比xml，除了拥有xml的众多优点外，它足够简单，易于使用。而对于json，YAML可以写成规范化的配置文件
# YAML使用冒号加缩进的方式代表层级（属性）关系，使用短横杠(-)代表数组元素

class DataProvider(object):
    users = [] # 列表（类似数组）
    devices = {} # 字典，key-value方式存储
    config = None
    testers = {}
    starttime = {}
    stoptime = {}
    devicenamelist = []

    @classmethod
    def init_data(cls):
        cls.init_config_yaml()
        cls.load_devices()
        cls.load_users()
        cls.show_devicename_list()

    @classmethod
    def init_config_yaml(cls):
        filepath = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..")) + '/configure/config.yaml'
        currentplatform = platform.system()
        if(currentplatform == 'Windows'):
            filepath = filepath.replace("\\", '/')

        with open(filepath, 'r') as stream:
            try:
                cls.config = yaml.load(stream)
            except yaml.YAMLError as exc:
                Log.logger.error('failed to open configure file')
                Log.logger.error(exc)
            finally:
                stream.close()

    @classmethod
    def load_devices(cls):#cls代表类方法，self代表成员方法
        cls.devicenamelist = []
        for device in cls.config['Devices']:
            deviceobject = Device(device['udid'])
            deviceobject.deviceName = device['deviceName']
            deviceobject.platformName = device['platformName']
            deviceobject.platformVersion = device['platformVersion']
            deviceobject.serverPort = device['serverPort']
            deviceobject.bootstrapPort = device['bootstrapPort']
            deviceobject.deviceStatus = device['status']
            deviceobject.server = device['server']
            deviceobject.app = device['app']
            deviceobject.appPackage = device['appPackage']
            deviceobject.appActivity = device['appActivity']

            cls.devices[deviceobject.deviceUdid] = deviceobject # 将yaml配置中的设备加入dataprovider的类变量中
                                                                # 设备实例存储在devices字典中
            cls.devicenamelist.append(device['deviceName'])
        Log.logger.info(
            "Detected %s set devices in configure file" % len(
                cls.devices))

    @classmethod
    def load_users(cls):
        for user in cls.config['Users']:
            userobject = User(user['uid'])
            userobject.userName = user['userName']
            userobject.upassword = user['upassword']
            userobject.mobile = user['mobile']
            userobject.mpassword = user['mpassword']
            userobject.email = user['email']
            userobject.epassword = user['epassword']

            cls.users.append(userobject) # 用户实例存储在users列表中
        Log.logger.info("Detected %s User info" % len(cls.users))

    @classmethod
    def show_devicename_list(cls):
        Log.logger.info("Show devicename:")
        for i in range(len(cls.devicenamelist)):
            Log.logger.info(cls.devicenamelist[i])
            i += 1


if __name__ == "__main__":
    Log.create_log_file()
    DataProvider.init_data()
