# !/usr/bin/env python
# -*- coding: utf-8 -*-
import GetData.lib.baseObject as baseObject
import GetData.lib.funcUtil as funcUtil
import GetData.lib.sql as sql

class SaveFail(baseObject.base):
    def __init__(self, db_config, uri):
        self.__sql = sql.Sql(**db_config)
        self.__uri = uri

    def run(self):
        try:
            self.__save()
        except Exception, ex:
            print ex
            funcUtil.write_log('saveFail')

    def __save(self, uri):
        query = u'select * from `finance`.`fail_uri` where uri = %s'
        param = (uri,)
        if self.__sql.query(query, param):
            return

        stmt = u'insert into `finance`.`fail_uri`(`uri`) values(%s)'
        self.__sql.execute(stmt, param)
