# -*- coding:utf-8 -*-

import requests
import time
import json
from optparse import OptionParser


def main():
    '''
    current only support autotest
    will enable more later
    '''

    ip_addr = '127.0.0.1'
    port = '8886'

    parser = OptionParser(usage="usage:%prog [options] arg1 arg2")
    parser.add_option("-t", "--type",
                action = "store",
                type = 'string',
                dest = "test_type",
                default = "stable",
                )
    parser.add_option("-m", "--mode",
                action = "store",
                type = "string",
                dest = "test_mode",
                default = "autotest",
                )

    url = 'http://' + ip_addr + ':' + port + '/run?'
    (options, args) = parser.parse_args()
    #testype = quick or slow or stable
    data = {"mode":"autotest", "testype":"stable"}
    data["mode"] = options.test_mode
    data["testype"] = options.test_type

    # for Jenkins's support
    # wait for 10s for server to get ready
    time.sleep(10)
    #url = 'http://127.0.0.1:8886/run?mode=autotest'
    try:
        response = requests.get(url, data)
        resjson = response.json()
        print resjson
    except:
        print "Server is not ready, try again!"
        pass


if __name__ == '__main__':
    main()
