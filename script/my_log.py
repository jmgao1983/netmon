#!/usr/bin/env python
# -*- coding: utf-8 -*-
#CRITICAL=50> ERROR=40> WARNING=30> INFO=20> DEBUG=10> NOTSET=0

import logging
from logging.handlers import RotatingFileHandler, SMTPHandler, SysLogHandler
from netmon_env import envi

#------------logging for python-script
logger = logging.getLogger('netmon')
logger.setLevel(envi['log_lvl'])
File1 = '/var/www/html/netmon/log/netmon.log'
FM = '%(asctime)s %(filename)s %(lineno)d %(levelname)s %(message)s'
DF = '%Y-%m-%d %H:%M:%S'
#定义RotatingFileHandler，最多备份3个日志文件，每个日志文件2M
RH = RotatingFileHandler(File1, 'a', 2*1024*1024, 3)
RH.setLevel(logging.DEBUG)
RH.setFormatter(logging.Formatter(FM,DF))
logger.addHandler(RH)
#定义StreamHandler，输出到屏幕
SH = logging.StreamHandler()
SH.setLevel(logging.DEBUG)
SH.setFormatter(logging.Formatter(FM,DF))
logger.addHandler(SH)

#------------logging for link status
link_logger = logging.getLogger('link-status-local')
link_logger.setLevel(logging.DEBUG)
File2 = '/var/www/html/netmon/log/link.log'
FM = '%(asctime)s %(message)s'
RH = RotatingFileHandler(File2, 'a', 2*1024*1024, 3)
RH.setLevel(logging.DEBUG)
RH.setFormatter(logging.Formatter(FM,DF))
link_logger.addHandler(RH)
#
#定义SysLogHandler
syslog = logging.getLogger('link-status-syslog')
#slogH = SysLogHandler('/dev/log', 1)
slogH = SysLogHandler((envi['slog_server'],514))
slogH.setLevel(logging.DEBUG)
slogH.setFormatter(logging.Formatter(FM,DF))
syslog.addHandler(slogH)


if __name__ == '__main__':
   #link_logger.error('ZJ_ECN_R1 测试线路DX up->down')
   #link_logger.warn('ZJ_ECN_R2 测试线路 down->up')
   msg = 'ZJ_ECN_R2 测试线路 down->up'
   msg = msg.decode("UTF-8").encode('gbk')
   syslog.error(msg)
