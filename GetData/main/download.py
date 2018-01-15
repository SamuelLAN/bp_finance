# !/usr/bin/env python
# -*- coding: utf-8 -*-
import GetData.lib.dispatch as base
import GetData.lib.curl as curl
import time

class Download(base.Base):
    def __init__(self, uri, data_queue):
        self.__uri = uri
        self.__dataQueue = data_queue
        self.init()

    def __save(self, data):
        self.__dataQueue.put(data)

    def run(self):
        o_curl = curl.Curl(self.__uri)

        s_time = time.time()
        data = o_curl.get()
        e_time = time.time()
        self.useTime = e_time - s_time

        if o_curl.getErrorQueue():
            self.mergeErrorQueue(o_curl.getErrorQueue())
        else:
            self.__save({self.__uri: data})
