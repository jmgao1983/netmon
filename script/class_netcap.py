#!/usr/bin/env python
# -*- coding: utf-8 -*-
#'RPing(Remote Ping): auto-login net devices and check status'

import pexpect, os, time, md5, class_login
from db_fun import xgetone
from my_log import logger

###class definition
class NetCap(class_login.NetLogin):
   def __init__(self, ip):
      class_login.NetLogin.__init__(self, ip)
      self.txt_conf = ''
      self.txt_mod = ''
      self.txt_invent = ''
      self.txt_int = ''
      self.txt_ipint = ''
      self.txt_stp = ''
      self.txt_stp2 = ''
      self.txt_route_sum = ''
      self.txt_route = ''

   def capture(self):
      #check 'login_mode' describe in 'class_login.py'
      provider = (self.login_mode % 1000) / 10
      if provider == 1:
         self.cisco_cap(self.login())
      elif provider == 2:
         self.h3c_cap(self.login())
      elif provider == 3:
         self.h3c_cap(self.login())
      elif provider == 4:
         self.cisco_cap(self.login())
      else:
         logger.error(self.ip + ' Error : device with unknown provider!')

   ##cisco_cap
   def cisco_cap(self, obj):
      if obj == None:
         return
      try:
         str_cisco = self.name + '#'
         obj.sendline('terminal len 0')
         obj.expect([str_cisco, pexpect.TIMEOUT], timeout=2)

         #capture running-configration
         logger.debug(self.ip + ' executing [sh run]')
         obj.sendline('sh run')
         i = obj.expect([str_cisco, pexpect.TIMEOUT], timeout=20)
         if i == 1:
            logger.error(self.ip + ' error exec [sh run]')
            obj.close()
            return
         self.txt_conf = obj.before

         #capture module info
         logger.debug(self.ip + ' executing [sh module]')
         obj.sendline('sh module')
         i = obj.expect([str_cisco, pexpect.TIMEOUT], timeout=20)
         if i == 1:
            logger.error(self.ip + ' error exec [sh module]')
            obj.close()
            return
         self.txt_mod = obj.before

         #capture inventory info
         logger.debug(self.ip + ' executing [sh invent]')
         obj.sendline('sh invent')
         i = obj.expect([str_cisco, pexpect.TIMEOUT], timeout=20)
         if i == 1:
            logger.error(self.ip + ' error exec [sh invent]')
            obj.close()
            return
         self.txt_invent = obj.before

         #capture int-lv2
         logger.debug(self.ip + ' executing [sh int status]')
         obj.sendline('sh int status | in connected')
         i = obj.expect([str_cisco, pexpect.TIMEOUT], timeout=20)
         if i == 1:
            logger.error(self.ip + ' error exec [sh int status]')
            obj.close()
            return
         self.txt_int = obj.before

         #capture int-lv3
         logger.debug(self.ip + ' executing [sh ip int b]')
         obj.sendline('sh ip int b | in up')
         i = obj.expect([str_cisco, pexpect.TIMEOUT], timeout=20)
         if i == 1:
            logger.error(self.ip + ' error exec [sh ip int b]')
            obj.close()
            return
         self.txt_ipint = obj.before

         #capture stp info
         logger.debug(self.ip + ' executing [sh spanning-tree root id]')
         obj.sendline('sh spanning-tree root id')
         i = obj.expect([str_cisco, pexpect.TIMEOUT], timeout=20)
         if i == 1:
            logger.error(self.ip + ' error exec [sh spanning-tree root id]')
            obj.close()
            return
         self.txt_stp = obj.before

         #capture route summary info
         logger.debug(self.ip + ' executing [sh ip route sum]')
         obj.sendline('sh ip route sum')
         i = obj.expect([str_cisco, pexpect.TIMEOUT], timeout=20)
         if i == 1:
            logger.error(self.ip + ' error exec [sh ip route sum]')
            obj.close()
            return
         self.txt_route_sum = obj.before

         #capture routing table
         logger.debug(self.ip + ' executing [sh ip route]')
         obj.sendline('sh ip route')
         i = obj.expect([str_cisco, pexpect.TIMEOUT], timeout=20)
         if i == 1:
            logger.error(self.ip + ' error exec [sh ip route]')
            obj.close()
            return
         self.txt_route = obj.before

         logger.debug(self.ip + ' logged out!')
         obj.close()
      except Exception as e:
         logger.error(self.ip + ' ' + str(e))
         obj.close()
         return
      else:
         self.cisco_save()

   ##h3c_cap
   def h3c_cap(self, obj):
      if obj == None:
         return
      try:
         str_h3c = self.name + '>'
         obj.sendline('screen-length disable')
         obj.expect(str_h3c, timeout=2)

         #capture running-configration
         logger.debug(self.ip + ' executing [disp curr]')
         obj.sendline('disp curr')
         i = obj.expect([str_h3c, pexpect.TIMEOUT], timeout=20)
         if i == 1:
            logger.debug(self.ip + ' error exec [disp curr]')
            obj.close()
            return
         self.txt_conf = obj.before

         #capture module info
         logger.debug(self.ip + ' executing [disp device]')
         obj.sendline('disp device')
         i = obj.expect([str_h3c, pexpect.TIMEOUT], timeout=20)
         if i == 1:
            logger.debug(self.ip + ' error exec [disp device]')
            obj.close()
            return
         self.txt_mod = obj.before

         #capture interface info
         logger.debug(self.ip + ' executing [disp int brief]')
         obj.sendline('disp int brief | in UP')
         i = obj.expect([str_h3c, pexpect.TIMEOUT], timeout=20)
         if i == 1:
            logger.debug(self.ip + ' error exec [disp int brief]')
            obj.close()
            return
         self.txt_int = obj.before

         #capture stp info-1
         logger.debug(self.ip + ' executing [disp stp root]')
         obj.sendline('disp stp root')
         i = obj.expect([str_h3c, pexpect.TIMEOUT], timeout=20)
         if i == 1:
            logger.debug(self.ip + ' error exec [disp stp root]')
            obj.close()
            return
         self.txt_stp = obj.before

         #capture stp info-2
         logger.debug(self.ip + ' executing [disp stp brief]')
         obj.sendline('disp stp brief')
         i = obj.expect([str_h3c, pexpect.TIMEOUT], timeout=20)
         if i == 1:
            logger.debug(self.ip + ' error exec [disp stp brief]')
            obj.close()
            return
         self.txt_stp2 = obj.before

         #capture route summary info
         logger.debug(self.ip + ' executing [disp ip rout stat]')
         obj.sendline('disp ip rout stat')
         i = obj.expect([str_h3c, pexpect.TIMEOUT], timeout=20)
         if i == 1:
            logger.debug(self.ip + ' error exec [disp ip rout stat]')
            obj.close()
            return
         self.txt_route_sum = obj.before

         #capture routing table
         logger.debug(self.ip + ' executing [disp ip rout]')
         obj.sendline('disp ip rout')
         i = obj.expect([str_h3c, pexpect.TIMEOUT], timeout=20)
         if i == 1:
            logger.debug(self.ip + ' error exec [disp ip rout]')
            obj.close()
            return
         self.txt_route = obj.before

         logger.debug(self.ip + ' logged out!')
         obj.close()
      except Exception as e:
         logger.error(self.ip + ' ' + str(e))
         obj.close()
         return
      else:
         self.h3c_save()

   ##cisco_save file
   def cisco_save(self):
      logger.debug(self.ip + ' start to save info to disk')
      city = md5.new((self.city).encode('UTF-8')).hexdigest()
      fpath = r'/var/www/html/netmon/down/cap/%s/%s' % (city, self.name)
      if not os.path.exists(fpath):
         try:
            os.makedirs(fpath)
         except Exception as e:
            logger.error(str(e))
            return

      os.chdir(fpath)

      #save config
      file = open('conf', 'w')
      try:
         file.writelines(self.txt_conf)
      finally:
         file.close()

      #save module-info
      file = open('mod', 'w')
      try:
         file.writelines(self.txt_mod)
         file.writelines(self.txt_invent)
      finally:
         file.close()

      #save interface-info
      file = open('int', 'w')
      try:
         file.writelines(self.txt_int)
         file.writelines(self.txt_ipint)
      finally:
         file.close()

      #save spanning-tree info
      file = open('stp', 'w')
      try:
         file.writelines(self.txt_stp)
      finally:
         file.close()

      #save route summary info
      file = open('routesum', 'w')
      try:
         file.writelines(self.txt_route_sum)
      finally:
         file.close()

      #save routing table
      file = open('route.txt', 'w')
      try:
         file.writelines(self.txt_route)
      finally:
         file.close()

      #trim routing table
      val = os.system("bash ../../../../script/trim_cisco.sh")
      if(val != 0):
         logger.error(self.ip + ' Error exec trim_route script')

      logger.info(self.ip + ' finish saving info!')

   ##h3c_save file
   def h3c_save(self):
      logger.debug(self.ip + ' start to save info to disk')
      city = md5.new((self.city).encode('UTF-8')).hexdigest()
      fpath = r'/var/www/html/netmon/down/cap/%s/%s' % (city, self.name)
      if not os.path.exists(fpath):
         try:
            os.makedirs(fpath)
         except Exception as e:
            logger.error(str(e))
            return

      os.chdir(fpath)

      #save config
      file = open('conf', 'w')
      try:
         file.writelines(self.txt_conf)
      finally:
         file.close()

      #save module-info
      file = open('mod', 'w')
      try:
         file.writelines(self.txt_mod)
      finally:
         file.close()

      #save interface-info
      file = open('int', 'w')
      try:
         file.writelines(self.txt_int)
      finally:
         file.close()

      #save spanning-tree info
      file = open('stp', 'w')
      try:
         file.writelines(self.txt_stp)
         file.writelines(self.txt_stp2)
      finally:
         file.close()

      #save route summary info
      file = open('routesum', 'w')
      try:
         file.writelines(self.txt_route_sum)
      finally:
         file.close()

      #save routing table
      file = open('route.txt', 'w')
      try:
         file.writelines(self.txt_route)
      finally:
         file.close()

      #trim routing table
      val = os.system("bash ../../../../script/trim_h3c.sh")
      if(val != 0):
         logger.error(self.ip + ' Error exec trim_route script')

      logger.info(self.ip + ' finish saving info!')

### test code
if __name__ == '__main__':

   #NetCap('15.34.254.5').capture()
   NetCap('34.0.30.45').capture()
