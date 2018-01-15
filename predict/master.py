# !/usr/bin/env python
# -*- coding: utf-8 -*-
import lib.baseObject as baseObject
import lib.funcUtil as funcUtil
import main.BPNN as NN
# import main.BPNN2 as NN
# import main.BPNN_sigmoid as NN
import main.load as load

import time
import json

class Master(baseObject.base):
    def __init__(self, config):
        try:
            self.__dataConfig = config['data']
            self.__nnConfig = config['network']
            self.__id = config['id']
            self.__record = config['record']

            self.__nnConfig['id'] = self.__id
            self.__bpNN = NN.BPNN(self.__nnConfig)                      #　初始化神经网络
            self.__success = True
        except Exception, ex:
            print ex
            funcUtil.write_log('config')
            self.__success = False

    def run(self):
        self.__load()

        self.__preProcess()

        self.__train()

        self.__test()

        self.__predict()

        self.__recordResult()

        self.__plot()

    def success(self):
        return self.__success

    def getNN(self):
        return self.__bpNN

    def getTestRecord(self):
        return self.__bpNN.testRecord

    def __load(self):
        print 'loading data ...'
        funcUtil.recordStatus(self.__id, 'loading data ...')
        load_s_time = time.time()

        try:
            o_load = load.Load(self.__dataConfig)                       # 加载数据 并 进行数据预处理
            data_training, data_val, data_test, data_last = o_load.run()
            self.__bpNN.loadData(data_training, data_val, data_test, data_last)
        except Exception, ex:
            print ex
            funcUtil.write_log('load')
            self.__success = False

        load_e_time = time.time()
        print 'finish loading'
        print 'load data use time: %s\n' % str(load_e_time - load_s_time)
        funcUtil.recordStatus(self.__id, 'finish loading (use time: %s)' % str(load_e_time - load_s_time))

    def __preProcess(self):
        print 'pre processing data ...'
        funcUtil.recordStatus(self.__id, 'pre processing data ...')
        process_s_time = time.time()

        try:
            self.__bpNN.preProcess()
        except Exception, ex:
            print ex
            funcUtil.write_log('preProcess')
            self.__success = False

        process_e_time = time.time()
        print 'finish pre processing'
        print 'pre processing data use time: %s\n' % str(process_e_time - process_s_time)
        funcUtil.recordStatus(self.__id, 'finish pre processing (use time: %s)' % str(process_e_time - process_s_time))

    def __train(self):
        print 'training neural network ...'
        funcUtil.recordStatus(self.__id, 'training neural network ...')
        train_s_time = time.time()

        try:
            self.__bpNN.train()
        except Exception, ex:
            print ex
            funcUtil.write_log('train')
            self.__success = False

        train_e_time = time.time()
        print 'finish training'
        print 'train neural network use time: %s\n' % str(train_e_time - train_s_time)
        funcUtil.recordStatus(self.__id, 'finish training neural network (use time: %s)' % str(train_e_time - train_s_time))

    def __test(self):
        print 'testing neural network ...'
        funcUtil.recordStatus(self.__id, 'testing neural network ...')
        test_s_time = time.time()

        try:
            self.__bpNN.test()
        except Exception, ex:
            print ex
            funcUtil.write_log('test')
            self.__success = False

        test_e_time = time.time()
        print 'finish testing'
        print 'test neural network use time: %s\n' % str(test_e_time - test_s_time)
        funcUtil.recordStatus(self.__id, 'finish testing (use time: %s)' % str(test_e_time - test_s_time))

    def __predict(self):
        print 'predicting future data ...'
        predict_s_time = time.time()

        try:
            self.__bpNN.predictFuture()
        except Exception, ex:
            print ex
            funcUtil.write_log('predictFuture')
            self.__success = False

        predict_e_time = time.time()
        print 'finish predicting future data'
        print 'predict future data use time: %s\n' % str(predict_e_time - predict_s_time)
        funcUtil.recordStatus(self.__id, 'finish predicting future data (use time: %s)' % str(predict_e_time - predict_s_time))

    def __plot(self):
        try:
            self.__bpNN.plot()
        except Exception, ex:
            print ex
            funcUtil.write_log('plot')
            self.__success = False

    def __recordResult(self):
        if not self.__record:
            return

        print 'recording result ...'
        funcUtil.recordStatus(self.__id, 'recording result ...')
        record_s_time = time.time()

        try:
            result = {
                'training_record': self.__bpNN.trainingRecord,
                'test_record': self.__bpNN.testRecord,
                'original_data': self.__bpNN.originalData,
                'pred': self.__bpNN.pred,
            }
            result = json.dumps(result)

            with open(funcUtil.getTmpPath(self.__id, 'result.tmp'), 'w') as f:
                f.write(result)
        except Exception, ex:
            print ex
            funcUtil.write_log('recordResult')

        record_e_time = time.time()
        print 'finish recording'
        print 'record result use time: %s\n' % str(record_e_time - record_s_time)
        funcUtil.recordStatus(self.__id, 'finish recording (use time: %s)' % str(record_e_time - record_s_time))
