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



# log different data type


logger = logging.getLogger("logging_data_01")
logger.info("logging data for parsing")





lobj = [   1,
        "string",
        [0, 1, 2],
        ["abc", "def"],
        [0, "abc"],
        {"1":1, "2":2},
        {"abc":[0,1,2]},
     ]


llog = [logger.debug,
       logger.info,
       logger.warning,
       logger.error,
       ]


for t in range(1):
    
    for lo in  lobj:
        for ll in llog:
            s = lo.__str__()
            print s
            ll("%s" % s)
    print "%d" % t
    time.sleep(1)



