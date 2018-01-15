# !/usr/bin/env python
# -*- coding: utf-8 -*-
import predict.lib.baseObject as baseObject
from numpy import *
import math
import random

class Theta(baseObject.base):
    def __init__(self, layer_size):
        self.__layerSize = layer_size
        self.__initThetas()

    '''
        初始化 theta_list
    '''
    def __initThetas(self):
        self.__thetaList = []
        for index, value in enumerate(self.__layerSize[0:-1]):
            self.__thetaList.append(self.randInitTheta(value, self.__layerSize[index + 1]))

    def setTheta(self, theta_list):
        self.__thetaList = theta_list

    def getTheta(self):
        return self.__thetaList

    '''
        theta_list 的 相减，用于 训练时的权值更新
    '''
    def minusGrad(self, grad, learning_rate):
        new_thetas_list = []
        for index, theta in enumerate(self.__thetaList):
            new_thetas_list.append(theta - learning_rate * grad[index])
        return new_thetas_list

    '''
        随机初始化单个 theta
    '''
    @staticmethod
    def randInitTheta(num_in, num_out):
        epsilon = math.pow(6.0 / (num_in + num_out), 0.5)
        return array([[random.random() * 2 * epsilon - epsilon for j in range(num_in + 1)] for i in range(num_out)])
