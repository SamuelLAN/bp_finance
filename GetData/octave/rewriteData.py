# !/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import os

def normalize(data):
    mean = 0.0
    for value in data:
        mean += value
    mean /= len(data)

    std = 0.0
    for value in data:
        std += math.pow(value - mean, 2)
    std = math.pow(std / len(data), 0.5)
    if std == 0:
        std = 1.0

    for index, value in enumerate(data):
        data[index] = (value - mean) / std
    return data, mean, std

def conv(data, kernal):
    step = (len(kernal) - 1) / 2
    data_len = len(data)
    result = []
    for i, v in enumerate(data):
        tmp = 0.0
        for j, vj in enumerate(kernal):
            if i - step + j < 0:
                tmp_v = data[0]
                # tmp_v = 0
            elif i - step + j > data_len - 1:
                # tmp_v = 0
                tmp_v = data[-1]
            else:
                tmp_v = data[i - step + j]
            tmp += tmp_v * vj
        result.append(tmp)
    return result

file_name_list = ['sz002316_2015-01-01_2016-05-03_500', 'sz002396_2015-01-01_2016-05-03_500',
                  'sz300051_2015-01-01_2016-05-03_500', 'sz300379_2015-01-01_2016-05-03_500']

for file_name in file_name_list:
    last_name = '.mat'
    save_file_name = file_name + last_name

    with open(os.path.join(r'F:\spark\data', file_name), 'r') as f:
        content = f.read()

    with open(os.path.join(r'F:\spark\data\octave', 'X_' + save_file_name), 'w') as f:
        f.write('')

    with open(os.path.join(r'F:\spark\data\octave', 'y_' + save_file_name), 'w') as f:
        f.write('')

    # with open(os.path.join(r'F:\spark\data\octave', 'normalize_' + save_file_name), 'w') as f:
    #     f.write('')

    # pre_name = 'special_'
    # with open(os.path.join(r'F:\spark\data\octave', pre_name + 'X_' + save_file_name), 'w') as f:
    #     f.write('')
    #
    # with open(os.path.join(r'F:\spark\data\octave', pre_name + 'y_' + save_file_name), 'w') as f:
    #     f.write('')
    #
    # with open(os.path.join(r'F:\spark\data\octave', pre_name + 'normalize_' + save_file_name), 'w') as f:
    #     f.write('')

    content = content.split('******\n')[1:]

    for i, v in enumerate(content):
        data = v.split('\n')
        x = data[0]
        y = data[1]

        x = [float(v_x) for v_x in x.split(' ')]
        # x = [(v_x - x[0]) / x[0] for v_x in x]
        #
        # kernal = [-1, -1, -1, 7, -1, -1, -1]
        # x = conv(x, kernal)
        #
        # x, x_mean, x_std = normalize(x)
        # kernal = [0.1, 0.12, 0.13, 0.3, 0.13, 0.12, 0.1]
        # x = conv(x, kernal)

        y = [float(v_y) for v_y in y.split(' ')]
        # y = (y[1] - y[0]) / y[0]
        #
        # special_point = 0.05
        # if math.fabs(y) >= special_point:
        #     _pre_name = pre_name
        # else:
        #     _pre_name = ''
        #
        # y = (y - x_mean) / x_std

        with open(os.path.join(r'F:\spark\data\octave', 'X_' + save_file_name), 'a') as f:
            x = reduce((lambda a, b: str(a) + ' ' + str(b)), x)
            f.write(x + '\n')

        with open(os.path.join(r'F:\spark\data\octave', 'y_' + save_file_name), 'a') as f:
            f.write(str(y[0]) + ' ' + str(y[1]) + '\n')

        # with open(os.path.join(r'F:\spark\data\octave', _pre_name + 'normalize_' + save_file_name), 'a') as f:
        #     f.write(str(x_mean) + ' ' + str(x_std) + '\n')

import time
print 'done ' + str(time.time())
