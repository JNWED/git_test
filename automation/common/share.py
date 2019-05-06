# -*- coding:utf-8 -*-
import os
import re
import datetime
import time
import subprocess
from psutil import process_iter
from signal import SIGTERM


class global_var:
    run_mode = 'autotest'
    run_type = "stable"
    if_run = False
    task_id = 0


def set_run_mode(value):
    global_var.run_mode = value


def get_run_mode():
    return global_var.run_mode

def set_run_type(value):
    global_var.run_type = value

def get_run_type():
    return global_var.run_type

def set_if_run(value):
    global_var.if_run = value


def get_if_run():
    return global_var.if_run


def set_taskid(value):
    global_var.task_id = value


def get_taskid():
    return global_var.task_id


def get_format_currenttime():
    return datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")


def clean_brackets_from_str(string):
    final_string = re.sub(r'[\(（][\s\S]*[\)）]', "", string)
    return final_string

def exe_command(cmdstring, timeout=None):
    """
    this function is used to call system command with timeout
    cmdstring: input command
    timeout: timeout time
    returns: return code
    """
    if timeout:
        end_time = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
    cmd = cmdstring.split(" ")
    sub = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while sub.poll() is None:
        time.sleep(0.1)
        if timeout:
            if end_time <= datetime.datetime.now():
                raise Exception("Timeout: %s" %cmdstring)
    return str(sub.returncode)


def kill_with_port(port):
    try:
        #this method may be failed due to permisssion issue
        for proc in process_iter():
            for conns in proc.connections(kind='inet'):
                if conns.laddr.port == port:
                    proc.send_signal(SIGTERM)  # or SIGKILL
                    continue
    except Exception:
        #kill with another way only work for Linux/Mac
        cmd = "lsof -t -i:%s" % port
        pid = os.popen(cmd).read()
        if(pid):
            cmd = "kill -9 %s" % pid
            #os.popen(cmd).read()
            exe_command(cmd, timeout=10)


def get_fullfile_from_path(path, ext=None):
    allfiles = []
    needExtFilter = (ext is not None)
    for root, dirs, files in os.walk(path):
        for filespath in files:
            filepath = os.path.join(root, filespath)
            extension = os.path.splitext(filepath)[1][1:]
            if needExtFilter and extension in ext:
                allfiles.append(filepath)
            elif not needExtFilter:
                allfiles.append(filepath)
    return allfiles


def get_file_name_from_path(path, ext=None):
    allfilenames = []
    needExtFilter = (ext is not None)
    for root, dirs, files in os.walk(path):
        for filespath in files:
            filename, suffix = os.path.splitext(filespath)
            extension = os.path.splitext(filespath)[1][1:]
            if needExtFilter and extension in ext:
                allfilenames.append(filename)
            elif not needExtFilter:
                allfilenames.append(filename)
    return allfilenames
