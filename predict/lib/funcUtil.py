# !/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import random

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

# 生成随机索引序列
def getShuffleList(num):
    _list = range(num)
    random.shuffle(_list)
    return _list

# 获取 从 start 开始 end 结束，步长为 step 的离散序列
def getContinuousList(_list, start, end, step):
    while start >= end and step < 0 or start <= end and step > 0:
        _list.append(start)
        start += step
    return _list

# 根据 list_b 作为索引，取出 list_a 中对应的数据，生成新的list
def getListFromList(list_a, list_b):
    return [list_a[i] for i in list_b]

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

def recordSparkStatus(module_name, content, mode='w'):
    tmp_path = getTmpPath(module_name, 'sparkStatus.tmp')

    with open(tmp_path, mode) as f:
        f.write(content)

def killRunningProcess(module_name):
    tmp_dir_path = os.path.join(os.path.abspath(os.path.curdir), 'tmp')
    if not tmp_dir_path:
        return

    tmp_dir_path = os.path.join(tmp_dir_path, module_name)
    if not tmp_dir_path:
        return

    import json

    try:
        tmp_path = os.path.join(tmp_dir_path, 'pid.tmp')
        with open(tmp_path, 'r') as f:
            content = f.read()
            content = content.split('\n')
            for line in content:
                if not line:
                    continue
                line = json.loads(line)
                if line['status'] == 'running':
                    os.kill(int(line['pid']), 9)
    except Exception, ex:
        print 'kill process fail'
        write_log('killRunningProcess')

    try:
        for file_name in os.listdir(tmp_dir_path):
            tmp_file_path = os.path.join(tmp_dir_path, file_name)
            os.remove(tmp_file_path)
        os.rmdir(tmp_dir_path)
    except Exception, ex:
        print 'remove file or dir fail'
        write_log('killRunningProcess')

def clearStatus(module_name):
    tmp_dir_path = os.path.join(os.path.abspath(os.path.curdir), 'tmp')
    if not tmp_dir_path:
        return

    tmp_dir_path = os.path.join(tmp_dir_path, module_name)
    if not tmp_dir_path:
        return

    try:
        for file_name in os.listdir(tmp_dir_path):
            tmp_file_path = os.path.join(tmp_dir_path, file_name)
            os.remove(tmp_file_path)
        os.rmdir(tmp_dir_path)
    except Exception, ex:
        print ex
        write_log('clearStatus')

def readStatus(module_name, file_name):
    tmp_dir_path = os.path.join(os.path.abspath(os.path.curdir), 'tmp')
    if not tmp_dir_path:
        return

    tmp_dir_path = os.path.join(tmp_dir_path, module_name)
    if not tmp_dir_path:
        return

    tmp_path = os.path.join(tmp_dir_path, file_name)

    if not os.path.exists(tmp_path):
        return

    with open(tmp_path, 'r') as f:
        return f.read()
