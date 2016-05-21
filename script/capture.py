#!/usr/bin/env python
# -*- coding: utf-8 -*-

import class_netcap, sys
from my_log import logger

if len(sys.argv) == 2:
   class_netcap.NetCap(sys.argv[1]).capture()
else:
   logger.error(sys.argv[0]+" Error参数错误")
