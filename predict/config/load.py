# !/usr/bin/env python
# -*- coding: utf-8 -*-

def config():
    return {
        # 训练集、校验集的数据存储路径
        'X_path_list': [r'F:\GraduateProject\data\octave\2008-01-01_2014-12-31_500\X_sz002316_2008-01-01_2014-12-31_500.mat'],
        'y_path_list': [r'F:\GraduateProject\data\octave\2008-01-01_2014-12-31_500\y_sz002316_2008-01-01_2014-12-31_500.mat'],
        # 测试集的数据存储路径
        'X_test_path_list': [r'F:\GraduateProject\data\octave\2015-01-01_2016-05-03_500\X_sz002316_2015-01-01_2016-05-03_500.mat'],
        'y_test_path_list': [r'F:\GraduateProject\data\octave\2015-01-01_2016-05-03_500\y_sz002316_2015-01-01_2016-05-03_500.mat'],
        'training_percent': 0.8,    # 训练集 占 (训练集，校验集) 的比例
    }
