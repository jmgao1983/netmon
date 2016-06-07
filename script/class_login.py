#!/usr/bin/env python
# -*- coding: utf-8 -*-
# auto-login net devices

import pexpect, time
from db_fun import xgetone
from my_log import logger
from my_crypt import my_decode

###class definition
class NetLogin(object):
   def __init__(self, ip):
      self.ip = ip
      self.name = ''
      sql = "select rname,pass1,pass2,pass3,login_mode,city from router where rip='%s'" % ip
      if xgetone(sql) != None:
         (self.name,self.pass1,self.pass2,self.pass3,self.login_mode,self.city) = xgetone(sql)
         self.pass1 = my_decode(self.pass1,self.name)
         self.pass2 = my_decode(self.pass2,self.name)
         self.pass3 = my_decode(self.pass3,self.name)
         #print self.pass1
         #print self.pass2
         #print self.pass3

      """
      login_mode: describe how to login the device, it's an integer like '22011,23020'.
         --first two digits imply the protocol used;
         --next two digits imply the device providers;
         --last one digit implies the auth-modes used;
      Supported protocols: {'22': 'ssh', '23': 'telnet'}
      Supported providers: {'01': 'cisco', '02': 'h3c', '03': 'huawei', '04': 'ruijie'}
      Supported auth-modes: {'0': 'pwd1+pwd2+pwd3', '1': 'pwd1+pwd2'}
      Example: to login a cisco router(IP:1.1.1.1) in linux shell, 
         --type 'ssh admin@1.1.1.1'
         when prompt 'admin@1.1.1.1's password:'
         --type 'cs1234' to login in non-priviledged mode
         and then we need priviledged mode
         --type 'enable'
         when prompt 'Password:'
         --type 'sup123'
         finally we login in priviledged mode
         now we determin this cisco router' login_mode=22010
         #'22' for 'ssh', '01' for 'cisco', '0' for 'pwd1+pwd2+pwd3'('admin'+'cs1234'+'sup123')

   # monitor targets according self.login_mode
   # 22010 for cisco_ssh_login1
   # 22011 for cisco_ssh_login2
   # 22020 for h3c_ssh_login1
   # 22021 for h3c_ssh_sa_login1(no sup password needed)
   # 22022 for h3c_ssh_login3(workaroud for ssh bug: hash mismatch)
   # 23010 for cisco_tel_login1
   # 23011 for cisco_tel_login2
   # 23013 for cisco_tel_login4(workaroud for AAA auth mode)
   # 23020 for h3c_tel_login1
   # 23021 for h3c_tel_login2
      """

   def login(self):
      if self.name == '':
         logger.warn(self.ip + ' No device with this IP!')
         return None
      if self.login_mode == 22010:
         return self.cisco_ssh_login1()
      elif self.login_mode == 22012:
         return self.cisco_ssh_login2()
      elif self.login_mode == 22020:
         return self.h3c_ssh_login1()
      elif self.login_mode == 22022:
         return self.h3c_ssh_login2()
      elif self.login_mode == 22030:
         return self.huawei_ssh_login1()
      elif self.login_mode == 22032:
         return self.huawei_ssh_login2()
      elif self.login_mode == 23010 or self.login_mode == 23040:
         return self.cisco_tel_login1()
      elif self.login_mode == 23011 or self.login_mode == 23041:
         return self.cisco_tel_login2()
      elif self.login_mode == 23012 or self.login_mode == 23042:
         return self.cisco_tel_login3()
      elif self.login_mode == 23020 or self.login_mode == 23030:
         return self.h3c_tel_login1()
      elif self.login_mode == 23021 or self.login_mode == 23031:
         return self.h3c_tel_login2()
      elif self.login_mode == 23022 or self.login_mode == 23032:
         return self.h3c_tel_login3()
      else:
         logger.error(self.ip + ' Error login_mode!')
         return None

   ## test to login, then to logout 
   def test(self):
      return self.logout(self.login())


   #login_mode=22010, cisco_ssh_login1
   def cisco_ssh_login1(self):
      try:
         logger.debug(self.ip + " Connecting...")
         ssh=pexpect.spawn('ssh -p 22 %s@%s' %(self.pass1, self.ip))
         i=ssh.expect(['word:', 'continue connecting (yes/no)?',
            'refused', 'fail', 'time', pexpect.TIMEOUT], timeout=8)
         if i == 1:
            ssh.sendline('yes')
            ssh.expect('word:',timeout=3)
         if i >= 2:
            logger.error(self.ip + " Can not reach the remote router!")
            ssh.close()
            return None
         ssh.sendline(self.pass2)
         i = ssh.expect(['>', 'word:', pexpect.TIMEOUT], timeout=3)
         if i == 1:
            logger.error(self.ip + " Error username or password!")
            ssh.close()
            return None
         ssh.sendline('en')
         ssh.expect('word:')
         ssh.sendline(self.pass3)
         i = ssh.expect(['#', '>', pexpect.TIMEOUT], timeout=3)
         if i == 1:
            logger.error(self.ip + " ERROR super password!")
            ssh.close()
            return None
      except Exception as e:
         logger.error(self.ip + ' ' + str(e))
         ssh.close()
         return None
      else:
         logger.debug(self.ip + " Logged in!")
         return ssh


   #login_mode=22012, cisco_ssh_login2 for GD AAA auth
   def cisco_ssh_login2(self):
      try:
         logger.debug(self.ip + " Connecting...")
         ssh=pexpect.spawn('ssh -p 22 %s@%s' %(self.pass1, self.ip))
         i=ssh.expect(['word:', 'continue connecting (yes/no)?',
            'refused', 'fail', 'time', pexpect.TIMEOUT], timeout=8)
         if i == 1:
            ssh.sendline('yes')
            ssh.expect('word:',timeout=3)
         if i >= 2:
            logger.error(self.ip + " Can not reach the remote router!")
            ssh.close()
            return None
         ssh.sendline(self.pass2)
         i = ssh.expect(['#', 'word:', pexpect.TIMEOUT], timeout=3)
         if i == 1:
            logger.error(self.ip + " Error username or password!")
            ssh.close()
            return None
      except Exception as e:
         logger.error(self.ip + ' ' + str(e))
         ssh.close()
         return None
      else:
         logger.debug(self.ip + " Logged in!")
         return ssh

   ##login_mode=22020, h3c_ssh_login1
   def h3c_ssh_login1(self):
      try:
         logger.debug(self.ip + " Connecting...")
         #ssh=pexpect.spawn('ssh -p 22 %s@%s' %(self.pass1, self.ip))
         ssh=pexpect.spawn('ssh -1 %s@%s' %(self.pass1, self.ip))
         i=ssh.expect(['word:', 'continue connecting (yes/no)?',
           'fail', 'refused', 'time', pexpect.TIMEOUT], timeout=8)
         if i == 1:
            ssh.sendline('yes')
            ssh.expect('word:',timeout=3)
         if i >= 2:
            logger.error(self.ip + " Can not reach the remote router!")
            ssh.close()
            return None
         ssh.sendline(self.pass2)
         i = ssh.expect(['>', 'word:', pexpect.TIMEOUT], timeout=3)
         if i == 1:
            logger.error(self.ip + " Error username or password!")
            ssh.close()
            return None
         ssh.sendline('sup')
         ssh.expect('ssword:',timeout=1)
         ssh.sendline(self.pass3)
         i = ssh.expect(['>', 'ssword:', pexpect.TIMEOUT], timeout=3)
         if i == 1:
            logger.error(self.ip + " Error super password!")
            ssh.close()
            return None
      except Exception as e:
         logger.error(self.ip + ' ' + str(e))
         ssh.close()
         return None
      else:
         logger.debug(self.ip + " Logged in!")
         return ssh
         

   ##login_mode 22022
   def h3c_ssh_login2(self):
      try:
         logger.debug(self.ip + " Connecting...")
         #ssh=pexpect.spawn('ssh -p 22 %s@%s' %(self.pass1, self.ip))
         ssh=pexpect.spawn('ssh -1 %s@%s' %(self.pass1, self.ip))
         i=ssh.expect(['word:', 'continue connecting (yes/no)?',
           'fail', 'refused', 'time', pexpect.TIMEOUT], timeout=8)
         if i == 1:
            ssh.sendline('yes')
            ssh.expect('word:',timeout=3)
         if i >= 2:
            logger.error(self.ip + " Can not reach the remote router!")
            ssh.close()
            return None
         ssh.sendline(self.pass2)
         i = ssh.expect(['>', 'word:', pexpect.TIMEOUT], timeout=3)
         if i == 1:
            logger.error(self.ip + " Error username or password!")
            ssh.close()
            return None
      except Exception as e:
         logger.error(self.ip + ' ' + str(e))
         ssh.close()
         return None
      else:
         logger.debug(self.ip + " Logged in!")
         return ssh

   ##login_mode=22030, huawei_ssh_login1
   def huawei_ssh_login1(self):
      try:
         logger.debug(self.ip + " Connecting...")
         ssh=pexpect.spawn('ssh -p 22 %s@%s' %(self.pass1, self.ip))
         i=ssh.expect(['word:', 'continue connecting (yes/no)?',
           'fail', 'refused', 'time', pexpect.TIMEOUT], timeout=8)
         if i == 1:
            ssh.sendline('yes')
            ssh.expect('word:',timeout=3)
         if i >= 2:
            logger.error(self.ip + " Can not reach the remote router!")
            ssh.close()
            return None
         ssh.sendline(self.pass2)
         i = ssh.expect(['>', 'word:', pexpect.TIMEOUT], timeout=3)
         if i == 1:
            logger.error(self.ip + " Error username or password!")
            ssh.close()
            return None
         ssh.sendline('sup')
         ssh.expect('ssword:',timeout=1)
         ssh.sendline(self.pass3)
         i = ssh.expect(['>', 'ssword:', pexpect.TIMEOUT], timeout=3)
         if i == 1:
            logger.error(self.ip + " Error super password!")
            ssh.close()
            return None
      except Exception as e:
         logger.error(self.ip + ' ' + str(e))
         ssh.close()
         return None
      else:
         logger.debug(self.ip + " Logged in!")
         return ssh
         

   ##login_mode 22032
   def huawei_ssh_login2(self):
      try:
         logger.debug(self.ip + " Connecting...")
         ssh=pexpect.spawn('ssh -p 22 %s@%s' %(self.pass1, self.ip))
         i=ssh.expect(['word:', 'continue connecting (yes/no)?',
           'fail', 'refused', 'time', pexpect.TIMEOUT], timeout=8)
         if i == 1:
            ssh.sendline('yes')
            ssh.expect('word:',timeout=3)
         if i >= 2:
            logger.error(self.ip + " Can not reach the remote router!")
            ssh.close()
            return None
         ssh.sendline(self.pass2)
         i = ssh.expect(['>', 'word:', pexpect.TIMEOUT], timeout=3)
         if i == 1:
            logger.error(self.ip + " Error username or password!")
            ssh.close()
            return None
      except Exception as e:
         logger.error(self.ip + ' ' + str(e))
         ssh.close()
         return None
      else:
         logger.debug(self.ip + " Logged in!")
         return ssh

   #login_mode=23010, cisco_tel_login1
   def cisco_tel_login1(self):
      try:
         logger.debug(self.ip + " Connecting...")
         tel=pexpect.spawn('telnet %s' % self.ip)
         i=tel.expect(['name:','refused','fail','time',pexpect.TIMEOUT], timeout=5)
         if i >= 1 :
            logger.error(self.ip + " Can not reach the remote router!")
            tel.close()
            return None
         tel.sendline(self.pass1)
         i = tel.expect('word:',timeout=2)
         tel.sendline(self.pass2)
         i = tel.expect(['>','name:',pexpect.TIMEOUT], timeout=5)
         if i == 1:
            logger.error(self.ip + " Error username or password!")
            tel.close()
            return None
         tel.sendline('en')
         tel.expect('word:',timeout=1)
         tel.sendline(self.pass3)
         i = tel.expect(['#', '>', pexpect.TIMEOUT], timeout=3)
         if i == 1:
            logger.error(self.ip + " ERROR super password!")
            tel.close()
            return None
         #
      except Exception as e:
         logger.error(self.ip + ' ' + str(e))
         tel.close()
         return None
      else:
         logger.debug(self.ip + " Logged in!")
         return tel

   #login_mode=23011, cisco_tel_login2
   def cisco_tel_login2(self):
      try:
         logger.debug(self.ip + " Connecting...")
         tel=pexpect.spawn('telnet %s' % self.ip)
         i=tel.expect(['word:','refused','fail','time',pexpect.TIMEOUT], timeout=15)
         if i >= 1:
            logger.error(self.ip + " Can not reach the remote router!")
            tel.close()
            return None
         tel.sendline(self.pass1)
         i = tel.expect(['>', 'word:', pexpect.TIMEOUT], timeout=5)
         if i == 1:
            logger.error(self.ip + " Invald password!")
            tel.close()
            return None
         tel.sendline('en')
         tel.expect('word:',timeout=1)
         tel.sendline(self.pass2)
         i = tel.expect(['#', 'word:', pexpect.TIMEOUT], timeout=3)
         if i == 1:
            logger.error(self.ip + " ERROR super password!")
            tel.close()
            return None
      except Exception as e:
         logger.error(self.ip + ' ' + str(e))
         tel.close()
         return None
      else:
         logger.debug(self.ip + " Logged in!")
         return tel

   ##login_mode 23012 for GD AAA auth login
   def cisco_tel_login3(self):
      try:
         logger.debug(self.ip + " Connecting...")
         tel=pexpect.spawn('telnet %s' % self.ip)
         i=tel.expect(['name:','refused','fail','time',pexpect.TIMEOUT], timeout=15)
         if i >= 1:
            logger.error(self.ip + " Can not reach the remote router!")
            tel.close()
            return None
         tel.sendline(self.pass1)
         i = tel.expect(['#', 'name:', pexpect.TIMEOUT], timeout=5)
         if i == 1:
            logger.error(self.ip + " Invald username or password!")
            tel.close()
            return None
      except Exception as e:
         logger.error(self.ip + ' ' + str(e))
         tel.close()
         return None
      else:
         logger.debug(self.ip + " Logged in!")
         return tel

   ##login_mode 23020
   def h3c_tel_login1(self):
      try:
         logger.debug(self.ip + " Connecting...")
         tel=pexpect.spawn('telnet %s' % self.ip)
         i=tel.expect(['name:','refused','fail','time',pexpect.TIMEOUT], timeout=15)
         if i >= 1 :
            logger.error(self.ip + " Can not reach the remote router!")
            tel.close()
            return None
         tel.sendline(self.pass1)
         i = tel.expect('word:',timeout=2)
         tel.sendline(self.pass2)
         i = tel.expect(['>','name:',pexpect.TIMEOUT], timeout=5)
         if i == 1:
            logger.error(self.ip + " Invald password!")
            tel.close()
            return None
         tel.sendline('sup')
         tel.expect('ssword:',timeout=1)
         tel.sendline(self.pass3)
         i = tel.expect(['>', 'ssword:', pexpect.TIMEOUT], timeout=3)
         if i == 1:
            logger.error(self.ip + " Error super password!")
            tel.close()
            return None
      except Exception as e:
         logger.error(self.ip + ' ' + str(e))
         tel.close()
         return None
      else:
         logger.debug(self.ip + " Logged in!")
         return tel

   ##login_mode 23021
   def h3c_tel_login2(self):
      try:
         logger.debug(self.ip + " Connecting...")
         tel=pexpect.spawn('telnet %s' % self.ip)
         i=tel.expect(['word:','refused','fail','time',pexpect.TIMEOUT], timeout=15)
         if i == 1:
            logger.error(self.ip + " Can not reach the remote router!")
            tel.close()
            return None
         tel.sendline(self.pass1)
         i = tel.expect(['>','word:', pexpect.TIMEOUT], timeout=5)
         if i == 1:
            logger.error(self.ip + " Invald password!")
            tel.close()
            return None
         tel.sendline('sup')
         tel.expect('ssword:',timeout=1)
         tel.sendline(self.pass2)
         i = tel.expect(['>', 'ssword:', pexpect.TIMEOUT], timeout=3)
         if i == 1:
            logger.error(self.ip + " Error super password!")
            tel.close()
            return None
      except Exception as e:
         logger.error(self.ip + ' ' + str(e))
         tel.close()
         return None
      else:
         logger.debug(self.ip + " Logged in!")
         return tel

   ##login_mode 23022
   def h3c_tel_login3(self):
      try:
         logger.debug(self.ip + " Connecting...")
         tel=pexpect.spawn('telnet %s' % self.ip)
         i=tel.expect(['name:','refused','fail','time',pexpect.TIMEOUT], timeout=15)
         if i >= 1 :
            logger.error(self.ip + " Can not reach the remote router!")
            tel.close()
            return None
         tel.sendline(self.pass1)
         i = tel.expect('word:',timeout=2)
         tel.sendline(self.pass2)
         i = tel.expect(['>','name:',pexpect.TIMEOUT], timeout=5)
         if i == 1:
            logger.error(self.ip + " Invald password!")
            tel.close()
            return None
      except Exception as e:
         logger.error(self.ip + ' ' + str(e))
         tel.close()
         return None
      else:
         logger.debug(self.ip + " Logged in!")
         return tel

   ##logout
   def logout(self, obj):
      #print type(obj)
      if obj == None:
         return False
      time.sleep(1)
      obj.close()
      logger.info(self.ip + " Logged out")
      return True

### test code
if __name__ == '__main__':

   NetLogin('34.0.30.35').test()
   NetLogin('34.0.30.45').test()
   NetLogin('34.0.223.2').test()
   NetLogin('15.34.254.5').test()
   NetLogin('15.34.81.253').test()
   NetLogin('15.34.177.253').test()
   NetLogin('15.34.49.99').test()
   NetLogin('15.34.21.85').test()
   NetLogin('34.1.3.25').test()
   NetLogin('34.112.31.2').test()
