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




logger = logging.getLogger("logging_limit_01")

logger.info("logging data for test limit")





def gen_str_hc(number, step=16):
    l = list()
    for i in range(number):
        s = ""
        for j in range(i+1):
            t = "%d" % (step*j)
            t = t.ljust(step, ".")
            s += t
        l.append(s)
    return l, len(max(l))



lobj, max = gen_str_hc(32, 1024)


llog = [logger.debug,
       logger.info,
       logger.warning,
       logger.error,
       ]


for t in range(1):
    
    for ll in llog:
        
        ll("Max : %d" % max)

    
    for lo in  lobj:
        for ll in llog:
            s = lo.__str__()
            print s
            ll("%s" % s)
    print "%d" % t
    time.sleep(1)



