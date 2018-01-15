# !/usr/bin/env python
# -*- coding: utf-8 -*-

import time

for i in range(20):
    print i
    with open(r'1.txt', 'w') as f:
        f.write(str(i))
    time.sleep(1)
