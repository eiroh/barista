#!/usr/bin/env python
# -*- coding:utf-8 -*-

import redis
rc = redis.Redis(host='localhost', port=6379, db=0)
for key in rc.keys():
    print key
