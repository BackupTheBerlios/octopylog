# -*- coding: UTF-8 -*-
###########################################################
# Project  : Octopylog                                    #
# License  : GNU General Public License (GPL)             #
# Author   : JMB                                          #
# Date     : 21/10/08                                     #
###########################################################


__version__ = "$Revision: 1.5 $"
__author__ = "$Author: octopy $"



import wx
import threading 

import network.oc_message as oc_message

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



class Manager:
    """ """

    def __init__(self, fifoIn, gui_logctrl, gui_int):
        
        self.fifoIn             = fifoIn 
        self._wxLogCtrl_log     = gui_logctrl
        self._wxTextCtrl_Int    = gui_int
               
     
        self._finished = threading.Event()
        
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
        
        # wx.log
        self.wxLogTextCtrl = wx.LogTextCtrl(self._wxTextCtrl_Int)
        self.wxLogTextCtrl.AddTraceMask("general")
        wx.Log_SetActiveTarget(self.wxLogTextCtrl)
        wx.Log_SetVerbose()

    
     
    def logRaw(self, param):
        lst = []
        lst.append(param["connectionID"].__str__())
        lst.append(param["name"].__str__())
        lst.append(param["msg"].__str__())
        self._wxLogCtrl_log.addLogItem(lst)       
     
     
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
    

    def logctrlAutoscroll(self, param):
        self.appLog("Autoscroll=%s" % param)
        self._wxLogCtrl_log.setAutoscroll(param)

    
    def logctrlWriteFile(self, param):
        #self.
        pass
        
    def initView(self):
        # wxLogCtrl_log
        lst = ["connectionID","name","msg"]
        self._wxLogCtrl_log.setHeader(lst)
        

    def stop(self):
        self._finished.set()
        self.fifoIn.unblock()
        self._th.join()
                
    def start(self):
        self._th = threading.Thread(target=self.run,  name="AppControler")
        self._th.start()
    
    def run(self):
        while not self._finished.isSet():
            item = self.fifoIn.getitem(True, None)
            if item is not None :
                self._dispatch[item.type](item.obj)
            else:
                return
        







if __name__ == '__main__':
    
    
    pass






