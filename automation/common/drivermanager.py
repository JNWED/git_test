# -*- coding:utf-8 -*-


class DriverManager(object):

    drivers = {}

    @classmethod
    def quit_all_driver(cls):
        print cls.drivers
        for driver in cls.drivers.iteritems():
            if driver is not None:
                driver[1].quit()

    @classmethod
    def quit_driver(cls, deviceid):
        if deviceid in cls.drivers:
            if cls.drivers[deviceid] is not None:
                cls.drivers[deviceid].quit()
