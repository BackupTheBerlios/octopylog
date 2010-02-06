# -*- coding: UTF-8 -*-

""" 
OctopyLog Project : 
"""

__author__      = "$Author: octopy $"
__version__     = "$Revision: 1.1 $"
__copyright__   = "Copyright 2009, The OctopyLog Project"
__license__     = "GPL"
__email__       = "octopy@gmail.com"



import wx

import network.oc_fifo as oc_fifo
import network.oc_message as oc_message



import oc_manager
import oc_logserver
import oc_designGUI

import logging.handlers







class MainFrame(oc_designGUI.oc_designGUI):
    def __init__(self, *args, **kwds):
        oc_designGUI.oc_designGUI.__init__(self, *args, **kwds)
        
        
        
        self.fifoManager = None
        self.ocManager = None
        self.ocLogserver = None
        
        self.Bind(wx.EVT_CLOSE,self.onDestroy)
        #self.Bind(wx.EVT_IDLE, self.on_idle)
        
        
        self.splitter.SetSashGravity(0.85) 
        #self.splitterLog.SetSashGravity(0.85)
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
        

    def on_idle(self, event):
        #self.ocManager.run_no_blocking()
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

    def OnSaveAs(self, event): 

       
        import os


        wildcard = "Txt file (*.txt)|*.txt|"     \
           "All files (*.*)|*.*"

        dlg = wx.FileDialog(
            self, message="Choose a file",
            #"defaultDir=os.getcwd(),
            defaultDir="",
            defaultFile="",
            wildcard=wildcard,
            style=wx.SAVE | wx.CHANGE_DIR
            )

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
        else :
            path = None
        dlg.Destroy()


        if path is not None :
            self.postManager("EXPORT.TXT", path)
        
        event.Skip()


    def onAbout(self, event): 
        from app import APP_NAME
        from app import APP_VERSION
        from wx.lib.wordwrap import wordwrap
        import platform

        description = "Octopylog is a sink for trace coming from different source\n"
        description += "\n WX-version : %s" % wx.VERSION_STRING
        description += "\n WX-plateform : %s" % wx.Platform
        description += "\n Python-version : %s" % platform.python_version()
        description += "\n Plateform : %s" % platform.platform(terse=True)
        description += "\n"
        
        info = wx.AboutDialogInfo()
        _icon = wx.EmptyIcon()
        _icon.CopyFromBitmap(wx.Bitmap("images/octopylog_logo.png", wx.BITMAP_TYPE_ANY))
        
        info.Icon = _icon 
        info.Name = APP_NAME
        info.Version = APP_VERSION
        info.Copyright = "GNU GENERAL PUBLIC LICENSE v3"
        info.Description = wordwrap(description, 350, wx.ClientDC(self))
        info.WebSite = ("http://developer.berlios.de/projects/octopylog/", "berlios home page")
        info.Developers = [ "Jean-Marc Beguinet" ]
        
        licenseText = "GNU GENERAL PUBLIC LICENSE v3\n"
        licenseText += "Please report to :\n"
        licenseText += "http://www.gnu.org/licenses/licenses.html"
        info.License = wordwrap(licenseText, 500, wx.ClientDC(self))

        wx.AboutBox(info)

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
        
        


        
        
        
        
        
        
        
        
        
        
        
        