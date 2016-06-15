#!/usr/bin/env python
# -*- coding: utf-8 -*-
#'RPing(Remote Ping): auto-login net devices and save config'

import pexpect, os, time, hashlib, class_login
from db_fun import xgetone, xgetall
from my_log import logger

###class definition
class NetSav(class_login.NetLogin):
   def __init__(self, ip):
      class_login.NetLogin.__init__(self, ip)
      self.txt_conf = ''


   def save(self):
      #check 'login_mode' describe in 'class_login.py'
      provider = (self.login_mode % 1000) / 10
      if provider == 1:
         self.cisco_save(self.login())
      elif provider == 2:
         self.h3c_save(self.login())
      elif provider == 3:
         self.huawei_save(self.login())
      elif provider == 4:
         self.cisco_save(self.login())
      else:
         logger.error(self.ip + ' Error : device with unknown provider!')


   ##cisco_save
   def cisco_save(self, obj):
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

         #copy run start
         logger.debug(self.ip + ' executing [write]')
         obj.sendline('write')
         i = obj.expect([str_cisco, pexpect.TIMEOUT], timeout=100)
         if i == 1:
            logger.error(self.ip + ' error exec [write]')
            obj.close()
            return

         logger.debug(self.ip + ' logged out!')
         obj.close()
      except Exception as e:
         logger.error(self.ip + ' ' + str(e))
         obj.close()
         return
      else:
         self.save_to_disk()


   ##h3c_save
   def h3c_save(self, obj):
      if obj == None:
         return
      try:
         str_h3c = self.name + '>'
         obj.sendline('screen-length disable')
         obj.expect(str_h3c, timeout=2)

         #capture running-configration
         logger.debug(self.ip + ' executing [disp curr]')
         obj.sendline('disp curr')
         i = obj.expect([str_h3c, pexpect.TIMEOUT], timeout=80)
         if i == 1:
            logger.error(self.ip + ' error exec [disp curr]')
            obj.close()
            return
         self.txt_conf = obj.before

         #save config
         logger.debug(self.ip + ' executing [save]')
         obj.sendline("save safe\ny\n\ny\n")
         i = obj.expect([str_h3c, pexpect.TIMEOUT], timeout=100)
         if i == 1:
            logger.error(self.ip + ' error exec [save]')
            obj.close()
            return

         logger.debug(self.ip + ' logged out!')
         obj.close()
      except Exception as e:
         logger.error(self.ip + ' ' + str(e))
         obj.close()
         return
      else:
         self.save_to_disk()

   ##huawei_save
   def huawei_save(self, obj):
      if obj == None:
         return
      try:
         str_h3c = self.name + '>'
         obj.sendline('sys\nuser-interface vty 0 4\nscreen-length 0\n')
         obj.expect(self.name + ']', timeout=2)

         #capture running-configration
         logger.debug(self.ip + ' executing [disp curr]')
         obj.sendline('disp curr')
         i = obj.expect([str_h3c, pexpect.TIMEOUT], timeout=60)
         if i == 1:
            logger.error(self.ip + ' error exec [disp curr]')
            obj.close()
            return
         self.txt_conf = obj.before

         obj.sendline('undo screen-length\nquit\nquit\n')

         #save config
         logger.debug(self.ip + ' executing [save]')
         obj.sendline("save\ny\n\ny\n")
         i = obj.expect([str_h3c, pexpect.TIMEOUT], timeout=100)
         if i == 1:
            logger.error(self.ip + ' error exec [save]')
            obj.close()
            return

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
      fpath = r'/var/www/html/netmon/down/conf/%s/%s' % (city, self.name)
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

   #NetSav('34.0.30.35').save()
   #NetSav('34.0.30.45').save()
   NetSav('34.0.223.2').save()
   #NetSav('15.34.254.5').save()
   #NetSav('15.34.81.253').save()
   #NetSav('15.34.177.253').save()
   #NetSav('15.34.49.99').save()
   #NetSav('15.34.21.85').save()
