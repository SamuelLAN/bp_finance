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
import time

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

if __name__ == '__main__':
    print 'start main process ...\n'
    s_time = time.time()

    unique_id = sys.argv[1]
    symbol = sys.argv[2]
    # unique_id = 'test'
    # symbol = 'sz002316'
    # save_module = 'save4'
    save_module = 'save'

    funcUtil.killRunningProcess(unique_id)
    funcUtil.recordPid(unique_id)

    funcUtil.recordStatus(unique_id, 'Start ...')

    training_start_date = '2008-01-01'
    training_end_date = '2015-12-31'

    test_start_date = '2016-01-01'
    test_end_date = time.strftime('%Y-%m-%d', time.localtime())
    # test_end_date = '2016-05-16'

    input_node_num = 600
    output_node_num = 100

    cur_path = os.path.abspath(os.path.split(__file__)[0])
    save_dir = os.path.join(cur_path, r'data')

    X_training_file_path = os.path.join(save_dir, 'X_' + symbol + '_' + training_start_date + '_' + training_end_date + '_' + str(input_node_num) + '_' + str(unique_id) + '.mat')
    y_training_file_path = os.path.join(save_dir, 'y_' + symbol + '_' + training_start_date + '_' + training_end_date + '_' + str(input_node_num) + '_' + str(unique_id) + '.mat')

    X_test_file_path = os.path.join(save_dir, 'X_' + symbol + '_' + test_start_date + '_' + test_end_date + '_' + str(input_node_num) + '_' + str(unique_id) + '.mat')
    y_test_file_path = os.path.join(save_dir, 'y_' + symbol + '_' + test_start_date + '_' + test_end_date + '_' + str(input_node_num) + '_' + str(unique_id) + '.mat')

    training_percent = 0.8

    run_process_num = 10

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
        'output_nodes': output_node_num,
        'save_module': 'save4',
        'id': unique_id,
        'x_days': input_node_num,
        'y_days': 5,
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
        'output_nodes': output_node_num,
        'save_module': 'save4',
        'id': unique_id,
        'x_days': input_node_num,
        'y_days': 5,
    }

    config_load_data = {
        'X_path_list': [X_training_file_path],
        'y_path_list': [y_training_file_path],
        'X_test_path_list': [X_test_file_path],
        'y_test_path_list': [y_test_file_path],
        'training_percent': training_percent,    # 训练集 占 (训练集，校验集) 的比例
    }

    p = Pool()
    p.apply_async(get_data, args = (1, config_training, db_config, unique_id))
    p.apply_async(get_data, args = (2, config_test, db_config, unique_id))

    print 'waiting for all get_data subprocess done ...'

    p.close()
    p.join()

    print '\n all get_data subprocess done'

    config_predict = {
        'input_num': input_node_num,
        'hidden_base': int(input_node_num * 0.8),
        'hidden_range': int(input_node_num * 4),
        'iter_time_base': 80,
        'iter_time_range': 50,
    }

    kernal = array([1.5])
    step = int(random.random() * 3) + 2
    for j in range(step):
        kernal = hstack((array([random.random() * 0.41 - 0.2]), kernal))
        kernal = hstack((kernal, array([random.random() * 0.41 - 0.2])))
    kernal = kernal / kernal.sum()

    config_network = {
        'layer_size': [config_predict['input_num'], config_predict['hidden_base'] + int(random.random() * config_predict['hidden_range']), output_node_num],   # 神经网络的层级结构
        'iter_times': config_predict['iter_time_base'] + int(random.random() * config_predict['iter_time_range']),            # 训练的迭代次数
        'lamda': random.random() * 2,                                                 # 正则化的 lamda 参数
        'kernal': kernal,               # 数据预处理时 用来 convolve 数据的矩阵
    }

    config_p = {
        'data': config_load_data,                        # 读取 加载数据的配置
        'network': config_network,                  # 读取 神经网络的配置
        'id': unique_id,
        'record': True,
    }

    o_master = master.Master(config_p)
    o_master.run()

    funcUtil.recordStatus(unique_id, 'done')
    funcUtil.recordPid(unique_id, 'done')

    # try:
    #     os.remove(X_training_file_path)
    #     os.remove(y_training_file_path)
    #     os.remove(X_test_file_path)
    #     os.remove(y_test_file_path)
    # except Exception, ex:
    #     print ex
    #     funcUtil.write_log('deleteTmp')

    e_time = time.time()

    print '\n******************** done **************************'
    print 'use time: %s' % str(e_time - s_time)
