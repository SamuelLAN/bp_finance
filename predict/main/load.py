# !/usr/bin/env python
# -*- coding: utf-8 -*-
import predict.lib.baseObject as baseObject
from numpy import *
import random

'''
    加载数据模块
'''
class Load(baseObject.base):
    def __init__(self, config):
        self.__XPathList = config['X_path_list']
        self.__yPathList = config['y_path_list']

        self.__XTestPathList = config['X_test_path_list']
        self.__yTestPthList = config['y_test_path_list']

        self.__trainingPercent = config['training_percent']

    '''
        运行接口
    '''
    def run(self):
        data = self.__load(self.__XPathList, self.__yPathList)
        data, tmp_end = self.__popLast(data)

        data_test = self.__load(self.__XTestPathList, self.__yTestPthList)
        data_test, data_last = self.__popLast(data_test)

        data_training, data_val = self.__split(data, self.__trainingPercent)

        return data_training, data_val, data_test, data_last

    '''
        划分 训练集 和 校验集 (根据 training_percent 的比例 进行划分)
    '''
    @staticmethod
    def __split(data, training_percent):
        X, y = data

        m, n = X.shape
        m_training = int(m * training_percent)

        rand_indices = range(m)             # 生成随机索引序列
        random.shuffle(rand_indices)

        X_training = array([X[i] for i in rand_indices[0: m_training]])         # 根据 划分比例 和 随机索引序列 进行数据划分
        y_training = array([y[i] for i in rand_indices[0: m_training]])

        X_val = array([X[i] for i in rand_indices[m_training:]])
        y_val = array([y[i] for i in rand_indices[m_training:]])

        return (X_training, y_training), (X_val, y_val)

    @staticmethod
    def __popLast(data):
        X, y = data
        return (X[0:-1, :], y[0:-1, :]), (X[-1:, :], y[-1:, :])

    '''
        从文件中读取数据 （没对数据进行预处理）
    '''
    @staticmethod
    def __load(x_path_list, y_path_list):
        X_defined = False
        y_defined = False
        X = None
        y = None

        for x_path in x_path_list:
            with open(x_path, 'r') as f:
                content = f.read()
                if not X_defined:
                    X_defined = True
                    X = array([[float(x) for x in line.split(' ')] for line in content.split('\n') if line])
                else:
                    X = vstack((X, array([[float(x) for x in line.split(' ')] for line in content.split('\n') if line])))

        for y_path in y_path_list:
            with open(y_path, 'r') as f:
                content = f.read()
                if not y_defined:
                    y_defined = True
                    y = array([[float(x) for x in line.split(' ')] for line in content.split('\n') if line])
                else:
                    y = vstack((y, array([[float(x) for x in line.split(' ')] for line in content.split('\n') if line])))

        return X, y
