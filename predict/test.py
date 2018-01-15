# !/usr/bin/env python
# -*- coding: utf-8 -*-
import master
import config.load as configLoad
import lib.funcUtil as funcUtil

from numpy import *
from multiprocessing import Pool, Queue, Lock, Process
import random
import time
import json
import os

def run(process_id, queue, lock, process_num, unique_id):
    print 'process %d start ...' % process_id

    # kernal = array([1.5])
    # step = int(random.random() * 3) + 2
    # for j in range(step):
    #     kernal = hstack((array([random.random() * 0.41 - 0.2]), kernal))
    #     kernal = hstack((kernal, array([random.random() * 0.41 - 0.2])))
    # kernal = kernal / kernal.sum()

    # config_network = {
    #     'layer_size': [500, 400 + int(random.random() * 201), 1],   # 神经网络的层级结构
    #     'iter_times': 60 + int(random.random() * 100),            # 训练的迭代次数
    #     'lamda': random.random() * 2,                                                 # 正则化的 lamda 参数
    #     'kernal': kernal,               # 数据预处理时 用来 convolve 数据的矩阵
    # }
    #
    # master_config = {
    #     'data': configLoad.config(),
    #     'network': config_network,
    #     'id': unique_id,
    #     'record': False,
    # }
    #
    # o_master = master.Master(master_config)
    # o_master.run()
    #
    # _bpNN = o_master.getNN()
    # run_result = {
    #     'training_record': _bpNN.trainingRecord,
    #     'test_record': _bpNN.testRecord,
    #     'original_data': _bpNN.originalData,
    # }
    #
    # queue.put([master_config, run_result])
    #
    # lock.acquire()
    # try:
    #     funcUtil.recordSparkStatus(unique_id, 'finish ' + str(queue.qsize()) + ' | ' + str(process_num))
    # finally:
    #     lock.release()

    print 'process %d finish' % process_id

def long_time_task(name, process_num, unique_id):
    print 'Run task %s (%s)...' % (name, os.getpid())
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print 'Task %s runs %0.2f seconds.' % (name, (end - start))

if __name__=='__main__':
    unique_id = 'test'

    q = Queue()
    l = Lock()

    print 'Parent process %s.' % os.getpid()
    p = Pool()
    for i in range(5):
        p.apply_async(long_time_task, args=(i, 6, unique_id))
        # p.apply_async(run, args=(i, q, l, 6, unique_id))
    print 'Waiting for all subprocesses done...'
    p.close()
    p.join()
    print 'All subprocesses done.'
