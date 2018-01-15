import sys, os
sys.path.append(os.path.split(os.path.abspath(os.path.curdir))[0])

import predict.lib.funcUtil as funcUtil

unique_id = sys.argv[1]

funcUtil.killRunningProcess(unique_id)

print 'done'
