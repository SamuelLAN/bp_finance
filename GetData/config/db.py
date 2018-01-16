# !/usr/bin/env python
# -*- coding: utf-8 -*-

# 数据库配置
def config():
    return {
        'user': 'root',
        'password': '',
        'host': '127.0.0.1',
        'port': 3306,
        'connection_timeout': 1,
        'database': 'finance',
        'use_unicode': True
    }
