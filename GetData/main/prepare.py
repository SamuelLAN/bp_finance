# !/usr/bin/env python
# -*- coding: utf-8 -*-
import GetData.lib.funcUtil as funcUtil
import GetData.lib.sql as sql
import GetData.lib.baseObject as baseObject
import Queue

class Prepare(baseObject.base):
    def __init__(self, config, db_config):
        self.__dateStart = config['start_date']
        self.__dateEnd = config['end_date']
        self.__symbolList = config['symbol_list']

        self.__sql = sql.Sql(**db_config)

        self.__uriQueue = Queue.Queue()
        self.__dataQueue = Queue.Queue()

    def run(self):
        try:
            self.__getUriQueue()
        except Exception, ex:
            print ex
            funcUtil.write_log('Prepare')
        return self.__uriQueue, self.__dataQueue, self.__symbolList

    def __getUriQueue(self):
        date_queue = funcUtil.get_date_list(self.__dateStart, self.__dateEnd)

        if not self.__symbolList:
            self.__symbolList = self.__getAllSymbol()
        self.__sql.close()

        for symbol in self.__symbolList:
            for date in date_queue:
                uri = self.getApi(date, symbol)
                self.__uriQueue.put(uri)

    def __getAllSymbol(self):
        symbol_queue = []
        query = 'select id from code'
        for _id in self.__sql.query(query):
            symbol_queue.append(_id[0])
        return symbol_queue

    @staticmethod
    def getApi(date, symbol):
        return 'http://market.finance.sina.com.cn/downxls.php?date=%s&symbol=%s' % (date, symbol)
