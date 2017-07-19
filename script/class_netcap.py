#!/usr/bin/env python
# -*- coding: utf-8 -*-
#'RPing(Remote Ping): auto-login net devices and check status'

import pexpect, os, time, hashlib, class_login
from db_fun import xgetone
from my_log import logger
from netmon_env import base_dir

###class definition
class NetCap(class_login.NetLogin):
   def __init__(self, ip):
      class_login.NetLogin.__init__(self, ip)
      self.txt_conf = ''
      self.txt_mod = ''
      self.txt_int = ''
      self.txt_stp = ''
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
         self.huawei_cap(self.login())
      elif provider == 4:
         self.cisco_cap(self.login())
      elif provider == 5:
         self.junos_cap(self.login())
      else:
         logger.error(self.ip + ' Error : device with unknown provider!')

   ##cisco_cap
   def cisco_cap(self, obj):
      if obj == None:
         return
      try:
         obj.sendline('terminal len 0')
         obj.expect([self.wait2, pexpect.TIMEOUT], timeout=2)

         #capture running-configration
         logger.debug(self.ip + ' executing [sh run]')
         obj.sendline('sh run')
         i = obj.expect([self.wait2, pexpect.TIMEOUT], timeout=20)
         if i == 1:
            logger.error(self.ip + ' error exec [sh run]')
            obj.close()
            return
         self.txt_conf = obj.before

         #capture module info
         logger.debug(self.ip + ' executing [sh module]')
         obj.sendline('sh module')
         i = obj.expect([self.wait2, pexpect.TIMEOUT], timeout=20)
         if i == 1:
            logger.error(self.ip + ' error exec [sh module]')
            obj.close()
            return
         self.txt_mod = obj.before

         #capture inventory info
         logger.debug(self.ip + ' executing [sh invent]')
         obj.sendline('sh invent')
         i = obj.expect([self.wait2, pexpect.TIMEOUT], timeout=20)
         if i == 1:
            logger.error(self.ip + ' error exec [sh invent]')
            obj.close()
            return
         self.txt_mod += obj.before

         #capture int-lv2
         logger.debug(self.ip + ' executing [sh int status]')
         obj.sendline('sh int status | in connected')
         i = obj.expect([self.wait2, pexpect.TIMEOUT], timeout=20)
         if i == 1:
            logger.error(self.ip + ' error exec [sh int status]')
            obj.close()
            return
         self.txt_int = obj.before

         #capture int-lv3
         logger.debug(self.ip + ' executing [sh ip int b]')
         obj.sendline('sh ip int b | in up')
         i = obj.expect([self.wait2, pexpect.TIMEOUT], timeout=20)
         if i == 1:
            logger.error(self.ip + ' error exec [sh ip int b]')
            obj.close()
            return
         self.txt_int += obj.before

         #capture stp info
         logger.debug(self.ip + ' executing [sh spanning-tree root id]')
         obj.sendline('sh spanning-tree root id')
         i = obj.expect([self.wait2, pexpect.TIMEOUT], timeout=20)
         if i == 1:
            logger.error(self.ip + ' error exec [sh spanning-tree root id]')
            obj.close()
            return
         self.txt_stp = obj.before

         #capture route summary info
         logger.debug(self.ip + ' executing [sh ip route sum]')
         obj.sendline('sh ip route sum')
         i = obj.expect([self.wait2, pexpect.TIMEOUT], timeout=20)
         if i == 1:
            logger.error(self.ip + ' error exec [sh ip route sum]')
            obj.close()
            return
         self.txt_route_sum = obj.before

         #capture routing table
         logger.debug(self.ip + ' executing [sh ip route]')
         obj.sendline('sh ip route')
         i = obj.expect([self.wait2, pexpect.TIMEOUT], timeout=20)
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
         self.save_to_disk()
         #trim routing table
         cmd = "bash " + base_dir + "/script/trim_cisco.sh"
         val = os.system(cmd)
         if(val != 0):
            logger.error(self.ip + ' Error exec trim_route script')


   ##h3c_cap
   def h3c_cap(self, obj):
      if obj == None:
         return
      try:
         obj.sendline('screen-length disable')
         obj.expect(self.wait1, timeout=2)

         #capture running-configration
         logger.debug(self.ip + ' executing [disp curr]')
         obj.sendline('disp curr')
         i = obj.expect([self.wait1, pexpect.TIMEOUT], timeout=20)
         if i == 1:
            logger.debug(self.ip + ' error exec [disp curr]')
            obj.close()
            return
         self.txt_conf = obj.before

         #capture module info
         logger.debug(self.ip + ' executing [disp device]')
         obj.sendline('disp device')
         i = obj.expect([self.wait1, pexpect.TIMEOUT], timeout=20)
         if i == 1:
            logger.debug(self.ip + ' error exec [disp device]')
            obj.close()
            return
         self.txt_mod = obj.before

         #capture interface info
         logger.debug(self.ip + ' executing [disp int brief]')
         obj.sendline('disp int brief')
         i = obj.expect([self.wait1, pexpect.TIMEOUT], timeout=20)
         if i == 1:
            logger.debug(self.ip + ' error exec [disp int brief]')
            obj.close()
            return
         self.txt_int = obj.before

         #capture stp info-1
         logger.debug(self.ip + ' executing [disp stp root]')
         obj.sendline('disp stp root')
         i = obj.expect([self.wait1, pexpect.TIMEOUT], timeout=20)
         if i == 1:
            logger.debug(self.ip + ' error exec [disp stp root]')
            obj.close()
            return
         self.txt_stp = obj.before

         #capture stp info-2
         logger.debug(self.ip + ' executing [disp stp brief]')
         obj.sendline('disp stp brief')
         i = obj.expect([self.wait1, pexpect.TIMEOUT], timeout=20)
         if i == 1:
            logger.debug(self.ip + ' error exec [disp stp brief]')
            obj.close()
            return
         self.txt_stp += obj.before

         #capture route summary info
         logger.debug(self.ip + ' executing [disp ip rout stat]')
         obj.sendline('disp ip rout stat')
         i = obj.expect([self.wait1, pexpect.TIMEOUT], timeout=20)
         if i == 1:
            logger.debug(self.ip + ' error exec [disp ip rout stat]')
            obj.close()
            return
         self.txt_route_sum = obj.before

         #capture routing table
         logger.debug(self.ip + ' executing [disp ip rout]')
         obj.sendline('disp ip rout')
         i = obj.expect([self.wait1, pexpect.TIMEOUT], timeout=20)
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
         self.save_to_disk()
         #trim routing table
         cmd = "bash " + base_dir + "/script/trim_h3c.sh"
         val = os.system(cmd)
         if(val != 0):
            logger.error(self.ip + ' Error exec trim_route script')


   ##huawei_cap
   def huawei_cap(self, obj):
      if obj == None:
         return
      try:
         obj.sendline('screen-length 0')
         obj.expect(self.wait1, timeout=2)

         #capture running-configration
         logger.debug(self.ip + ' executing [disp curr]')
         obj.sendline('disp curr')
         i = obj.expect([self.wait1, pexpect.TIMEOUT], timeout=20)
         if i == 1:
            logger.debug(self.ip + ' error exec [disp curr]')
            obj.close()
            return
         self.txt_conf = obj.before

         #capture module info
         logger.debug(self.ip + ' executing [disp device]')
         obj.sendline('disp device')
         i = obj.expect([self.wait1, pexpect.TIMEOUT], timeout=20)
         if i == 1:
            logger.debug(self.ip + ' error exec [disp device]')
            obj.close()
            return
         self.txt_mod = obj.before

         #capture interface info
         logger.debug(self.ip + ' executing [disp int brief]')
         obj.sendline('disp int brief')
         i = obj.expect([self.wait1, pexpect.TIMEOUT], timeout=20)
         if i == 1:
            logger.debug(self.ip + ' error exec [disp int brief]')
            obj.close()
            return
         self.txt_int = obj.before

         #capture stp info-1
         logger.debug(self.ip + ' executing [disp stp bri root]')
         obj.sendline('disp stp bri root')
         i = obj.expect([self.wait1, pexpect.TIMEOUT], timeout=20)
         if i == 1:
            logger.debug(self.ip + ' error exec [disp stp bri root]')
            obj.close()
            return
         self.txt_stp = obj.before

         #capture stp info-2
         logger.debug(self.ip + ' executing [disp stp brief]')
         obj.sendline('disp stp brief')
         i = obj.expect([self.wait1, pexpect.TIMEOUT], timeout=20)
         if i == 1:
            logger.debug(self.ip + ' error exec [disp stp brief]')
            obj.close()
            return
         self.txt_stp += obj.before

         #capture route summary info
         logger.debug(self.ip + ' executing [disp ip rout stat]')
         obj.sendline('disp ip rout stat')
         i = obj.expect([self.wait1, pexpect.TIMEOUT], timeout=20)
         if i == 1:
            logger.debug(self.ip + ' error exec [disp ip rout stat]')
            obj.close()
            return
         self.txt_route_sum = obj.before

         #capture routing table
         logger.debug(self.ip + ' executing [disp ip rout]')
         obj.sendline('disp ip rout')
         i = obj.expect([self.wait1, pexpect.TIMEOUT], timeout=20)
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
         self.save_to_disk()
         #trim routing table
         cmd = "bash " + base_dir + "/script/trim_huawei.sh"
         val = os.system(cmd)
         if(val != 0):
            logger.error(self.ip + ' Error exec trim_route script')


   ##junos_cap
   def junos_cap(self, obj):
      if obj == None:
         return
      try:
         obj.sendline('set cli screen-length 0')
         obj.expect([self.wait1, pexpect.TIMEOUT], timeout=2)

         #capture running-configration
         logger.debug(self.ip + ' executing [show configuration | display set]')
         obj.sendline('show configuration | display set')
         i = obj.expect([self.wait1, pexpect.TIMEOUT], timeout=20)
         if i == 1:
            logger.error(self.ip + 'error exec [show configuration | display set]')
            obj.close()
            return
         self.txt_conf = obj.before

         #capture module info
         logger.debug(self.ip + ' executing [show chassis hardware detail]')
         obj.sendline('show chassis hardware detail')
         i = obj.expect([self.wait1, pexpect.TIMEOUT], timeout=20)
         if i == 1:
            logger.error(self.ip + ' error exec [show chassis hardware detail]')
            obj.close()
            return
         self.txt_mod = obj.before

         #capture int
         logger.debug(self.ip + ' executing [show interfaces terse]')
         obj.sendline('show interfaces terse')
         i = obj.expect([self.wait1, pexpect.TIMEOUT], timeout=20)
         if i == 1:
            logger.error(self.ip + ' error exec [show interfaces terse]')
            obj.close()
            return
         self.txt_int = obj.before

         #capture stp info
         logger.debug(self.ip + ' executing [show spanning-tree interface]')
         obj.sendline('show spanning-tree interface')
         i = obj.expect([self.wait1, pexpect.TIMEOUT], timeout=20)
         if i == 1:
            logger.error(self.ip + ' error exec [show spanning-tree interface]')
            obj.close()
            return
         self.txt_stp = obj.before

         #capture stp info-2
         logger.debug(self.ip + ' executing [show spanning-tree bridge | match root]')
         obj.sendline('show spanning-tree bridge | match root')
         i = obj.expect([self.wait1, pexpect.TIMEOUT], timeout=20)
         if i == 1:
            logger.error(self.ip + ' error exec [show spanning-tree bridge | match root]')
            obj.close()
            return
         self.txt_stp += obj.before

         #capture route summary info
         logger.debug(self.ip + ' executing [show route summary]')
         obj.sendline('show route summary')
         i = obj.expect([self.wait1, pexpect.TIMEOUT], timeout=20)
         if i == 1:
            logger.error(self.ip + ' error exec [show route summary]')
            obj.close()
            return
         self.txt_route_sum = obj.before

         #capture routing table
         logger.debug(self.ip + ' executing [show route terse]')
         obj.sendline('show route terse')
         i = obj.expect([self.wait1, pexpect.TIMEOUT], timeout=20)
         if i == 1:
            logger.error(self.ip + ' error exec [show route terse]')
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
         self.save_to_disk()
         #trim routing table
         cmd = "bash " + base_dir + "/script/trim_junos.sh"
         val = os.system(cmd)
         if(val != 0):
            logger.error(self.ip + ' Error exec trim_route script')


   ##save file
   def save_to_disk(self):
      logger.debug(self.ip + ' start to save info to disk')
      city = hashlib.md5((self.city).encode('UTF-8')).hexdigest()
      fpath = base_dir + r'/down/cap/%s/%s' % (city, self.name)
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

      logger.info(self.ip + ' finish saving info!')


### test code
if __name__ == '__main__':

   NetCap('10.7.10.254').capture()
   NetCap('10.7.11.1').capture()
   NetCap('10.7.254.1').capture()
   NetCap('10.100.1.1').capture()
   NetCap('10.100.255.68').capture()
