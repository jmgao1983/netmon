#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from my_log import logger,link_logger,syslog
from db_fun import xgetone,xgetall
from my_mail import send_mail,send_mail_ext
from my_ftp import ftp_alert
from netmon_env import envi

def my_alert(msg, tdes):

   #1.日志记录到link.log和syslog服务器
   link_logger.warn(msg)

   if envi['slog_server'] != '':
      syslog.error(msg.encode('gbk'))


   #2.发送邮件
   timestr = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
   t_hour = time.localtime().tm_hour
   phone    = []     #获取手机号码列表
   mail_int = []     #获取内部邮箱列表
   mail_ext = []     #获取外部邮箱列表
   detail = ''       #线路详细信息
   re = ()

   #获取该线路的单独告警邮箱和手机号码
   sql = "select mail1,mail2,phone,city,pri from target where tdes='%s'" % tdes
   (m1, m2, p, city, pri) = xgetone(sql)
   if m1 != '' and m1 != None:
      temp = (str(m1).strip(';')).split(';')
      mail_int.extend(temp)
   if m2 != '' and m2 != None:
      temp = (str(m2).strip(';')).split(';')
      mail_ext.extend(temp)
   if p != '' and p != None:
      temp = (str(p).strip(';')).split(';')
      phone.extend(temp)

   #获取用户所在组的告警邮箱和手机号码
   sql="select mail1, mail2, phone from user where city='%s'" % city
   if xgetall(sql) != None:
      mlists = xgetall(sql)
      for mlist in mlists:
         if mlist[0] != '' and mlist[0] != None:
            mail1 = (str(mlist[0]).strip(';')).split(';')
            mail_int.extend(mail1)
         if mlist[1] != '' and mlist[1] != None:
            mail2 = (str(mlist[1]).strip(';')).split(';')
            mail_ext.extend(mail2)
         if mlist[2] != '' and mlist[2] != None:
            tmp_phone = (str(mlist[2]).strip(';')).split(';')
            phone.extend(tmp_phone)
         
   if mail_int != [] or mail_ext != []:
      sql = "select * from detail where tdes='%s'" % tdes
      if xgetone(sql) != None:
         re = xgetone(sql)
         #
         detail = detail + u"线路编号:" + re[1] + "\n"
         detail = detail + u"报障电话:" + re[2] + "\n"
         detail = detail + u"对端联系:" + re[4] + "\n"
         detail = detail + u"对端地址:" + re[3] + "\n"
         detail = detail + u"应用名称:" + re[5] + "\n"
         detail = detail + u"应用联系:" + re[6] + "\n"
         detail = detail + u"线路资费:" + re[7] + "\n"
         detail = detail + u"线路所属:" + re[8] + "\n"
         detail = detail + u"其他信息:" + re[9] + "\n"

   #print mail_int
   #print mail_ext
   #print phone
   if mail_int != []:
      if (pri > 0 or (t_hour>7 and t_hour<24)):
         send_mail(timestr+msg, detail, mail_int)
   if mail_ext != []:
      if (pri > 1 or (t_hour>6 and t_hour<21)):
         send_mail_ext(timestr+msg, detail, mail_ext)

   #print phone
   #3.发送到短信平台
   if envi['ftp_server'] != '' and phone != []:
      if (pri > 1 or (t_hour>6 and t_hour<21)):
         ftp_alert(timestr+msg, phone)

   return
 


if __name__ == '__main__':
   #sql = "select mail1 from user where name='hzjh'"
   #print xgetone(sql)
   my_alert(u'this is a test msg', '工商银行生产')

