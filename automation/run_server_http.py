# -*- coding:utf-8 -*-

import sys
import time
from SocketServer import ThreadingTCPServer
from server.server import Server
from common.httpserverhandler import HttpServerHandler
from common.log import Log
from common.share import kill_with_port
from common.dataprovider import DataProvider
from common.devicemanager import DeviceManager

def kill_server(port):
    """
    Kill server with port
    Need to be fixed
    """
    kill_with_port(port)


def start_server():
    """
    Start server
    """
    myport = 8886
    kill_server(myport)
    host = "127.0.0.1"
    port = myport
    addr = (host, port)
    Log.logger.debug('Start Server...')
    server = ThreadingTCPServer(addr, HttpServerHandler)
    #server.serve_forever()
    server.handle_request()


def main():
    """
    The main function
    """
    Log.create_log_file()
    Log.logger.info("Loading devices and user info")
    DataProvider.init_data()
    Log.logger.info("Detected the test devices at this server")
    DeviceManager.get_server_test_device()

    if not DeviceManager.serverdevices:
        time.sleep(10)
        Log.logger.info("Detected test devices again")
        DeviceManager.get_server_test_device()
        if not DeviceManager.serverdevices:
            Log.logger.info("No testable device at this server")
            sys.exit()
    DeviceManager.get_connect_deviceid()
    if not DeviceManager.connectdeviceid:
        Log.logger.error("No connect test device!")
        sys.exit()
    else:
        DeviceManager.get_test_device()
        for device in DeviceManager.testdevices.items():
            server = Server(device)
            server.list_connect_devices()

    start_server()


if __name__ == '__main__':
    main()
