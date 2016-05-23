#!/usr/bin/env python
# -*- coding: utf-8 -*-

import md5

def my_encode(txt, seed):
   tmp = md5.new((seed).encode('UTF-8')).hexdigest()
   i = 0
   N = len(txt)
   r = ''
   offset = 0
   while i < N:
      if ord(tmp[i]) > 96:
         offset = ord(tmp[i]) - 87
      else:
         offset = ord(tmp[i]) - 48
      r = r + chr(ord(txt[i]) - offset)
      i = i + 1
   #print tmp
   return r
   
def my_decode(txt, seed):
   tmp = md5.new((seed).encode('UTF-8')).hexdigest()
   i = 0
   N = len(txt)
   r = ''
   offset = 0
   while i < N:
      if ord(tmp[i]) > 96:
         offset = ord(tmp[i]) - 87
      else:
         offset = ord(tmp[i]) - 48
      r = r + chr(ord(txt[i]) + offset)
      i = i + 1
   #print tmp
   return r
   


### test code
if __name__ == '__main__':
   #test = '!"#$%&()*+,-./:;<=?@[\]^-`{}|~' + "'"
   test = 'ccbwlgl0701'
   code = my_encode(test,'ZJ_TZ_ECN_SW_1')
   print test
   print code
   print my_decode(code,'ZJ_TZ_ECN_SW_1')
   
