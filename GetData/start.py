# !/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.split(os.path.abspath(os.path.curdir))[0])

import GetData.main.dispatch as dispatch
import config.db as db
import config.symbol as symbol
import time

unique_id = sys.argv[1]

db_config = db.config()

config = {
    'start_date': '2008-01-01',
    'end_date': '2014-12-31',
    # 'symbol_list': symbol.get(),
    'symbol_list': ['sz002316'],
    'thread_num_of_download': 150,
    'thread_num_of_handle': 100,
    'limit_date_num': 20,
    'retry_times': 5,
    'save_dir': r'../data',
    'tmp_data_dir': r'../data/tmp',
    'input_nodes': 600,
    'id': unique_id,
    'x_days': 600,
    'y_days': 1,
}

s_time = time.time()

o_manager = dispatch.DispatchManager(config, db_config)
o_manager.run()

e_time = time.time()

print '*********** done ***********'
print 'use time : ' + str(e_time - s_time)
