# -*- coding: UTF-8 -*-
###########################################################
# Project  : Octopylog                                    #
# License  : GNU General Public License (GPL)             #
# Author   : JMB                                          #
# Date     : 11/01/09                                     #
###########################################################


__version__ = "$Revision: 1.5 $"
__author__ = "$Author: octopy $"



import wx

import wxcustom.oc_wxLogCtrl as oc_wxLogCtrl
import wxcustom.oc_wxDesCtrl as oc_wxDesCtrl



class oc_designGUI(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.splitterMain = wx.SplitterWindow(self, -1, style=wx.SP_3DBORDER|wx.SP_BORDER)
        self.windowMainDown = wx.Panel(self.splitterMain, -1, style=wx.NO_BORDER|wx.TAB_TRAVERSAL)
        self.windowMainUp = wx.Panel(self.splitterMain, -1)
        self.splitterLog = wx.SplitterWindow(self.windowMainUp, -1, style=wx.SP_3DBORDER|wx.SP_BORDER)
        self.windowLogDown = wx.Panel(self.splitterLog, -1)
        self.windowLogUp = wx.Panel(self.splitterLog, -1)
        
        # Menu Bar
        self.frameMain_menubar = wx.MenuBar()
        wxglade_tmp_menu = wx.Menu()
        wxglade_tmp_menu.Append(10100, "Quit", "", wx.ITEM_NORMAL)
        self.frameMain_menubar.Append(wxglade_tmp_menu, "File")
        wxglade_tmp_menu = wx.Menu()
        wxglade_tmp_menu.Append(10101, "About", "", wx.ITEM_NORMAL)
        self.frameMain_menubar.Append(wxglade_tmp_menu, "Help")
        self.SetMenuBar(self.frameMain_menubar)
        self.statusbar = self.CreateStatusBar(1, 0)
        
        # Tool Bar
        self.toolbar = wx.ToolBar(self, -1, style=wx.TB_HORIZONTAL|wx.TB_FLAT|wx.TB_DOCKABLE|wx.TB_NODIVIDER)
        self.SetToolBar(self.toolbar)
        self.toolbar.AddSeparator()
        self.toolbar.AddLabelTool(10050, "Start", wx.Bitmap("images/control_play_blue.png", wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, "Start Capture", "Start Capture")
        self.toolbar.AddLabelTool(10051, "Stop", wx.Bitmap("images/control_stop_blue.png", wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, "Stop Capture", "Stop Capture")
        self.toolbar.AddLabelTool(10052, "Clear", wx.Bitmap("images/application_delete.png", wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, "Clear Capture", "Clear Capture")
        self.toolbar.AddSeparator()
        self.toolbar.AddLabelTool(10060, "AutoScroll", wx.Bitmap("images/arrow_down.png", wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_CHECK, "Activate/Deactivate Autoscroll", "Activate/Deactivate Autoscroll")
        
        
        self.logCtrl = oc_wxLogCtrl.LogCtrl(self.windowLogUp, -1)
        self.desCtrl = oc_wxDesCtrl.DesCtrl(self.windowLogDown, -1)
        self.txtctrlLogApp = wx.TextCtrl(self.windowMainDown, -1, "", style=wx.TE_MULTILINE|wx.NO_BORDER)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_MENU, self.OnQuit, id=10100)
        self.Bind(wx.EVT_MENU, self.onAbout, id=10101)
        self.Bind(wx.EVT_TOOL, self.onStartCapture, id=10050)
        self.Bind(wx.EVT_TOOL, self.onStopCapture, id=10051)
        self.Bind(wx.EVT_TOOL, self.onClearCapture, id=10052)
        self.Bind(wx.EVT_TOOL, self.onAutoScroll, id=10060)
    

    def __set_properties(self):
        self.SetTitle("OctopyLog")
        _icon = wx.EmptyIcon()
        _icon.CopyFromBitmap(wx.Bitmap("images/octopylog_icone.png", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)
        self.statusbar.SetStatusWidths([-1])
        # statusbar fields
        statusbar_fields = ["frame_1_statusbar"]
        for i in range(len(statusbar_fields)):
            self.statusbar.SetStatusText(statusbar_fields[i], i)
        self.toolbar.SetToolBitmapSize((16, 16))
        self.toolbar.SetMargins((2, 2))
        self.toolbar.SetToolPacking(2)
        self.toolbar.SetToolSeparation(2)
        self.toolbar.Realize()
        
        
    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4.Add(self.logCtrl, 1, wx.EXPAND|wx.FIXED_MINSIZE, 0)
        self.windowLogUp.SetSizer(sizer_4)
        sizer_5.Add(self.desCtrl, 1, wx.EXPAND|wx.FIXED_MINSIZE, 0)
        self.windowLogDown.SetSizer(sizer_5)
        self.splitterLog.SplitHorizontally(self.windowLogUp, self.windowLogDown)
        sizer_3.Add(self.splitterLog, 1, wx.EXPAND, 0)
        self.windowMainUp.SetSizer(sizer_3)
        sizer_2.Add(self.txtctrlLogApp, 1, wx.EXPAND|wx.FIXED_MINSIZE, 0)
        self.windowMainDown.SetSizer(sizer_2)
        self.splitterMain.SplitHorizontally(self.windowMainUp, self.windowMainDown)
        sizer_1.Add(self.splitterMain, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
     

    def OnQuit(self, event): 
        print "Event handler `OnQuit' not implemented!"
        event.Skip()

    def onAbout(self, event):
        print "Event handler `onAbout' not implemented!"
        event.Skip()

    def onStartCapture(self, event):
        print "Event handler `onStartCapture' not implemented!"
        event.Skip()

    def onStopCapture(self, event): 
        print "Event handler `onStopCapture' not implemented!"
        event.Skip()

    def onClearCapture(self, event):
        print "Event handler `onClearCapture' not implemented!"
        event.Skip()

    def onAutoScroll(self, event): 
        print "Event handler `onAutoScroll' not implemented!"
        event.Skip()



