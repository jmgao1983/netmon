#!/usr/bin/env python
# -*- coding: utf-8 -*-
#'RPing(Remote Ping): auto-login net devices for monitoring WAN lines'

import pexpect, class_login
from db_fun import xgetone, xgetall, mupdate
from my_alert import my_alert
from my_log import logger
from NetworkDevice import device_netmon

# RTT_MAX
RTT_MAX=9999

###class definition
class NetMon(class_login.NetLogin):
   def __init__(self, ip):
      class_login.NetLogin.__init__(self, ip)
      self.target = ()
      if self.name != '':
         sql = "select tip,tdes,rtt from target where rname='%s'" % self.name
         self.target = xgetall(sql)


   def mon(self):
      if self.target == ():
         logger.warn(self.ip + ' No target to monitor!')
         return

      if device_netmon.get(self.corp) == None:
         logger.error(self.ip + ' Error : unsupported device to monitor!')
         return

      obj = self.login()
      if obj == None:
         logger.error(self.ip + ' Error : monitor failed due to login error!')
         return

      success = device_netmon.get(self.corp).get('succ')
      fail = device_netmon.get(self.corp).get('fail')
      pingCmd = device_netmon.get(self.corp).get('ping')

      list_tdes = []
      list_rtts = []
      try:
         for line in self.target:
            cmd = pingCmd %line[0]
            logger.debug(self.ip + ' ' + cmd)
            obj.sendline(cmd)
            rtt = 0
            i=obj.expect([success, fail, pexpect.TIMEOUT], timeout=10)
            if i == 2:
               logger.error(self.ip + " Command runs abnormal!")
               obj.close()
               return
            if i == 1:
               if line[2] > 0:
                  msg = self.name + line[1] + u':线路中断'
                  my_alert(msg, line[1])
            if i == 0:
               rtt = int(obj.after.split(' ')[2])
               if line[2] == 0:
                  msg = self.name + line[1] + u':线路恢复' + str(rtt) + 'ms'
                  my_alert(msg, line[1])
               elif line[2] > RTT_MAX:
                  if rtt < RTT_MAX:
                     msg = self.name + line[1] + u': 线路延时恢复' + str(rtt) + 'ms'
                     my_alert(msg, line[1])
               else:
                  if rtt > RTT_MAX:
                     msg = self.name + line[1] + u': 线路延时过高' + str(rtt) + 'ms'
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

   NetMon('10.33.128.60').mon()
   #NetMon('10.33.2.148').mon()
