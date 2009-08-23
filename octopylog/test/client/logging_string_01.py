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






vector = [  "предыстория",
            "الإنكليزية",
            u"предыстория",
            u"الإنكليزية",
            u"ascii",
            "ascii",
            u"\u0627\u0644\u0625\u0646\u0643\u0644\u064a\u0632\u064a\u0629"
            "\u0627\u0644\u0625\u0646\u0643\u0644\u064a\u0632\u064a\u0629"
            u"\xd8\xa7\xd9\x84\xd8\xa5\xd9\x86\xd9\x83\xd9\x84\xd9\x8a\xd8\xb2\xd9\x8a\xd8\xa9",
            ""
            ]

llog = [logger.debug,
       logger.info,
       logger.warning,
       logger.error,
       ]


for t in range(1):
    for lo in  vector:
        for ll in llog:
            s = "%s" % lo
            
            print s
            ll("%s" % s)
    print "%d" % t
    time.sleep(1)



