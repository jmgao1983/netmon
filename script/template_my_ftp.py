#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time,os
from ftplib import FTP
from my_log import logger
from netmon_env import envi

ftp_server = envi['ftp_server']
ftp_port   = envi['ftp_port']
ftp_usr    = envi['ftp_usr']
ftp_pwd    = envi['ftp_pwd']
ftp_dir    = envi['ftp_dir']

def ftp_alert(msg, phone):
   #新建临时文件
   fpath = r'/var/www/html/netmon/log'
   os.chdir(fpath)

   timestr = time.strftime('%H%M%S',time.localtime())
   fname = '220000000_000000000000_' + timestr + '_NETMON.txt'
   text = ''
   #print type(msg)
   #将中文编码转换成ftp服务器上的编码
   msg = msg.encode('gbk')
   for num in phone:
      text  = text + '|' + num + '||' + msg + "|0|\n"

   #print type(text)
   try:
      file = open(fname, 'w')
      file.writelines(text)
      file.close()
   except Exception as e:
      logger.error(str(e))
      file.close()
      return False
   else:
      logger.debug('temp file [' + fname + '] created')

   #临时文件上传ftp服务器
   try:
      ftp = FTP()
      ftp.set_debuglevel(1)
      ftp.connect(ftp_server, ftp_port)
      ftp.login(ftp_usr, ftp_pwd)
      logger.debug(" Ftp Server Logged in!")
      ftp.cwd(ftp_dir)
      ftp.storlines('STOR '+fname, open(fname, 'r'))
      ftp.set_debuglevel(0)
      ftp.close()
   except Exception as e:
      logger.error(str(e))
      ftp.close()
      return False
   else:
      logger.info(" file uploaded to FTP server!")

   #清理临时文件
   os.remove(fname)
   return True

### test code
if __name__ == '__main__':

   phone = ['13135469461','15237372838']
   ftp_alert(u'2016-04-08 08:22:12JL_ECN_RT_1移动代收:down->up!', phone)
