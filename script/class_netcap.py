#!/usr/bin/env python
# -*- coding: utf-8 -*-
# auto-login net devices and check status'

import pexpect, os, hashlib
from class_login import NetLogin
from my_log import logger
from netmon_env import base_dir
from NetworkDevice import device

###class definition
class NetCap(NetLogin):
   def __init__(self, ip):
      NetLogin.__init__(self, ip)
      self.re_conf = ''
      self.re_mod = ''
      self.re_int = ''
      self.re_stp = ''
      self.re_routesum = ''
      self.re_route = ''

   def capture(self):
      if device.get(self.corp) == None:
         logger.error(self.ip + ' Error : unsupported device to capture!')
         return
      obj = self.login()
      if obj == None:
         logger.error(self.ip + ' Error : capture failure due to login error!')
         return
      
      prompt = self.name + device.get(self.corp).get('prompt')
      pageCmd = device.get(self.corp).get('page')
      cmdSet = {
         'conf': device.get(self.corp).get('conf'),
         'routesum': device.get(self.corp).get('routesum'),
         'route': device.get(self.corp).get('route'),
         'mod': device.get(self.corp).get('mod'),
         'int': device.get(self.corp).get('int'),
         'stp': device.get(self.corp).get('stp')
      }
      try:
         obj.sendline(pageCmd)
         obj.expect([prompt, pexpect.TIMEOUT], timeout=3)

         #exec CMDs on the target device
         for (cmd_key, cmd_value) in cmdSet.items():
            for cmd_str in cmd_value:
               logger.debug(self.ip + ' executing ' + cmd_str)
               obj.sendline(cmd_str)
               i = obj.expect([prompt, pexpect.TIMEOUT], timeout=20)
               if i == 1:
                  logger.error(self.ip + ' error exec ' + cmd_str)
                  obj.close()
                  return
               temp = self.__getattribute__('re_%s' % cmd_key)
               temp += obj.before
               self.__setattr__('re_%s' % cmd_key, temp)

         logger.debug(self.ip + ' logged out!')
         obj.close()
      except Exception as e:
         logger.error(self.ip + ' ' + str(e))
         obj.close()
         return
      else:
         #save things to disk
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

         for cmd_key in cmdSet.keys():
            try:
               file = open(cmd_key, 'w')
               file.writelines(self.__getattribute__('re_%s' % cmd_key))
            finally:
               file.close()

         #trim routing table
         cmd = 'bash %s/script/trim_%s.sh' % (base_dir, self.corp)
         val = os.system(cmd)
         if(val != 0):
            logger.error(self.ip + ' Error exec trim_route script')

### test code
if __name__ == '__main__':

   #NetCap('10.7.10.254').capture()
   #NetCap('10.7.11.1').capture()
   #NetCap('10.7.254.1').capture()
   #NetCap('10.100.1.1').capture()
   NetCap('10.100.254.86').capture()
