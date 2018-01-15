# !/usr/bin/env python
# -*- coding: utf-8 -*-
import GetData.lib.dispatch as base
import GetData.lib.funcUtil as funcUtil
import prepare
import download
import handle
# import save
# import save4 as save
# import saveFail
import support
import threading
import Queue
import os
import time

class DispatchManager(base.BaseManager):
    def __init__(self, config, db_config):
        self.__threadNumOfDownload = config['thread_num_of_download']
        self.__threadNumOfHandle = config['thread_num_of_handle']
        self.__retryTimes = config['retry_times']
        self.__tmpDataDir = config['tmp_data_dir']
        self.__saveModule = config['save_module']
        self.__id = config['id']
        self.__fileName = config['start_date'] + '_' + config['end_date'] + '_' + str(config['input_nodes']) + '_' + self.__id

        self.__config = config
        self.__dbConfig = db_config

        self.__uriLock = threading.Lock()
        self.__dataLock = threading.Lock()
        self.__fileLock = threading.Lock()

        self.__downloadThreadLock = threading.Lock()

        self.__failQueue = Queue.Queue()
        self.__failUriDict = {}

        self.__com = {}

        self.init()
        self.o_prepare = prepare.Prepare(self.__config, self.__dbConfig)

        self.__curlTime = 0
        self.__curlCounts = 0

        self.__handleTime = 0
        self.__handleCount = 0

    def __prepare(self):
        funcUtil.recordStatus(self.__id, 'preparing dispatch manager ...')

        self.__uriQueue, self.__dataQueue, self.__symbolList = self.o_prepare.run()

        self.__comLock = {}
        for symbol in self.__symbolList:
            if symbol not in self.__com:
                self.__com[symbol] = []
                self.__comLock[symbol] = threading.Lock()

            try:
                tmp_path = os.path.join(self.__tmpDataDir, symbol + '_' + self.__fileName)
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
            except Exception, ex:
                print ex
                funcUtil.write_log('deleteTmp')

        funcUtil.recordStatus(self.__id, 'finish preparing dispatch manager ...')

    def __getUri(self):
        uri = None
        self.__uriLock.acquire()
        try:
            if not self.__uriQueue.empty():
                uri = self.__uriQueue.get()
        finally:
            self.__uriLock.release()
        return uri

    def __getData(self):
        data = None
        self.__dataLock.acquire()
        try:
            if not self.__dataQueue.empty():
                data = self.__dataQueue.get()
        finally:
            self.__dataLock.release()
        return data

    def __addFailUri(self, uri, error_queue):
        if not error_queue:
            return
        if uri in self.__failUriDict and self.__failUriDict[uri] > self.__retryTimes:
            self.mergeErrorQueue(error_queue)
            self.__failQueue.put(uri)
        else:
            if uri not in self.__failUriDict:
                self.__failUriDict[uri] = 1
            else:
                self.__failUriDict[uri] += 1
            self.__uriQueue.put(uri)

    def dispatch(self):
        self.__prepare()

        self.setThread(self.download)
        self.forkAll('download', self.__threadNumOfDownload, self.__id)

        self.setThread(self.handle)
        self.forkAll('handle', self.__threadNumOfHandle, self.__id)

        self.join_all()
        print '\n *************** download and handle have finished *****************\n'

        self.save()
        print '\n *************** save have finished *****************\n'

        # self.saveFail()
        # print '\n *************** saveFail have finished *****************\n'

        # support.update(self.__dbConfig)
        # print '\n *************** update support sql have finished *****************\n'

    def download(self, thread_id):
        try:
            uri = self.__getUri()
            while uri:
                o_download = download.Download(uri, self.__dataQueue)
                o_download.setThreadId(thread_id)
                o_download.run()

                self.__curlTime += o_download.getUsedTime()
                self.__curlCounts += 1
                funcUtil.recordStatus(self.__id, '%s  uri: %s  use time: %.2f  size: %d' % (thread_id, uri, o_download.getUsedTime(), self.__uriQueue.qsize()))
                print thread_id + '    uri: ' + uri + '   use time: ' + str(o_download.getUsedTime()) + '  size: ' + str(self.__uriQueue.qsize())

                self.__addFailUri(uri, o_download.getErrorQueue())

                uri = self.__getUri()
        except Exception, ex:
            print ex
        finally:
            self.status[thread_id] = self.STATUS_END
            self.__downloadThreadLock.acquire()
            try:
                self.threadNums['download'] -= 1
            finally:
                self.__downloadThreadLock.release()

    def handle(self, thread_id):
        most_wait = 10
        while self.threadNums['download'] or not self.__dataQueue.empty():
            data = self.__getData()
            if not data:
                if self.threadNums['download'] <= 1 and self.__dataQueue.empty():
                    if most_wait <= 0:
                        break
                    most_wait -= 1
                    time.sleep(1)
                continue

            o_handle = handle.Handle(self.__config, data, self.__com, self.__comLock)
            o_handle.setThreadId(thread_id)
            o_handle.run()

            self.__handleTime += o_handle.getUsedTime()
            self.__handleCount += 1
            funcUtil.recordStatus(self.__id, '%s  uri: %s  use time: %.2f  size: %d' % (thread_id, str(o_handle.getUri()), o_handle.getUsedTime(), self.__dataQueue.qsize()))
            # print thread_id + '    uri: ' + str(o_handle.getUri()) + '   use time: ' + str(o_handle.getUsedTime()) + '  size: ' + str(self.__dataQueue.qsize())

        self.status[thread_id] = self.STATUS_END
        self.threadNums['handle'] -= 1

    def save(self):
        save = __import__(self.__saveModule)
        o_save = save.Save(self.__config, self.__com)
        o_save.run()

    def saveFail(self):
        while not self.__failQueue.empty():
            uri = self.__failQueue.get()
            o_save_fail = saveFail.SaveFail(self.__dbConfig, uri)
            o_save_fail.run()
