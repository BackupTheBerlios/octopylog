# -*- coding: UTF-8 -*-
###########################################################
# Project  : Octopylog                                    #
# License  : GNU General Public License (GPL)             #
# Author   : JMB                                          #
# Date     : 21/10/08                                     #
###########################################################


__version__ = "$Revision: 1.1 $"
__author__ = "$Author: octopy $"


import logging.handlers
import threading

import fifo   
import server
import message



class ConnectionManager(server.ConnectionManagerBase):
    
    def __init__(self, maxconnection, fifo_log, fifo_event ):
        server.ConnectionManagerBase.__init__(self, maxconnection)
        self.fifo_log   = fifo_log
        self.fifo_event = fifo_event
    
    
    def evtConnection(self, id):
        message.postMessage(self.fifo_event,"CONNECTION.INFO", "Connection id:%04d"%id)
        
    def evtDisconnection(self, id):
        message.postMessage(self.fifo_event,"CONNECTION.INFO", "Disconnection id:%04d"%id)
    
    def evtReject(self):
        message.postMessage(self.fifo_event,"CONNECTION.INFO", "Connection rejected")
            
        
    def evtReceived(self, id, obj):
        obj["connectionID"] = id
        try:
            self._fifo_trace.putitem(obj)
        except fifo.Overrun, ex:
            pass
 
