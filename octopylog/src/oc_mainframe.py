# -*- coding: UTF-8 -*-

""" 
OctopyLog Project : 
"""

__author__      = "$Author: octopy $"
__version__     = "$Revision: 1.7 $"
__copyright__   = "Copyright 2009, The OctopyLog Project"
__license__     = "GPL"
__email__       = "octopy@gmail.com"



import wx

import network.oc_fifo as oc_fifo
import network.oc_message as oc_message



import oc_manager
import oc_logserver
import oc_designGUI
import oc_aboutdlg

import logging.handlers





class MainFrame(oc_designGUI.oc_designGUI):
    def __init__(self, *args, **kwds):
        oc_designGUI.oc_designGUI.__init__(self, *args, **kwds)
        
        
        
        self.fifoManager = None
        self.ocManager = None
        self.ocLogserver = None
        
        self.Bind(wx.EVT_CLOSE,self.onDestroy)
        
        
        self.splitterMain.SetSashGravity(0.85) 
        self.splitterLog.SetSashGravity(0.85)
        self.SetSize(wx.Size(700, 600))
        

        self.statusbar.SetStatusText("", 0)        
        
        # Event of App Init
        self.onInit()
        
        
    def onInit(self):
    
        self.startManager()
        
        # activate trace by default
        self.ocLogserver.startLog()
        
  
        
    def onDestroy(self, event):
        self.stopManager()
        event.Skip()
        
        
    def OnQuit(self, event): 
        self.Close()
        event.Skip()
        



    def onAutoScroll(self, event):
        val = self.toolbar.GetToolState(event.GetId())
        self.postManager("LOGCTRL.AUTOSCROLL", val)
        event.Skip()

    def onStartCapture(self, event): 
        self.ocLogserver.startLog()
        event.Skip()

    def onStopCapture(self, event): 
        self.ocLogserver.stopLog()
        event.Skip()
        
    def onClearCapture(self, event): 
        self.postManager("LOGCTRL.CLEAR", None)
        event.Skip()

    def onAbout(self, event): 
        about = oc_aboutdlg.About(self, -1, "")
        about.ShowModal()
        event.Skip()


    def postManager(self, typename, param):
        oc_message.postMessage(self.fifoManager, typename, param)

    
    def startManager(self):
        # create fifo
        self.fifoManager = oc_fifo.Fifo(128)
        # Create Manager
        self.ocManager = oc_manager.Manager(self.fifoManager, self.logCtrl, self.txtctrlLogApp, self.desCtrl )
        self.ocManager.initView()
        self.ocManager.start()
        # Create logserver
        self.ocLogserver = oc_logserver.Logserver(self.fifoManager, self.fifoManager, \
                                                  "localhost", logging.handlers.DEFAULT_TCP_LOGGING_PORT, 5)
        self.ocLogserver.start()             
    
        self.logCtrl.fifoManager = self.fifoManager
    
    
    def stopManager(self):
        self.ocManager.stop()
        self.ocLogserver.stop()
        
        


        
        
        
        
        
        
        
        
        
        
        
        