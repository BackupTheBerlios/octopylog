# -*- coding: UTF-8 -*-

""" 
OctopyLog Project : 
"""

__author__      = "$Author: octopy $"
__version__     = "$Revision: 1.10 $"
__copyright__   = "Copyright 2009, The OctopyLog Project"
__license__     = "GPL"
__email__       = "octopy@gmail.com"



import wx
import threading 

import network.oc_message as oc_message
import wxcustom.oc_wxLogCtrl as oc_wxLogCtrl
# create message


oc_message.addMessageType("LOG.RAW")


oc_message.addMessageType("LOGCTRL.AUTOSCROLL")
oc_message.addMessageType("LOGCTRL.CLEAR")
oc_message.addMessageType("LOGCTRL.WRITEFILE")




# connection
oc_message.addMessageType("CONNECTION.INFO")
oc_message.addMessageType("CONNECTION.CLOSE")

oc_message.addMessageType("CONNECTION.STARTCAPTURE")
oc_message.addMessageType("CONNECTION.STOPCAPTURE")


# general application log
oc_message.addMessageType("APP.LOG")
oc_message.addMessageType("APP.CRITICALERROR")
oc_message.addMessageType("APP.DROPFIFO")

oc_message.addMessageType("PARSEUR.ITEM")


class Manager:
    """ """

    def __init__(self, fifoIn, gui_logctrl, gui_int, gui_des):
        
        self.fifoIn             = fifoIn 
        self._wxLogCtrl_log     = gui_logctrl
        self._wxTextCtrl_Int    = gui_int
        self._wxDesCtrl_Des     = gui_des       
     
        self.finished = threading.Event()
        self.thd = None
        
        # event => callback
        self._dispatch = {}
        self._dispatch[ oc_message.getId("LOG.RAW") ]              = self.logRaw
        self._dispatch[ oc_message.getId("LOGCTRL.AUTOSCROLL") ]   = self.logctrlAutoscroll
        self._dispatch[ oc_message.getId("LOGCTRL.CLEAR") ]        = self.logctrlClear
        self._dispatch[ oc_message.getId("LOGCTRL.WRITEFILE") ]    = self.logctrlWriteFile
        self._dispatch[ oc_message.getId("CONNECTION.INFO") ]      = self.connectionInfo
        self._dispatch[ oc_message.getId("CONNECTION.CLOSE") ]     = self.connectionClose
        self._dispatch[ oc_message.getId("APP.LOG") ]              = self.appLog
        self._dispatch[ oc_message.getId("APP.CRITICALERROR") ]    = self.appCriticalError
        self._dispatch[ oc_message.getId("APP.DROPFIFO") ]         = self.appDropFifo
        
        self._dispatch[ oc_message.getId("PARSEUR.ITEM") ]         = self.parseurItem
        
        
        # wx.log
        self.wxLogTextCtrl = wx.LogTextCtrl(self._wxTextCtrl_Int)
        self.wxLogTextCtrl.AddTraceMask("general")
        wx.Log_SetActiveTarget(self.wxLogTextCtrl)
        wx.Log_SetVerbose()

    
    def parseurItem(self, param):
        pass
        #self._wxDesCtrl_Des.parse_item(param)
    
    
     
    def logRaw(self, param):
        
        
        try :
            lst = []
            lst.append(param["connectionID"].__str__())
            lst.append(param["name"])
            lst.append(param["msg"].encode("utf-8"))
            lst.append(param["funcName"])
            evt = oc_wxLogCtrl.EventMsgLogCtrl(lst)
            self._wxLogCtrl_log.AddPendingEvent(evt)            
            
        except Exception, ex:
            print "Drop one raw : %s" % ex.__str__()

     
    def connectionInfo(self, param):
        # use Application log
        self.appLog(param)
        
    def connectionClose(self, param):
        pass
        
    
    def appLog(self, param):
        """ Application log view """
        wx.LogMessage(param)
     
    def appCriticalError(self, param):
        self.appLog("Critical Error for application")
        self.appLog("ToDo : add a debug trace system")
        
    def appDropFifo(self, param):
        self.appLog("FIFO full, one item was lost in : %s" % param)
        
    def logctrlClear(self, param):
        self.appLog("Clear Log")
        self._wxLogCtrl_log.clear()
        self._wxDesCtrl_Des.clear_view()
    

    def logctrlAutoscroll(self, param):
        self.appLog("Autoscroll=%s" % param)
        self._wxLogCtrl_log.setAutoscroll(param)

    
    def logctrlWriteFile(self, param):
        pass
        
    def initView(self):
        # wxLogCtrl_log
        lst = ["connectionID","name","msg","function"]
        self._wxLogCtrl_log.setHeader(lst)
        

    def stop(self):
        print "try to stop oc_manager"
        self.finished.set()
        self.fifoIn.unblock()
        self.thd.join()
                
    def start(self):
        self.thd = threading.Thread(target=self.run,  name="AppControler")
        self.thd.start()
    
    def run(self):
        while not self.finished.isSet():
            item = self.fifoIn.getitem(True, None)
            if item is not None :
                self._dispatch[item.type](item.obj)
            else:
                break
        print "exit run oc_manager"
    
    def run_no_blocking(self):
        for i in range(10):
            item = self.fifoIn.getitem(False, 0)
            if item is not None :
                self._dispatch[item.type](item.obj)
            else :
                break
        
        
        
        







if __name__ == '__main__':
    
    
    pass






