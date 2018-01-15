# !/usr/bin/env python
# -*- coding: utf-8 -*-
import GetData.lib.baseObject as baseObject
import GetData.lib.funcUtil as funcUtil
from numpy import *
import os
import json

'''
延长了预测的天数
'''
class Save(baseObject.base):
    def __init__(self, config, com):
        self.__inputNodes = config['input_nodes']
        self.__dateStart = config['start_date']
        self.__dateEnd = config['end_date']
        self.__saveDir = config['save_dir']
        self.__tmpDataDir = config['tmp_data_dir']
        self.__xDays = config['x_days']
        self.__yDays = config['y_days']
        self.__id = config['id']
        self.__fileName = self.__dateStart + '_' + self.__dateEnd + '_' + str(self.__inputNodes) + '_' + self.__id

        self.__domain = []
        self.__com = com

    def run(self):
        try:
            self.__process()
        except Exception, ex:
            print ex
            funcUtil.write_log('save')

    @staticmethod
    def sortByDate(a, b):
        if a[0] > b[0]:
            return 1
        elif a[0] == b[0]:
            return 0
        else:
            return -1

    def __process(self):
        self.__calculateDomain()

        for file_name in os.listdir(self.__tmpDataDir):
            symbol = file_name.split('_')[0]
            if file_name[len(symbol) + 1:] != self.__fileName:
                continue

            funcUtil.recordStatus(self.__id, 'sampling %s data ...' % file_name)
            print 'sampling %s data ...' % file_name

            try:
                tmp_path = os.path.join(self.__tmpDataDir, file_name)
                with open(tmp_path, 'r') as f:
                    content = f.read()
                    content = content.split('\n')
                    for line in content:
                        if not line:
                            continue
                        self.__com[symbol] += json.loads(line)

                os.remove(tmp_path)
            except Exception, ex:
                print ex
                funcUtil.write_log('getDataProcess')

            self.__com[symbol].sort(Save.sortByDate)

            symbol_data = []
            data_list = self.__com[symbol]
            data_len = len(data_list)
            for index, value in enumerate(data_list[0: -max(self.__xDays, self.__yDays)]):
                tmp_x = value[1]
                for i in range(self.__xDays - 1):
                    tmp_x += data_list[index + i + 1][1]
                x = self.__sample(tmp_x)

                # x = self.__sample(value[1])
                funcUtil.recordStatus(self.__id, 'has sample %d | %d' % (index + 1, data_len))
                print 'has sample %d | %d' % (index + 1, data_len)

                next_data_start = data_list[index + self.__yDays]
                next_data_end = data_list[index + self.__yDays + self.__xDays - 1]
                y = (next_data_start[1][0][1], next_data_end[1][-1][1])

                symbol_data.append((x, y))

            tmp_x = data_list[-self.__xDays][1]
            for i in range(self.__xDays - 1):
                tmp_x += data_list[-self.__xDays + i + 1][1]
            x_end = self.__sample(tmp_x)
            y_end = (0, 0)
            symbol_data.append((x_end, y_end))

            funcUtil.recordStatus(self.__id, 'finish sample %s' % file_name)
            print 'finish sample %s' % file_name

            funcUtil.recordStatus(self.__id, 'start save %s data' % file_name)
            print 'start save %s data' % file_name

            self.__save(symbol, symbol_data)

            funcUtil.recordStatus(self.__id, 'finish saving %s' % file_name)
            print 'finish saving %s' % file_name

            del self.__com[symbol]

        for symbol, data in self.__com.iteritems():
            self.__com[symbol].sort(Save.sortByDate)

            funcUtil.recordStatus(self.__id, 'sampling %s data ...' % symbol)
            print 'sampling %s data ...' % symbol

            symbol_data = []
            data_list = self.__com[symbol]
            data_len = len(data_list)
            for index, value in enumerate(data_list[0: -1]):
                tmp_x = value[1]
                for i in range(self.__xDays - 1):
                    tmp_x += data_list[index + i + 1][1]
                x = self.__sample(tmp_x)

                # x = self.__sample(value[1])
                funcUtil.recordStatus(self.__id, 'has sample %d | %d' % (index + 1, data_len))
                print 'has sample %d | %d' % (index + 1, data_len)

                next_data_start = data_list[index + self.__yDays]
                next_data_end = data_list[index + self.__yDays + self.__xDays - 1]
                y = (next_data_start[1][0][1], next_data_end[1][-1][1])

                symbol_data.append((x, y))

            tmp_x = data_list[-self.__xDays][1]
            for i in range(self.__xDays - 1):
                tmp_x += data_list[-self.__xDays + i + 1][1]
            x_end = self.__sample(tmp_x)
            y_end = (0, 0)
            symbol_data.append((x_end, y_end))

            funcUtil.recordStatus(self.__id, 'finish sample %s' % symbol)
            print 'finish sample %s' % symbol

            funcUtil.recordStatus(self.__id, 'start save %s data' % symbol)
            print 'start save %s data' % symbol

            self.__save(symbol, symbol_data)

            funcUtil.recordStatus(self.__id, 'finish saving %s' % symbol)
            print 'finish saving %s' % symbol

    def __calculateDomain(self):
        delta = int(14760 / self.__inputNodes)
        self.__domain = [i * delta for i in range(self.__inputNodes)]
        self.__domain.append(14760)

    def __sample(self, data):
        sample = []
        for i in self.__domain[0: -1]:
            sample.append((0, 0))

        for i, tmp_data in enumerate(data):
            for index, value in enumerate(self.__domain[0: -1]):
                if value <= tmp_data[0] <= self.__domain[index + 1]:
                    sample[index] = (sample[index][0] + tmp_data[1], sample[index][1] + 1)

        latest_record = 0
        for index, value in enumerate(sample):
            if value[1] > 0:
                latest_record = value[0] / value[1]
                break

        for index, value in enumerate(sample):
            if value[1] > 0:
                sample[index] = value[0] / value[1]
                latest_record = sample[index]
            else:
                sample[index] = latest_record

        return sample

    def __save(self, symbol, data):
        file_name = str(symbol) + '_' + self.__fileName + '.mat'
        x_file_name = 'X_' + file_name
        y_file_name = 'y_' + file_name

        file_path = os.path.join(self.__saveDir, x_file_name)
        with open(file_path, 'w') as f:
            f.write('')
        with open(file_path, 'a') as f:
            for tmp_data in data:
                x_str = ''
                x_list = tmp_data[0]
                for x in x_list[0: -1]:
                    x_str += str(x) + ' '
                x_str += str(x_list[-1])
                f.write(x_str + '\n')

        file_path = os.path.join(self.__saveDir, y_file_name)
        with open(file_path, 'w') as f:
            f.write('')
        with open(file_path, 'a') as f:
            for tmp_data in data:
                y_str = str(tmp_data[1][0]) + ' ' + str(tmp_data[1][1])
                f.write(y_str + '\n')
