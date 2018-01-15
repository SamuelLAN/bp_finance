# !/usr/bin/env python
# -*- coding: utf-8 -*-

# 错误号定义
SQL_NOT_START = -100
SQL_CONNECT = -101
SQL_QUERY = -102
SQL_EXECUTE_PROGRAMMING = -103
SQL_EXECUTE_INTEGRITY = -104

FILE_OPEN = -200
DIR_NOT_EXIST = -201

CURL = -300

MAIL_SERVER = -500
MAIL_SENDER = -501
MAIL_SOCKET = -502
MAIL_AUTHEN = -503
MAIL_RECEIVER = -504

# 错误信息
INFO = {
    '-100': 'Error: Mysql hasn\'t started',
    '-101': 'Error: Connect failed, access denied for user',
    '-102': 'Error: Query failed',
    '-103': 'Error: Execute programming error',
    '-104': 'Error: Execute integrity error',
    '-200': 'Error: Open file fail',
    '-201': 'Error: Dir path doesn\'t exist',
    '-300': 'Error: Curl error',
    '-500': 'Error: Mail server error',
    '-501': 'Error: Mail sender error',
    '-502': 'Error: Mail socket error, connection fail',
    '-503': 'Error: Mail authentication error',
    '-504': 'Error: Mail receiver error',
}

# 根据错误号 获取 错误信息
def getInfo(err_no):
    if str(err_no) in INFO:
        return INFO[str(err_no)]
    return ''
