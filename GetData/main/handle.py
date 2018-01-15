# !/usr/bin/env python
# -*- coding: utf-8 -*-
import GetData.lib.dispatch as base
import GetData.lib.funcUtil as funcUtil
import time
import re
import json
import os

class Handle(base.Base):
    def __init__(self, config, data, com, com_lock):
        self.__data = data

        self.__uri = None
        self.__com = com
        self.__comLock = com_lock
        self.__limitDateNum = config['limit_date_num']
        self.__tmpDataDir = config['tmp_data_dir']
        self.__inputNum = config['input_nodes']
        self.__id = config['id']
        self.__fileName = config['start_date'] + '_' + config['end_date'] + '_' + str(self.__inputNum) + '_' + self.__id

        self.init()

    '''
        对数据回来的数据进行处理
    '''
    def __process(self, data):
        for uri, _data in data.iteritems():
            self.__uri = uri
            matches = re.match(r'[\w\.:/]*\?date=([^&]*)&symbol=(\w*)', uri)
            date = matches.group(1)
            symbol = matches.group(2)
            param = []

            if '\xb5\xb1\xcc\xec\xc3\xbb\xd3\xd0\xca\xfd\xbe\xdd' in _data:     # 若抓取回来的数据为空
                return {
                    'date': date,
                    'symbol': symbol,
                    'param': param,
                }

            tmp_tuple = time.strptime(date + ' 13:00:00', '%Y-%m-%d %H:%M:%S')
            noon_time = time.mktime(tmp_tuple)

            tmp_tuple = time.strptime(date + ' 9:30:00', '%Y-%m-%d %H:%M:%S')
            morning_time = time.mktime(tmp_tuple)

            _data = _data.decode('GB2312')
            lines = _data.split("\n")

            if len(lines) < 100:
                return {
                    'date': date,
                    'symbol': symbol,
                    'param': param,
                }

            if not lines[-1]:
                start_data = lines[-2]
            else:
                start_data = lines[-1]
            matches = re.split('\s+', start_data)
            tmp_tuple = time.strptime(date + ' ' + matches[0], '%Y-%m-%d %H:%M:%S')
            start_time = time.mktime(tmp_tuple)
            if start_time > morning_time:
                start_time = morning_time

            for _line in lines[1:]:
                if not _line:
                    continue

                matches = re.split('\s+', _line)
                tmp_tuple = time.strptime(date + ' ' + matches[0], '%Y-%m-%d %H:%M:%S')
                deal_time = time.mktime(tmp_tuple)
                if deal_time >= noon_time:
                    deal_time -= 5400
                deal_time -= start_time
                deal_price = float(matches[1])
                # price_change = matches[2]                         # 由于目前只用到价格序列作为特征，所以以下信息暂不存储，节省空间
                # if price_change == '--':
                #     price_change = float(0.0)
                # else:
                #     price_change = float(price_change)
                # volume = int(matches[3])
                # turnover = int(float(matches[4]))
                # deal_type = matches[5]
                # if deal_type == u'卖盘':
                #     deal_type = -1
                # elif deal_type == u'买盘':
                #     deal_type = 1
                # else:
                #     deal_type = 0

                # param.append((deal_time, deal_price, price_change, volume, turnover, deal_type))
                param.insert(0, (deal_time, deal_price))

            return {
                'date': date,
                'symbol': symbol,
                'param': param,
            }

    def __save(self, data):
        deal_data = data['param']
        symbol = data['symbol']

        if not len(deal_data) > 100:
            return

        self.__comLock[symbol].acquire()
        try:
            self.__com[symbol].append((data['date'], deal_data))
            if len(self.__com[symbol]) > self.__limitDateNum:
                tmp_data = json.dumps(self.__com[symbol])
                with open(os.path.join(self.__tmpDataDir, symbol + '_' + self.__fileName), 'a') as f:
                    f.write(tmp_data + '\n')
                del self.__com[symbol]
                self.__com[symbol] = []
        finally:
            self.__comLock[symbol].release()

    def getUri(self):
        return self.__uri

    '''
        外部调用该模块的接口
    '''
    def run(self):
        s_time = time.time()

        try:
            data = self.__process(self.__data)
            self.__save(data)
        except Exception, ex:
            print ex
            funcUtil.write_log(self.moduleName)

        e_time = time.time()
        self.usedTime = e_time - s_time
