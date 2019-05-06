"""
server manager module
"""
# -*- coding:utf-8 -*-
import threading
from server import Server
from common.log import Log
from common.devicemanager import DeviceManager


class ServerManager():
    def __init__(self):
        '''
        server init
        '''
        self.testdevices = DeviceManager.testdevices
        self.disconnectdevices = DeviceManager.disconnectdevices
        self.serverobjects = []
        self.threads = []
        self.logger = Log.logger

    def start_all_server(self):
        '''
        start all server
        '''
        for device in self.testdevices.iteritems():
            server = Server(device)
            self.serverobjects.append(server)
            thread1 = threading.Thread(target=server.start)
            thread1.start()

    def stop_all_server(self):
        '''
        stop all server
        '''
        for server in self.serverobjects:
            server.stop()

    def list_devices(self):
        '''
        list devices
        '''
        self.logger.info("Connected devices:")
        for device in self.testdevices.iteritems():
            server = Server(device)
            server.list_connect_devices()
