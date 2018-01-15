# !/usr/bin/env python
# -*- coding: utf-8 -*-
import GetData.config.symbol as symbolConfig
import GetData.lib.sql as sql

def update(db_config):
    support_symbol_list = symbolConfig.get()

    o_sql = sql.Sql(**db_config)

    for symbol in support_symbol_list:
        query = u'select * from `finance`.`support` where symbol = %s'
        param = (symbol,)
        if o_sql.query(query, param):
            continue

        stmt = u'insert into `finance`.`support`(`symbol`) values(%s)'
        o_sql.execute(stmt, param)


