# -*- coding: UTF-8 -*-
###########################################################
# Project  : Octopylog                                    #
# License  : GNU General Public License (GPL)             #
# Author   : JMB                                          #
# Date     : 21/10/08                                     #
###########################################################


__version__ = "$Revision: 1.1 $"
__author__ = "$Author: octopy $"


import wx

import network.oc_fifo as oc_fifo
import network.oc_message as oc_message
import wxcustom.oc_wxLogCtrl as oc_wxLogCtrl


import oc_manager
import oc_logserver
import oc_designGUI

import logging.handlers





class MainFrame(oc_designGUI.oc_designGUI):
    def __init__(self, *args, **kwds):
        oc_designGUI.oc_designGUI.__init__(self, *args, **kwds)
        
        
        self.Bind(wx.EVT_CLOSE,self.onDestroy)
        
        # Event of App Init
        self.onInit()
        
        
    def onInit(self):
        self.startManager()
        
  
        
    def onDestroy(self, event):
        self.stopManager()
        event.Skip()


    def onAutoScroll(self, event):
        val = self.toolbar.GetToolState(event.GetId())
        self.postManager("LOGCTRL.AUTOSCROLL", val)
        event.Skip()




    def postManager(self, typename, param):
        oc_message.postMessage(self.fifoManager, typename, param)

    
    def startManager(self):
        # create fifo
        self.fifoManager = oc_fifo.Fifo(128)
        # Create Manager
        self.ocManager = oc_manager.Manager(self.fifoManager, self.logCtrl, self.txtctrlLogApp )
        self.ocManager.initView()
        self.ocManager.start()
        # Create logserver
        self.ocLogserver = oc_logserver.Logserver( self.fifoManager, self.fifoManager,"localhost", logging.handlers.DEFAULT_TCP_LOGGING_PORT,5)
        self.ocLogserver.start()             
    
    def stopManager(self):
        self.ocLogserver.stop()
        self.ocManager.stop()
        pass
        


        
        
        
        
        
        
        
        
        
        
        
        