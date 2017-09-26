#!/usr/bin/env python
# -*- coding: utf-8 -*-
#'RPing(Remote Ping): auto-login net devices and save config'

import pexpect, os, time, hashlib, class_login
from my_log import logger
from netmon_env import base_dir
from NetworkDevice import device_netcap

###class definition
class NetSav(class_login.NetLogin):
   def __init__(self, ip):
      class_login.NetLogin.__init__(self, ip)
      self.txt_conf = ''


   def save(self):
      if device_netcap.get(self.corp) == None:
         logger.error(self.ip + ' Error : unsupported device!')
         return

      obj = self.login()
      if obj == None:
         logger.error(self.ip + ' Error : saving config failed due to login error!')
         return

      prompt = self.name + device_netcap.get(self.corp).get('prompt')
      pageCmd = device_netcap.get(self.corp).get('page')
      saveCmd = device_netcap.get(self.corp).get('conf')[0]

      try:
         obj.sendline(pageCmd)
         obj.expect([prompt, pexpect.TIMEOUT], timeout=3)

         #capture running-configration
         logger.debug(self.ip + ' executing: ' + saveCmd)
         obj.sendline(saveCmd)
         i = obj.expect([prompt, pexpect.TIMEOUT], timeout=20)
         if i == 1:
            logger.error(self.ip + ' error exec ' + saveCmd)
            obj.close()
            return
         self.txt_conf = obj.before
         
         logger.debug(self.ip + ' logged out!')
         obj.close()
      except Exception as e:
         logger.error(self.ip + ' ' + str(e))
         obj.close()
         return
      else:
         self.save_to_disk()

   ##save config to disk
   def save_to_disk(self):
      timestr = time.strftime('%Y%m%d%H%M%S',time.localtime())
      logger.debug(self.ip + ' start to save config to disk')

      fname = self.name + '-' + timestr
      city = hashlib.md5((self.city).encode('UTF-8')).hexdigest()
      fpath = base_dir + r'/down/conf/%s/%s' % (city, self.name)
      if not os.path.exists(fpath):
         try:
            os.makedirs(fpath)
         except Exception as e:
            logger.error(str(e))
            return

      os.chdir(fpath)

      #save config
      try:
         file = open(fname, 'w')
         file.writelines(self.txt_conf)
      except Exception as e:
         logger.error(str(e))
      else:
         logger.info(self.ip + ' finish saving config!')
      finally:
         file.close()


### test code
if __name__ == '__main__':

   NetSav('10.33.2.148').save()
   #NetSav('15.34.21.85').save()
