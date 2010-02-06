# -*- coding: UTF-8 -*-

""" 
OctopyLog Project : 
"""

__author__      = "$Author: octopy $"
__version__     = "$Revision: 1.1 $"
__copyright__   = "Copyright 2009, The OctopyLog Project"
__license__     = "GPL"
__email__       = "octopy@gmail.com"



import logging.handlers
import threading

import network.oc_fifo  as oc_fifo   
import network.oc_server as oc_server
import network.oc_message as oc_message



class ConnectionManager(oc_server.ConnectionManagerBase):
    
    def __init__(self, maxconnection, fifoLog, fifoEvent ):
        oc_server.ConnectionManagerBase.__init__(self, maxconnection)
        self.fifoLog   = fifoLog
        self.fifoEvent = fifoEvent
        
        self.ctrlEvtReveived = threading.Event()   
    
    
    def enableEvtReveived(self):
        oc_message.postMessage(self.fifoEvent,"CONNECTION.INFO", "Enable Log event from connection(s)") 
        self.ctrlEvtReveived.set()
    
    def disableEvtReceived(self):
        oc_message.postMessage(self.fifoEvent,"CONNECTION.INFO", "Disable Log event from connection(s)") 
        self.ctrlEvtReveived.clear()

    
    def evtConnection(self, id):
        t = self.getConnectionInfo(id)
        oc_message.postMessage(self.fifoEvent,"CONNECTION.INFO", "Connection id:%04d from %s" % (id,t))
        
        
        obj = {}
        obj["connectionID"] = ""
        obj["name"] = "Octopylog"
        obj["msg"] = "Connection id:%04d from %s" % (id,t)
        obj["funcName"] = ""
        oc_message.postMessage(self.fifoLog,"LOG.RAW", obj) 
        
        
    def evtDisconnection(self, id):
        oc_message.postMessage(self.fifoEvent,"CONNECTION.INFO", "Disconnection id:%04d" % id)
        
        obj = {}
        obj["connectionID"] = ""
        obj["name"] = "Octopylog"
        obj["msg"] = "Disconnection id:%04d" % id
        obj["funcName"] = ""
        oc_message.postMessage(self.fifoLog,"LOG.RAW", obj) 
    
    def evtReject(self):
        oc_message.postMessage(self.fifoEvent,"CONNECTION.INFO", "Connection rejected")
            
    def evtReceived(self, id, obj):
        if self.ctrlEvtReveived.isSet():
            obj["connectionID"] = id
            try:
                #self.fifoLog.putitem(obj)
                oc_message.postMessage(self.fifoLog,"LOG.RAW", obj)   
            except oc_fifo.Overrun:
                oc_message.postMessage(self.fifoEvent,"APP.DROPFIFO", "Fifo log")
            
 
 
 
class Logserver:
    
    def __init__(self, fifo_log, fifo_event, host, port, maxconnection): 
        self.connnection = ConnectionManager(maxconnection, fifo_log, fifo_event)
        self.server = oc_server.createServer(self.connnection, host, port)
    
    def start(self):
        self.server.start()
    
    def stop(self):
        self.server.stop()
        self.connnection.closeAll()
        
        
    def startLog(self):
        """ """
        self.connnection.enableEvtReveived()
        
    def stopLog(self):
        self.connnection.disableEvtReceived()
        
        
    
    
    
    
    
    
    
    
    
