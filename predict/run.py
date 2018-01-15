# !/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.split(os.path.abspath(os.path.curdir))[0])

import master
import config.network as configNetwork
import config.load as configLoad
import lib.funcUtil as funcUtil

# unique_id = sys.argv[1]
unique_id = 'test'

funcUtil.killRunningProcess(unique_id)
funcUtil.recordPid(unique_id)

config = {
    'data': configLoad.config(),                        # 读取 加载数据的配置
    'network': configNetwork.config(),                  # 读取 神经网络的配置
    'id': unique_id,
    'record': True,
}

o_master = master.Master(config)
o_master.run()

funcUtil.recordStatus(unique_id, 'done')
funcUtil.recordPid(unique_id, 'done')

import time
print 'done ' + str(time.time())
