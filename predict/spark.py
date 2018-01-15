# !/usr/bin/env python
# -*- coding: utf-8 -*-
from scipy import optimize
from numpy import *

import sys

import master
import config.network as configNetwork
import config.load as configLoad
import lib.funcUtil as funcUtil

from pyspark import SparkConf, SparkContext

import random
import time
import sys
import json

unique_id = sys.argv[1]
funcUtil.killRunningProcess(unique_id)
funcUtil.recordPid(unique_id)

funcUtil.recordStatus(unique_id, 'Start ...')

conf = SparkConf().setMaster('local[2]').setAppName('Finance_Predict(%s)' % str(unique_id))
sc = SparkContext(conf = conf)

config = {
    'data': configLoad.config(),                        # 读取 加载数据的配置
    'network': configNetwork.config(),                  # 读取 神经网络的配置
    'id': unique_id,
    'record': False,
}

process_num = 30

Config = [config]
for i in range(process_num):
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

    Config.append({
        'data': config['data'],
        'network': config_network,
        'id': unique_id,
        'record': False,
    })

s_time = time.time()

Config_sc = sc.parallelize(Config)

def run(_config):
    o_master = master.Master(_config)
    o_master.run()

    funcUtil.recordSparkStatus(unique_id, str(process_num + 2) + '\n', 'a')
    return [_config]
    # return [_config, o_master.getTestRecord(), o_master.getNN()]

result = Config_sc.map(run)
result.persist()

print result.count()

def compare_accuracy(a, b):
    record_a = a[1]
    record_b = b[1]

    mean_accuracy_a = (record_a['Test']['accuracy'] + record_a['Validation']['accuracy']) / 2.0
    mean_accuracy_b = (record_b['Test']['accuracy'] + record_b['Validation']['accuracy']) / 2.0

    if mean_accuracy_a >= mean_accuracy_b:
        return a
    else:
        return b

def compare_diff(a, b):
    record_a = a[1]
    record_b = b[1]

    mean_diff_a = (record_a['Test']['diff'] + record_a['Validation']['diff']) / 2.0
    mean_diff_b = (record_b['Test']['diff'] + record_b['Validation']['diff']) / 2.0

    if mean_diff_a <= mean_diff_b:
        return a
    else:
        return b

def compare_cost(a, b):
    record_a = a[1]
    record_b = b[1]

    mean_cost_a = (record_a['Test']['cost'] + record_a['Validation']['cost']) / 2.0
    mean_cost_b = (record_b['Test']['cost'] + record_b['Validation']['cost']) / 2.0

    if mean_cost_a <= mean_cost_b:
        return a
    else:
        return b

def compare_validation_accuracy(a, b):
    record_a = a[1]
    record_b = b[1]

    validation_accuracy_a = record_a['Validation']['accuracy']
    validation_accuracy_b = record_b['Validation']['accuracy']

    if validation_accuracy_a >= validation_accuracy_b:
        return a
    else:
        return b

# best_validation_accuracy = result.reduce(compare_validation_accuracy)
# print '\n***************** best_validation_accuracy **************************'
# print best_validation_accuracy
#
# best_accuracy = result.reduce(compare_accuracy)
# print '\n****************** best_accuracy *************************'
# print best_accuracy
#
# best_diff = result.reduce(compare_diff)
# print '\n****************** best_diff *************************'
# print best_diff
#
# best_cost = result.reduce(compare_cost)
# print '\n****************** best_cost *************************'
# print best_cost
#
# def record_result(file_name, bpNN):
#     try:
#         tmp_path = funcUtil.getTmpPath(unique_id, file_name)
#         with open(tmp_path, 'w') as f:
#             best_result = {
#                 'training_record': bpNN.trainingRecord,
#                 'test_record': bpNN.testRecord,
#                 'original_data': bpNN.originalData,
#             }
#             best_result = json.dumps(best_result)
#             f.write(best_result)
#     except Exception, ex:
#         print ex
#         funcUtil.write_log('recordSparkResult')
#
# record_result('bestAccuracyResult.tmp', best_accuracy[2])
# record_result('bestDiffResult.tmp', best_diff[2])
# record_result('bestCostResult.tmp', best_cost[2])
# record_result('bestValidationAccuracyResult.tmp', best_validation_accuracy[2])

funcUtil.recordSparkStatus(unique_id, 'done', 'a')
funcUtil.recordPid(unique_id, 'done')

e_time = time.time()

print 'done use time: ' + str(e_time - s_time)
