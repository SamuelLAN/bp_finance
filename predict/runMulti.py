# !/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.split(os.path.abspath(os.path.curdir))[0])

import master
import config.load as configLoad
import lib.funcUtil as funcUtil

from numpy import *
from multiprocessing import Pool
import random
import time
import json

def run(process_id, process_num, unique_id):
    print 'process %d start ...' % process_id

    kernal = array([1.5])
    step = int(random.random() * 3) + 2
    for j in range(step):
        kernal = hstack((array([random.random() * 0.41 - 0.2]), kernal))
        kernal = hstack((kernal, array([random.random() * 0.41 - 0.2])))
    kernal = kernal / kernal.sum()

    config_network = {
        'layer_size': [500, 400 + int(random.random() * 201), 1],   # 神经网络的层级结构
        'iter_times': 60 + int(random.random() * 100),            # 训练的迭代次数
        'lamda': random.random() * 2,                                                 # 正则化的 lamda 参数
        'kernal': kernal,               # 数据预处理时 用来 convolve 数据的矩阵
    }

    master_config = {
        'data': configLoad.config(),
        'network': config_network,
        'id': unique_id,
        'record': False,
    }

    o_master = master.Master(master_config)
    o_master.run()

    _bpNN = o_master.getNN()
    run_result = {
        'training_record': _bpNN.trainingRecord,
        'test_record': _bpNN.testRecord,
        'original_data': _bpNN.originalData,
        'pred': _bpNN.pred
    }

    funcUtil.recordSparkStatus(unique_id, str(process_num + 2) + '\n', 'a')
    print 'process %d finish' % process_id
    return [master_config, run_result]

if __name__ == '__main__':
    process_num = 30

    import sys
    # unique_id = sys.argv[1]
    unique_id = 'test'

    s_time = time.time()

    funcUtil.killRunningProcess(unique_id)
    funcUtil.recordPid(unique_id)

    funcUtil.recordStatus(unique_id, 'Start ...')

    p = Pool()

    result_list = []
    for i in range(process_num):
        result_list.append(p.apply_async(run, args=(i, process_num, unique_id)))

    print 'Waiting for all subprocesses done...'
    p.close()
    p.join()
    print 'All subprocesses done.'

    result_list = map(lambda x: x.get(), result_list)

    def compare_accuracy(a, b):
        record_a = a[1]['test_record']
        record_b = b[1]['test_record']

        mean_accuracy_a = (record_a['Test']['accuracy'] + record_a['Validation']['accuracy']) / 2.0
        mean_accuracy_b = (record_b['Test']['accuracy'] + record_b['Validation']['accuracy']) / 2.0

        if mean_accuracy_a >= mean_accuracy_b:
            return a
        else:
            return b

    def compare_diff(a, b):
        record_a = a[1]['test_record']
        record_b = b[1]['test_record']

        mean_diff_a = (record_a['Test']['diff'] + record_a['Validation']['diff']) / 2.0
        mean_diff_b = (record_b['Test']['diff'] + record_b['Validation']['diff']) / 2.0

        if mean_diff_a <= mean_diff_b:
            return a
        else:
            return b

    def compare_cost(a, b):
        record_a = a[1]['test_record']
        record_b = b[1]['test_record']

        mean_cost_a = (record_a['Test']['cost'] + record_a['Validation']['cost']) / 2.0
        mean_cost_b = (record_b['Test']['cost'] + record_b['Validation']['cost']) / 2.0

        if mean_cost_a <= mean_cost_b:
            return a
        else:
            return b

    def compare_validation_accuracy(a, b):
        record_a = a[1]['test_record']
        record_b = b[1]['test_record']

        validation_accuracy_a = record_a['Validation']['accuracy']
        validation_accuracy_b = record_b['Validation']['accuracy']

        if validation_accuracy_a >= validation_accuracy_b:
            return a
        else:
            return b

    def compare_relative_cost(a, b):
        record_a = a[1]['test_record']
        record_b = b[1]['test_record']

        mean_relative_cost_a = (abs(record_a['Test']['relative_cost']) + abs(record_a['Validation']['relative_cost'])) / 2.0
        mean_relative_cost_b = (abs(record_b['Test']['relative_cost']) + abs(record_b['Validation']['relative_cost'])) / 2.0

        if mean_relative_cost_a <= mean_relative_cost_b:
            return a
        else:
            return b

    print 'start reducing ...'

    best_validation_accuracy = reduce(compare_validation_accuracy, result_list)
    print '\n***************** best_validation_accuracy **************************'
    print best_validation_accuracy[0]
    print best_validation_accuracy[1]['test_record']
    print best_validation_accuracy[1]['pred']

    best_accuracy = reduce(compare_accuracy, result_list)
    print '\n***************** best_accuracy **************************'
    print best_accuracy[0]
    print best_accuracy[1]['test_record']
    print best_accuracy[1]['pred']

    best_diff = reduce(compare_diff, result_list)
    print '\n***************** best_diff **************************'
    print best_diff[0]
    print best_diff[1]['test_record']
    print best_diff[1]['pred']

    best_cost = reduce(compare_cost, result_list)
    print '\n***************** best_cost **************************'
    print best_cost[0]
    print best_cost[1]['test_record']
    print best_cost[1]['pred']

    best_relative_cost = reduce(compare_relative_cost, result_list)
    print '\n***************** best_relative_cost **************************'
    print best_relative_cost[0]
    print best_relative_cost[1]['test_record']
    print best_relative_cost[1]['pred']

    def record_result(file_name, data):
        try:
            tmp_path = funcUtil.getTmpPath(unique_id, file_name)
            with open(tmp_path, 'w') as f:
                f.write(json.dumps(data))
        except Exception, ex:
            print ex
            funcUtil.write_log('recordSparkResult')

    record_result('bestAccuracyResult.tmp', best_accuracy[1])
    record_result('bestDiffResult.tmp', best_diff[1])
    record_result('bestCostResult.tmp', best_cost[1])
    record_result('bestValidationAccuracyResult.tmp', best_validation_accuracy[1])
    record_result('bestRelativeCostResult.tmp', best_relative_cost[1])

    funcUtil.recordSparkStatus(unique_id, 'done')
    funcUtil.recordPid(unique_id, 'done')

    e_time = time.time()

    print 'done use time: ' + str(e_time - s_time)
