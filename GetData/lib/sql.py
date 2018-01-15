# !/usr/bin/env python
# -*- coding: utf-8 -*-
import GetData.config.error as error
import mysql.connector
import baseObject
import funcUtil

class Sql(baseObject.base):
    __rowCount = -1                     # 影响的行数

    def __init__(self, **db_config):
        self.__config = db_config
        self.__connect()

    # 连接数据库; times 为失败后重试次数
    def __connect(self, times = 3):
        if times > 0:
            if hasattr(self, '__moduleName'):
                module_name = self.__moduleName
            else:
                module_name = 'sql'

            try:
                self.__conn = mysql.connector.connect(**self.__config)
            except mysql.connector.errors.ProgrammingError:
                self.setError(error.SQL_CONNECT)
                funcUtil.write_log(module_name)
                self.__connect(times - 1)
            except mysql.connector.errors.InterfaceError:
                self.setError(error.SQL_NOT_START)
                funcUtil.write_log(module_name)
                self.__connect(times - 1)
            except:
                self.setError(error.SQL_CONNECT)
                funcUtil.write_log(module_name)
                self.__connect(times - 1)

    def query(self, stmt, param=None, record_error=True):
        _values = []
        if self.getErrorQueue():
            return _values
        self.resetErrorNo()

        try:
            _cursor = self.__conn.cursor()
            _cursor.execute(stmt, param)
            _values = _cursor.fetchall()
            self.__rowCount = _cursor.rowcount
            _cursor.close()
        except Exception, ex:
            if not record_error:
                self.setErrorNo(error.SQL_QUERY, u'stmt: %s' % stmt)
                return

            self.setError(error.SQL_QUERY, u'stmt: %s' % stmt)

            if hasattr(self, '__moduleName'):
                module_name = self.__moduleName
            else:
                module_name = 'sql'

                # print '*********************'
                # print ex
                # print stmt
                # print param
                # # print isinstance(param, list)
                # # for _x in param:
                # #     print '#####'
                # #     for xx in _x:
                # #         print str(type(xx)) + '  ' + str(xx)
                # #     print '!!!!!'
                # print '&&&&&&&&&&&&&&&&&&&&&&'
            funcUtil.write_log(module_name, u'stmt: %s' % stmt)

        return _values

    # 设置项目名，方便记录错误日志到具体项目
    def setModuleName(self, module_name):
        self.__moduleName = module_name

    def execute(self, stmt, param=None, multi=False, record_error=True):
        if self.getErrorQueue():
            return
        self.resetErrorNo()

        try:
            _cursor = self.__conn.cursor()
            if isinstance(param, list):
                _cursor.executemany(stmt, param)
            else:
                _cursor.execute(stmt, param, multi)
            self.__rowCount = _cursor.rowcount
            self.__conn.commit()
            _cursor.close()
        except Exception, ex:
            if not record_error:
                self.setErrorNo(error.SQL_EXECUTE_PROGRAMMING, u'stmt: %s' % stmt)
                return

            self.setError(error.SQL_EXECUTE_PROGRAMMING, u'stmt: %s' % stmt)

            if hasattr(self, '__moduleName'):
                module_name = self.__moduleName
            else:
                module_name = 'sql'

                if 'syntax' in str(ex):
                    print '*********************'
                    print ex
                    print stmt
                    print param
                # print isinstance(param, list)
                # for _x in param:
                #     print '#####'
                #     for xx in _x:
                #         print str(type(xx)) + '  ' + str(xx)
                #     print '!!!!!'
                # print '&&&&&&&&&&&&&&&&&&&&&&'
            funcUtil.write_log(module_name, u'stmt: %s' % stmt)

    # 关闭数据库连接
    def close(self):
        if hasattr(self, '__conn') and self.__conn:
            self.__conn.close()

    # 返回影响的行数
    def getRowCount(self):
        return self.__rowCount

    @staticmethod
    def filter(_input):
        if isinstance(_input, str):
            _input = _input.decode('utf-8')
        import re
        special_chars = re.compile(';"\' ')
        return re.sub(special_chars, '', _input)
