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




logger = logging.getLogger("client_01")

logger.info("client_01 log info at each 1 seconde")

for t in range(3600):
    logger.debug("client_01 says > debug at %04ds" %t)
    logger.info("client_01 says > info at %04ds" %t)
    logger.warning("client_01 says > warning at %04ds" %t)
    logger.error("client_01 says > error at %04ds" %t)
    time.sleep(1)



