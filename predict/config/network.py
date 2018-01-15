# !/usr/bin/env python
# -*- coding: utf-8 -*-
import random
from numpy import *

def config():
    try:
        from scipy import optimize
        iter_times = 110            # 若能使用 共轭梯度下降，只需迭代 100 次左右
    except Exception, ex:
        iter_times = 2500           # 否则，若需要全局下降，需要迭代 2500 次左右，共轭梯度下降 比 全局梯度下降 和 随机梯度下降 都收敛得快

    return {
        'layer_size': [500, 400 + int(random.random() * 201), 1],   # 神经网络的层级结构
        'iter_times': iter_times,                                   # 训练的迭代次数
        'lamda': 0,                                                 # 正则化的 lamda 参数
        'kernal': array([0, 0, 0, 1, 0, 0, 0]),               # 数据预处理时 用来 convolve 数据的矩阵
    }

# kernal = [0.1, 0.15, 0.5, 0.15, 0.1]
# kernal = [-1, -1, -1, 7, -1, -1, -1]
# kernal = [-2, -2, -2, 10, -1, -1, -1]
