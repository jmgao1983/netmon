#!/usr/bin/env python
# -*- coding: utf-8 -*-

import class_login, sys
from my_log import logger

if len(sys.argv) == 2:
   class_login.NetLogin(sys.argv[1]).test()
else:
   logger.error(sys.argv[0]+" Error参数错误")
