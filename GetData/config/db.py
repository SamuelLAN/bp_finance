# !/usr/bin/env python
# -*- coding: utf-8 -*-

# 数据库配置
def config():
    return {
        'user': 'root',
        'password': '',
        'host': 'localhost',
        'port': 3306,
        'connection_timeout': 1,
        'database': 'finance',
        'use_unicode': True
    }
