#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import class_monitor
from db_fun import xgetall
from my_log import logger
from netmon_env import envi

#//支持最大线程数
thread_count = envi['threads']

#//获取router表的所有条目数
sql = "select rip from router"
ret = xgetall(sql)
all = len(ret)
if all == 0:
   logger.warn('No router for monitoring!')
   exit()

###//新建调用函数
def rt_mon(ip):
   r = class_monitor.router(ip)
   r.mon()

###//新建多线程进行监控
start = 0
end = thread_count
while start < all:
   #print '----------'
   threads = []
   for line in ret[start:end]:
      t = threading.Thread(target=rt_mon, args=(line[0],))
      threads.append(t)

   for t in threads:
      t.setDaemon(True)
      t.start()
   for t in threads:
      t.join()

   start = start + thread_count
   end = end + thread_count
