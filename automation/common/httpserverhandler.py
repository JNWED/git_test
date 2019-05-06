# -*- coding:utf-8 -*-
import share
import urlparse
import threading
import json
import re
import SimpleHTTPServer
import traceback
from common.log import Log
from common.runtestmanager import RunTestManager


class HttpServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    run_manager = None

    def end_headers(self):
        self.send_my_headers()
        SimpleHTTPServer.SimpleHTTPRequestHandler.end_headers(self)

    def send_my_headers(self):
        self.send_header(
            "Cache-Control",
            "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")

    def do_POST(self):
        self.logger = Log.logger
        self.logger.warning("--------- POST ---------")

    def do_GET(self):
        self.logger = Log.logger
        self.logger.warning("--------- GET ---------")
        self.logger.warning(self.path)
        parsedParams = urlparse.urlparse(self.path)
        queryParsed = urlparse.parse_qs(parsedParams.query)

        if parsedParams.path == '/run':
            self.run(queryParsed)
        else:
            result_dict = {'code': 1001, "data": {"message": "wrong command"}}
            self.set_response(result_dict)

    def run(self, params):
        if share.get_if_run():
            result_dict = {
                'code': 1002,
                "data": {
                    "message": "one task is running",
                    "taskid": "%s" %
                    share.get_taskid()}}
            self.set_response(result_dict)
            return
        if ('mode' in params) == False:
            result_dict = {'code': 1003, "data": {"message": "without mode"}}
            self.set_response(result_dict)
            return
        elif params['mode'][0] != "monkey" and params['mode'][0] != 'autotest':
            self.set_response(
                {'code': 1004, "data": {"message": "wrong mode"}})
            return
        if ('testype' in params):
            if (params['testype'][0] != "quick"
            and params['testype'][0] != "slow"
            and params['testype'][0] != "stable"
            and params['testype'][0] != "debug"
            ):
                self.set_response({'code': 1005, "data": {"message": "wrong test type"}})
                return
            else:
                share.set_run_type(params['testype'][0])
        try:
            set_run_manager(RunTestManager(params['mode'][0]))
            self.taskid = get_run_manager().task_id
            share.set_taskid(get_run_manager().task_id)
            share.set_if_run(True)
            thread = threading.Thread(target=get_run_manager().start_run)
            thread.start()
            result_dict = {
                'code': 0,
                "data": {
                    "taskid fuck": "%s" %
                    self.taskid,
                    "message": "start running %s task" %
                    params['mode']}}
            self.set_response(result_dict)
        except Exception:
            traceback.print_exc()
            get_run_manager().stop_run()

    def set_response(self, text, code=200):
        try:
            result = json.dumps(text, ensure_ascii=False)
        except Exception:
            traceback.print_exc()
            result = text
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(result)


def get_run_manager():
    return HttpServerHandler.run_manager


def set_run_manager(value):
    HttpServerHandler.run_manager = value
