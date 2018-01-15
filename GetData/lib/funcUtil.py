# !/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time, datetime

# 写错误日志到 log 文件夹，会调用 traceback 将之前错误的详细信息记录到日志
def write_log(module_name, err_msg=''):
    import time, traceback

    log_dir_path = os.path.join(os.path.abspath(os.path.curdir), 'log')
    if not os.path.isdir(log_dir_path):
        os.mkdir(log_dir_path)

    log_dir_path = os.path.join(log_dir_path, module_name)
    if not os.path.isdir(log_dir_path):
        os.mkdir(log_dir_path)
    log_path = os.path.join(log_dir_path, 'log.txt')

    with open(log_path, 'a') as f:
        f.write("time: %s\n" % time.asctime(time.localtime(time.time())))
        if err_msg:
            if isinstance(err_msg, unicode):
                err_msg = err_msg.encode('utf-8')
            f.write("msg: %s\n" % err_msg)
        traceback.print_exc(file=f)
        f.write("\n\n")

def flush_thread_status(module_name, thread_id):
    tmp_dir_path = os.path.abspath(os.path.curdir)

    tmp_module_path = os.path.join(tmp_dir_path, module_name)
    if not os.path.isdir(tmp_module_path):
        os.mkdir(tmp_module_path)
    tmp_thread_path = os.path.join(tmp_module_path, str(thread_id) + '.tmp')

    with open(tmp_thread_path, 'w') as f:
        f.write(str(time.time()))

def date2seconds(date):
    return int(time.mktime(datetime.datetime.strptime(date,"%Y-%m-%d").timetuple()))

def seconds2date(seconds):
    return time.strftime("%Y-%m-%d", time.localtime(seconds))

def get_next_date(date):
    return seconds2date(date2seconds(date) + 86400)

def get_pre_date(date):
    return seconds2date(date2seconds(date) - 86400)

def get_date_list(start_date, end_date):
    start_seconds = date2seconds(start_date)
    end_seconds = date2seconds(end_date)

    ar_date = []
    while start_seconds <= end_seconds:
        ar_date.append(seconds2date(start_seconds))
        start_seconds = start_seconds + 86400
    return ar_date

# 将 string 转化成 utf-8 编码，type 变成 unicode
def decode_2_utf8(string):
    if not isinstance(string, bytes):
        return string
    import chardet
    encoding = chardet.detect(string)['encoding']
    return string.decode(encoding)

def getTmpPath(module_name, file_name):
    tmp_dir_path = os.path.join(os.path.abspath(os.path.curdir), 'tmp')
    if not os.path.isdir(tmp_dir_path):
        os.mkdir(tmp_dir_path)

    tmp_dir_path = os.path.join(tmp_dir_path, module_name)
    if not os.path.isdir(tmp_dir_path):
        os.mkdir(tmp_dir_path)

    return os.path.join(tmp_dir_path, file_name)

def recordStatus(module_name, content, mode='w'):
    tmp_path = getTmpPath(module_name, 'status.tmp')

    with open(tmp_path, mode) as f:
        f.write(content)

def recordPid(module_name, status='running', mode='w'):
    tmp_dir_path = os.path.join(os.path.abspath(os.path.curdir), 'tmp')
    if not os.path.isdir(tmp_dir_path):
        os.mkdir(tmp_dir_path)

    tmp_dir_path = os.path.join(tmp_dir_path, module_name)
    if not os.path.isdir(tmp_dir_path):
        os.mkdir(tmp_dir_path)

    tmp_path = os.path.join(tmp_dir_path, 'pid.tmp')

    import time
    import json
    content = {'pid': os.getpid(), 'time': time.time(), 'status': status}
    content = json.dumps(content)

    with open(tmp_path, mode) as f:
        f.write(content + '\n')
