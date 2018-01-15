# !/usr/bin/env python
# -*- coding: utf-8 -*-
import GetData.config.error as error

'''
框架和插件里的所有class，都必须继承该基类 (里面封装了一系列设置错误信息的方法)
'''
class base(object):
    # 初始化错误号、错误队列
    def __initError(self):
        setattr(self, '__error', True)
        setattr(self, '__errorQueue', [])
        self.__error = {'no': 0, 'msg': ''}
        self.__errorQueue = []

    # 设置错误号，错误信息
    #   错误信息会自动带上捕捉到的错误的具体信息，以及错误号对应的错误信息；若不需要额外添加其他错误信息，无需写err_msg
    def setError(self, err_no, err_msg=''):
        self.setErrorNo(err_no, err_msg)
        self.__errorQueue.append({
            'no': err_no,
            'msg': self.__error['msg'],
        })

    # 只设置错误号，不将错误信息保存到错误队列
    def setErrorNo(self, err_no, err_msg=''):
        if not hasattr(self, '__errorQueue'):
            self.__initError()

        if err_no == 0:
            return

        import sys
        info = sys.exc_info()

        self.__error['no'] = err_no
        self.__error['msg'] = error.getInfo(err_no) + '; ' + str(info[0]) + ': ' + str(info[1])
        if err_msg:
            if self.__error['msg']:
                self.__error['msg'] += ' '
            self.__error['msg'] += err_msg

    # 合并错误队列
    def mergeErrorQueue(self, queue):
        if not hasattr(self, '__errorQueue'):
            self.__initError()
        self.__errorQueue += queue

    # 获取最近一次错误的错误对象 {'no': xxx, 'msg': xxx}
    def getError(self):
        if not hasattr(self, '__errorQueue'):
            self.__initError()
        return self.__error

    # 获取错误队列
    def getErrorQueue(self):
        if not hasattr(self, '__errorQueue'):
            self.__initError()
        return self.__errorQueue

    # 获取最近一次错误的错误号
    def getErrorNo(self):
        if not hasattr(self, '__errorQueue'):
            self.__initError()
        return self.__error['no']

    # 重置最近一次的错误，但不重置 errorQueue
    def resetErrorNo(self):
        if not hasattr(self, '__errorQueue'):
            self.__initError()
        self.__error = {'no': 0, 'msg': ''}

    # 判断最近是否有出错
    def hasError(self):
        if not hasattr(self, '__errorQueue'):
            return False
        if self.__error['no'] == 0:
            return False
        return True
