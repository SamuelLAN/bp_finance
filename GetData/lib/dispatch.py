# !/usr/bin/env python
# -*- coding: utf-8 -*-
import baseObject
import funcUtil
import threading
import re

class BaseManager(baseObject.base):
    STATUS_INIT = 0
    STATUS_RUNNING = 1
    STATUS_END = 2

    def init(self):
        self.moduleName = re.split('\.', str(self.__class__))[-1][:-len('Manager') - 2]
        self.pool = {}                      # 线程池
        self.status = {}                    # 线程状态
        self.threadNums = {}
        self.setThread(self.defaultThread)

    # fork 线程，线程进入 ready 状态
    def fork(self, group=None, target=None, name=None,args=(), kwargs=None, verbose=None):
        self.status[name] = self.STATUS_INIT
        self.pool[name] = threading.Thread(group, target, name, args, kwargs, verbose)

    def forkAll(self, pre_name, thread_num, record_id=None):
        self.threadNums[pre_name] = thread_num
        for x in range(0, thread_num):
            thread_id = pre_name + '(' + str(x) + ')'
            if record_id:
                funcUtil.recordStatus(record_id, ' %s fork thread: %s' % (self.moduleName, thread_id))
            print ' %s fork thread: %s' % (self.moduleName, thread_id)
            self.fork(target=self.runThread, name=thread_id, args=(thread_id,))
            self.start(thread_id)

    # 将 线程池里的线程 设置为运行状态
    def start(self, name):
        if name in self.pool:
            self.status[name] = self.STATUS_RUNNING
            self.pool[name].start()

    # 等待所有线程结束
    def join_all(self):
        for t in self.pool.itervalues():
            t.join()
        del self.pool
        del self.status

    def defaultThread(self, thread_id):
        pass

    def setThread(self, func):
        self.thread = func

    def runThread(self, *args):
        try:
            self.thread(*args)
        except Exception, ex:
            print ex
            funcUtil.write_log(self.moduleName)

    def run(self):
        self.dispatch()

    def dispatch(self):
        pass

class Base(baseObject.base):
    STATUS_INIT = 0
    STATUS_RUNNING = 1
    STATUS_END = 2

    def init(self):
        self.moduleName = re.split('\.', str(self.__class__))[1]
        self.usedTime = 0

    def getUsedTime(self):
        return self.usedTime

    def setThreadId(self, thread_id):
        self.threadId = thread_id

    def flush(self):
        funcUtil.flush_thread_status(self.moduleName, self.threadId)
