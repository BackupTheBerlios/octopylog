# -*- coding: UTF-8 -*-
###########################################################
# Project  : Octopylog                                    #
# License  : GNU General Public License (GPL)             #
# Author   : JMB                                          #
# Date     : 21/10/08                                     #
###########################################################


__version__ = "$Revision: 1.1 $"
__author__ = "$Author: octopy $"

import network.message as message


# create message


# message for logctrl 
message.addMessageType("LOGCTRL.AUTOSCROLL")
message.addMessageType("LOGCTRL.CLEAR")
message.addMessageType("LOGCTRL.LOGITEM")
message.addMessageType("LOGCTRL.WRITEFILE")

# connection
message.addMessageType("CONNECTION.INFO")
message.addMessageType("CONNECTION.CLOSE")

# general application log
message.addMessageType("APP.LOG")
message.addMessageType("APP.CRITICALERROR")


class Manager:
    """ """
    def __init__(self, fifo_in, gui_logctrl, gui_int):
        
        self._fifo_in           = fifo_in 
        self._wxLogCtrl_log     = gui_logctrl
        self._wxTextCtrl_Int    = gui_int
               
        
        self._finished = threading.Event()
        
        # event => callback
        self._dispatch = {}
        self._dispatch[ message.getId("LOGCTRL.AUTOSCROLL") ]   = self._logctrlAutoscroll
        self._dispatch[ message.getId("LOGCTRL.CLEAR") ]        = self._logctrlClear
        self._dispatch[ message.getId("LOGCTRL.LOGITEM") ]      = self._logctrlLogItem
        self._dispatch[ message.getId("LOGCTRL.WRITEFILE") ]    = self._logctrlWriteFile

        self._dispatch[ message.getId("CONNECTION.INFO") ]      = self._connectionInfo
        self._dispatch[ message.getId("CONNECTION.CLOSE") ]     = self._connectionClose

        self._dispatch[ message.getId("APP.LOG") ]              = self._appLog
        self._dispatch[ message.getId("APP.CRITICALERROR") ]    = self._appCriticalError
     
     
     
    def _connectionInfo(self, param):
        # use Application log
        self._appLog(param)
        
    
    def _appLog(self, param):
        """ Application log view """
        self._wxTextCtrl_Int.AppendText(param.__str__())
     
    def _appCriticalError(self, param):
        self._appLog("Critical Error for application")
        self._appLog("ToDo : add a debug trace system")
        
        
        
    def _logctrlClear(self, param):
        #self._wxLogCtrl_log
        pass
    
    def _logctrlLogItem(self, param):
        lst = []
        lst.append(param.connectionID.__str__())
        lst.append(param.name.__str__())
        lst.append(param.msg.__str__())
        self._wxLogCtrl_log.addLogItem(lst)
        
    
    def _logctrlWriteFile(self, param):
        #self.
        pass
        
    def initView(self):
        # wxLogCtrl_log
        lst = ["connectionID","name","msg"]
        self._wxLogCtrl_log.setHeader(lst)
        

    def stop(self):
        self._finished.set()
        self._event.unblock()
        self._th.join()
                
    def start(self):
        self._th = threading.Thread(target=self.run,  name="AppControler")
        self._th.start()
    
    def run(self):
        while not self._finished.isSet():
            item = self._fifo_in.getitem(True, None)
            if item is not None :
                self._dispatch[item.type](item.obj)




if __name__ == '__main__':
    
    
    pass






