#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading, class_login
from db_fun import xgetall
from my_log import logger
from netmon_env import envi

#//支持最大线程数
thread_count = envi['threads']

#//获取router表的所有有效条目数
sql = "select app from router where app>1"
all = len(xgetall(sql))
if all == 0:
   logger.warn('No device for config-saving!')
   exit()

#//新建调用函数
def c_login(ip):
   r = class_login.NetLogin(ip)
   r.test()

start = 0
while start < all:
   sql = "select rip from router where app>1 limit %d, %d" % (start, thread_count)
   ret = xgetall(sql)
   threads = []
   if ret != None:
      for line in ret:
         t = threading.Thread(target=c_login, args=(line[0],))
         threads.append(t)
   
   for t in threads:
      t.setDaemon(True)
      t.start()
   for t in threads:
      t.join()

   start = start + thread_count
