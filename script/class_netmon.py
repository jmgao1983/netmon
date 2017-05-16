#!/usr/bin/env python
# -*- coding: utf-8 -*-
#'RPing(Remote Ping): auto-login net devices for monitoring WAN lines'

import pexpect, class_login
from db_fun import xgetone, xgetall, mupdate
from my_alert import my_alert
from my_log import logger

###global variables setting
cisco_Fail = 'Success rate is 0 percent'
cisco_Succ = 'min/avg/max = [0-9]([0-9])*'
h3c_Fail = '100.00*% packet loss'
h3c_Succ = 'min/avg/max(\/std-dev)* = [0-9]([0-9])*'

###class definition
class NetMon(class_login.NetLogin):
   def __init__(self, ip):
      class_login.NetLogin.__init__(self, ip)
      self.target = ()
      if self.name != '':
         sql = "select tip,tdes,rtt from target where pri>0 and rname='%s'" % self.name
         self.target = xgetall(sql)


   def mon(self):
      if self.target == ():
         logger.warn(self.ip + ' No target to monitor!')
         return
      #check 'login_mode' describe in 'class_login.py'
      provider = (self.login_mode % 1000) / 10
      if provider == 1:
         self.cisco_ping(self.login())
      elif provider == 2:
         self.h3c_ping(self.login())
      elif provider == 3:
         self.h3c_ping(self.login())
      elif provider == 4:
         self.ruijie_ping(self.login())
      else:
         logger.error(self.ip + ' Error : device with unknown provider!')


   ##cisco_ping
   def cisco_ping(self, obj):
      if obj == None:
         return
      list_tdes = []
      list_rtts = []
      try:
         for line in self.target:
            logger.debug(self.ip + ' ping ' + line[0] + ' rep 2')
            cmd="ping\n\n" + line[0] + "\n2\n\n\n\n\n"
            obj.sendline(cmd)
            rtt = 0
            i=obj.expect([cisco_Succ, cisco_Fail, pexpect.TIMEOUT], timeout=10)
            if i == 2:
               logger.error(self.ip + " Command runs abnormal!")
               obj.close()
               return
            if i == 1:
               if line[2] > 0:
                  msg = self.name+line[1]+':up->down!'
                  my_alert(msg, line[1])
            if i == 0:
               rtt = int(obj.after.split(' ')[2])
               if line[2] == 0:
                  msg = self.name+line[1]+':down->up!'
                  my_alert(msg, line[1])
            list_tdes.append(line[1])
            list_rtts.append(rtt)
         obj.close()
         #批量更新线路延迟数据rtt,减少数据库访问
         mupdate(list_tdes, list_rtts)
      except Exception as e:
         logger.error(self.ip + ' ' + str(e))
         obj.close()
         return
      else:
         logger.info(self.ip + " monitoring finished!")
         return


   ##h3c_ping
   def h3c_ping(self, obj):
      if obj == None:
         return
      list_tdes = []
      list_rtts = []
      try:
         for line in self.target:
            logger.debug(self.ip + ' ping -c 2 ' + line[0])
            obj.sendline('ping -c 2 ' + line[0])
            rtt = 0
            i=obj.expect([h3c_Succ, h3c_Fail, pexpect.TIMEOUT], timeout=10)
            if i == 2:
               logger.error(self.ip + " Command runs abnormal!")
               obj.close()
               return
            if i == 1:
               if line[2] > 0:
                  msg = self.name+line[1]+':up->down!'
                  my_alert(msg, line[1])
            if i == 0:
               print obj.after
               rtt = int(obj.after.split(' ')[2])
               print rtt
               if line[2] == 0:
                  msg = self.name+line[1]+':down->up!'
                  my_alert(msg, line[1])
            list_tdes.append(line[1])
            list_rtts.append(rtt)
         obj.close()
         #批量更新线路延迟数据rtt,减少数据库访问
         mupdate(list_tdes, list_rtts)
      except Exception as e:
         logger.error(self.ip + ' ' + str(e))
         obj.close()
         return
      else:
         logger.info(self.ip + " monitoring finished!")
         return


   ##ruijie_ping
   def ruijie_ping(self, obj):
      if obj == None:
         return
      list_tdes = []
      list_rtts = []
      try:
         for line in self.target:
            logger.debug(self.ip + ' ping ' + line[0] + ' ntimes 2')
            obj.sendline('ping ' + line[0] + ' ntimes 2')
            rtt = 0
            i=obj.expect([cisco_Succ, cisco_Fail, pexpect.TIMEOUT], timeout=10)
            if i == 2:
               logger.error(self.ip + " Command runs abnormal!")
               obj.close()
               return
            if i == 1:
               if line[2] > 0:
                  msg = self.name+line[1]+':up->down!'
                  my_alert(msg, line[1])
            if i == 0:
               rtt = int(obj.after.split(' ')[2])
               if line[2] == 0:
                  msg = self.name+line[1]+':down->up!'
                  my_alert(msg, line[1])
            list_tdes.append(line[1])
            list_rtts.append(rtt)
         obj.close()
         #批量更新线路延迟数据rtt,减少数据库访问
         mupdate(list_tdes, list_rtts)
      except Exception as e:
         logger.error(self.ip + ' ' + str(e))
         obj.close()
         return
      else:
         logger.info(self.ip + " monitoring finished!")
         return


### test code
if __name__ == '__main__':

   NetMon('34.0.30.35').mon()
   NetMon('34.0.30.45').mon()
   NetMon('34.0.223.2').mon()
   NetMon('15.34.254.5').mon()
   NetMon('15.34.81.253').mon()
   NetMon('15.34.177.253').mon()
   NetMon('15.34.49.99').mon()
   NetMon('15.34.21.85').mon()
