#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
from my_log import logger
from my_crypt import mycrypt


if len(sys.argv) == 2:
    print(mycrypt.encrypt(sys.argv[1]))
else:
    logger.error(sys.argv[0]+" Error参数错误")
