# -*- coding:utf-8 -*-

import sys
from common.devicemanager import DeviceManager
from common.log import Log
from common.dataprovider import DataProvider
from server.servermanager import ServerManager


def run():
    '''
    Start server
    '''
    Log.create_log_file()

    Log.logger.info("Load devices and user config info")
    DataProvider.init_data()

    Log.logger.info("Detected Android Devices")
    DeviceManager.get_connect_deviceid()

    if DeviceManager.connectdeviceid is False:
        Log.logger.info("No device!")
        sys.exit()
    else:
        connected_device_num = "Connected devices number: " + \
                str(len(DeviceManager.connectdeviceid))
        Log.logger.info(connected_device_num)

    Log.logger.info("Detected test devices")
    DeviceManager.get_test_device()
    DeviceManager.get_server_test_device()

    servermanager = ServerManager()
    servermanager.list_devices()
    servermanager.start_all_server()


if __name__ == "__main__":
    run()
