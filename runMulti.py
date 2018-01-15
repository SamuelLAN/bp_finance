# !/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.split(os.path.abspath(os.path.curdir))[0])
sys.path.append(os.path.abspath(os.path.curdir))

import GetData.main.dispatch as dispatch
import GetData.config.db as db
import predict.lib.funcUtil as funcUtil
import predict.master as master

from multiprocessing import Pool
from numpy import *
import random
import time
import json

def get_data(process_id, config, db_config, unique_id):
    print 'GetData(%d) start ...' % process_id
    funcUtil.recordPid(unique_id, 'running', 'a')

    try:
        o_manager = dispatch.DispatchManager(config, db_config)
        o_manager.run()
    except Exception, ex:
        print ex
        funcUtil.write_log('GetData')

    print 'GetData(%d) finish' % process_id

def run(process_id, config_run, process_num, unique_id):
    print 'predict(%d) start ...' % process_id

    kernal = array([1.5])
    step = int(random.random() * 3) + 2
    for j in range(step):
        kernal = hstack((array([random.random() * 0.41 - 0.2]), kernal))
        kernal = hstack((kernal, array([random.random() * 0.41 - 0.2])))
    kernal = kernal / kernal.sum()

    config_network = {
        'layer_size': [config_run['input_num'], config_run['hidden_base'] + int(random.random() * config_run['hidden_range']), 1],   # 神经网络的层级结构
        'iter_times': config_run['iter_time_base'] + int(random.random() * config_run['iter_time_range']),            # 训练的迭代次数
        'lamda': random.random() * 2,                                                 # 正则化的 lamda 参数
        'kernal': kernal,               # 数据预处理时 用来 convolve 数据的矩阵
    }

    master_config = {
        'data': config_run['load'],
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
        'pred': _bpNN.pred,
    }

    funcUtil.recordSparkStatus(unique_id, str(process_num + 2) + '\n', 'a')
    print 'predict(%d) finish' % process_id
    return [master_config, run_result]

if __name__ == '__main__':
    print 'start main process ...\n'
    s_time = time.time()

    unique_id = sys.argv[1]
    symbol = sys.argv[2]

    save_module = 'save'

    funcUtil.killRunningProcess(unique_id)
    funcUtil.recordPid(unique_id)

    funcUtil.recordStatus(unique_id, 'Start ...')

    input_node_num = 600

    training_start_date = '2008-01-01'
    training_end_date = '2014-12-31'

    test_start_date = '2015-01-01'
    # test_end_date = time.strftime('%Y-%m-%d', time.localtime())
    test_end_date = '2016-05-16'

    save_dir = r'data'

    X_training_file_path = os.path.join(save_dir, 'X_' + symbol + '_' + training_start_date + '_' + training_end_date + '_' + str(input_node_num) + '_' + str(unique_id) + '.mat')
    y_training_file_path = os.path.join(save_dir, 'y_' + symbol + '_' + training_start_date + '_' + training_end_date + '_' + str(input_node_num) + '_' + str(unique_id) + '.mat')

    X_test_file_path = os.path.join(save_dir, 'X_' + symbol + '_' + test_start_date + '_' + test_end_date + '_' + str(input_node_num) + '_' + str(unique_id) + '.mat')
    y_test_file_path = os.path.join(save_dir, 'y_' + symbol + '_' + test_start_date + '_' + test_end_date + '_' + str(input_node_num) + '_' + str(unique_id) + '.mat')

    training_percent = 0.8

    run_process_num = 50

    db_config = db.config()

    config_training = {
        'start_date': training_start_date,
        'end_date': training_end_date,
        'symbol_list': [symbol],
        'thread_num_of_download': 150,
        'thread_num_of_handle': 100,
        'limit_date_num': 20,
        'retry_times': 5,
        'save_dir': save_dir,
        'tmp_data_dir': os.path.join(save_dir, 'tmp'),
        'input_nodes': input_node_num,
        'save_module': save_module,
        'id': unique_id,
        'x_days': input_node_num,
        'y_days': 1,
    }

    config_test = {
        'start_date': test_start_date,
        'end_date': test_end_date,
        'symbol_list': [symbol],
        'thread_num_of_download': 150,
        'thread_num_of_handle': 100,
        'limit_date_num': 20,
        'retry_times': 5,
        'save_dir': save_dir,
        'tmp_data_dir': os.path.join(save_dir, 'tmp'),
        'input_nodes': input_node_num,
        'save_module': save_module,
        'id': unique_id,
        'x_days': input_node_num,
        'y_days': 1,
    }

    config_load_data = {
        'X_path_list': [X_training_file_path],
        'y_path_list': [y_training_file_path],
        'X_test_path_list': [X_test_file_path],
        'y_test_path_list': [y_test_file_path],
        'training_percent': training_percent,    # 训练集 占 (训练集，校验集) 的比例
    }

    config_predict = {
        'load': config_load_data,
        'input_num': input_node_num,
        'hidden_base': int(input_node_num * 0.8),
        'hidden_range': int(input_node_num * 0.4),
        'iter_time_base': 50,
        'iter_time_range': 100,
    }

    p = Pool()
    p.apply_async(get_data, args = (1, config_training, db_config, unique_id))  # 开启多进程爬取数据 （爬训练集、校验集）
    p.apply_async(get_data, args = (2, config_test, db_config, unique_id))      # 爬测试集数据

    print 'waiting for all get_data subprocess done ...'

    p.close()
    p.join()

    print '\n all get_data subprocess done'

    p2 = Pool()

    result_list = []
    for i in range(run_process_num):        # 查看进程运行完返回的结果
        result_list.append(p2.apply_async(run, args=(i, config_predict, run_process_num, unique_id)))

    print 'Waiting for all predict subprocess done ...'

    p2.close()
    p2.join()

    print '\nAll predict subprocess done'

    result_list = map(lambda x: x.get(), result_list)

    '''
        根据 accuracy 指标进行对比，保留最优
    '''
    def compare_accuracy(a, b):
        record_a = a[1]['test_record']
        record_b = b[1]['test_record']

        mean_accuracy_a = (record_a['Test']['accuracy'] + record_a['Validation']['accuracy']) / 2.0
        mean_accuracy_b = (record_b['Test']['accuracy'] + record_b['Validation']['accuracy']) / 2.0

        if mean_accuracy_a >= mean_accuracy_b:
            return a
        else:
            return b

    '''
        根据 diff 指标进行对比，保留最优
    '''
    def compare_diff(a, b):
        record_a = a[1]['test_record']
        record_b = b[1]['test_record']

        mean_diff_a = (record_a['Test']['diff'] + record_a['Validation']['diff']) / 2.0
        mean_diff_b = (record_b['Test']['diff'] + record_b['Validation']['diff']) / 2.0

        if mean_diff_a <= mean_diff_b:
            return a
        else:
            return b

    '''
        根据 cost 指标进行对比，保留最优
    '''
    def compare_cost(a, b):
        record_a = a[1]['test_record']
        record_b = b[1]['test_record']

        mean_cost_a = (record_a['Test']['cost'] + record_a['Validation']['cost']) / 2.0
        mean_cost_b = (record_b['Test']['cost'] + record_b['Validation']['cost']) / 2.0

        if mean_cost_a <= mean_cost_b:
            return a
        else:
            return b

    '''
        根据 validation_accuracy 指标进行对比，保留最优
    '''
    def compare_validation_accuracy(a, b):
        record_a = a[1]['test_record']
        record_b = b[1]['test_record']

        validation_accuracy_a = record_a['Validation']['accuracy']
        validation_accuracy_b = record_b['Validation']['accuracy']

        if validation_accuracy_a >= validation_accuracy_b:
            return a
        else:
            return b

    '''
        根据 relative cost 指标进行对比，保留最优
    '''
    def compare_relative_cost(a, b):
        record_a = a[1]['test_record']
        record_b = b[1]['test_record']

        mean_relative_cost_a = (abs(record_a['Test']['relative_cost']) + abs(record_a['Validation']['relative_cost'])) / 2.0
        mean_relative_cost_b = (abs(record_b['Test']['relative_cost']) + abs(record_b['Validation']['relative_cost'])) / 2.0

        if mean_relative_cost_a <= mean_relative_cost_b:
            return a
        else:
            return b

    print '\nstart reducing ...'

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

    '''
        记录最优的结果
    '''
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

    try:                                            # 删除临时文件
        os.remove(X_training_file_path)
        os.remove(y_training_file_path)
        os.remove(X_test_file_path)
        os.remove(y_test_file_path)
    except Exception, ex:
        print ex
        funcUtil.write_log('deleteTmp')

    e_time = time.time()

    print '\n******************** done **************************'
    print 'use time: %s' % str(e_time - s_time)
