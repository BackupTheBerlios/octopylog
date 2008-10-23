# -*- coding: UTF-8 -*-
###########################################################
# Project  : Octopylog                                    #
# License  : GNU General Public License (GPL)             #
# Author   : JMB                                          #
# Date     : 21/10/08                                     #
###########################################################


__version__ = "$Revision: 1.1 $"
__author__ = "$Author: octopy $"


import time
import logging
import logging.handlers


rootLogger = logging.getLogger("")
rootLogger.setLevel(logging.DEBUG)
socketHandler = logging.handlers.SocketHandler("localhost", logging.handlers.DEFAULT_TCP_LOGGING_PORT)

rootLogger.addHandler(socketHandler)




logger = logging.getLogger("client_02")

logger.info("client_02 log info at each 100 ms")

for t in range(10*3600):
    logger.debug("client_02 says > debug at %09ds" %t*100)
    logger.info("client_02says > info at %09ds" %t*100)
    logger.warning("client_02 says > warning at %09ds" %t*100)
    logger.error("client_02 says > error at %09ds" %t*100)
    time.sleep(0.1)


