# -*- coding: UTF-8 -*-

""" 
OctopyLog Project : 
"""

__author__      = "$Author: octopy $"
__version__     = "$Revision: 1.9 $"
__copyright__   = "Copyright 2009, The OctopyLog Project"
__license__     = "GPL"
__email__       = "octopy@gmail.com"




import wx

import wxcustom.oc_wxLogCtrl as oc_wxLogCtrl
import wxcustom.oc_wxDesCtrl as oc_wxDesCtrl




ID_MENU_SAVEAS = wx.NewId()
ID_MENU_LOAD = wx.NewId()
ID_MENU_QUIT = wx.NewId()
ID_MENU_ABOUT = wx.NewId()

ID_TOOLBAR_LOAD = wx.NewId()
ID_TOOLBAR_SAVEAS = wx.NewId()
ID_TOOLBAR_START = wx.NewId()
ID_TOOLBAR_STOP = wx.NewId()
ID_TOOLBAR_CLEAR = wx.NewId()
ID_TOOLBAR_AUTOSCROLL = wx.NewId()



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
        # File
        tmp_menu = wx.Menu()      
        tmp_menu.Append(ID_MENU_SAVEAS, "Save As ...", "", wx.ITEM_NORMAL)
        tmp_menu.Append(ID_MENU_LOAD, "Load", "", wx.ITEM_NORMAL)
        tmp_menu.Append(ID_MENU_QUIT, "Quit", "", wx.ITEM_NORMAL)
        self.Bind(wx.EVT_MENU, self.OnSaveAs, id=ID_MENU_SAVEAS)
        self.Bind(wx.EVT_MENU, self.OnLoad, id=ID_MENU_LOAD)
        self.Bind(wx.EVT_MENU, self.OnQuit, id=ID_MENU_QUIT)
        
        self.frameMain_menubar.Append(tmp_menu, "File")
        # About
        tmp_menu = wx.Menu()
        tmp_menu.Append(ID_MENU_ABOUT, "About", "", wx.ITEM_NORMAL)
        self.Bind(wx.EVT_MENU, self.onAbout, id=ID_MENU_ABOUT)
        self.frameMain_menubar.Append(tmp_menu, "Help")
        self.SetMenuBar(self.frameMain_menubar)
        self.statusbar = self.CreateStatusBar(1, 0)
        
        # Tool Bar
        self.toolbar = wx.ToolBar(self, -1, style=wx.TB_HORIZONTAL|wx.TB_FLAT|wx.TB_DOCKABLE|wx.TB_NODIVIDER)
        self.SetToolBar(self.toolbar)
        self.toolbar.AddSeparator()
        self.toolbar.AddLabelTool(ID_TOOLBAR_LOAD     , "Load",    wx.Bitmap("images/page_white_database.png",\
                                        wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL,\
                                        "Load", "Load a Capture")
        self.toolbar.AddLabelTool(ID_TOOLBAR_SAVEAS, "Save As..", wx.Bitmap("images/page_save.png",\
                                        wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL,\
                                         "Save As...", "Save As capture") 
        self.toolbar.AddSeparator()                
        
        self.toolbar.AddLabelTool(ID_TOOLBAR_START, "Start",   wx.Bitmap("images/control_play_blue.png",\
                                        wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL,\
                                        "Start Capture", "Start Capture")
        self.toolbar.AddLabelTool(ID_TOOLBAR_STOP, "Stop",    wx.Bitmap("images/control_stop_blue.png",\
                                        wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL,\
                                        "Stop Capture", "Stop Capture")
        self.toolbar.AddLabelTool(ID_TOOLBAR_CLEAR, "Clear", wx.Bitmap("images/table_delete.png",\
                                        wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL,\
                                        "Clear Capture", "Clear Capture")


        self.toolbar.AddSeparator()
        self.toolbar.AddLabelTool(ID_TOOLBAR_AUTOSCROLL, "AutoScroll", wx.Bitmap("images/arrow_down.png", wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_CHECK, "Activate/Deactivate Autoscroll", "Activate/Deactivate Autoscroll")
        
        
        self.logCtrl = oc_wxLogCtrl.LogCtrl(self.windowLogUp, -1)
        self.desCtrl = oc_wxDesCtrl.DesCtrl(self.windowLogDown, -1)
        self.txtctrlLogApp = wx.TextCtrl(self.windowMainDown, -1, "", style=wx.TE_MULTILINE|wx.NO_BORDER)

        self.__set_properties()
        self.__do_layout()



        self.Bind(wx.EVT_TOOL, self.OnLoad, id=ID_TOOLBAR_LOAD)
        self.Bind(wx.EVT_TOOL, self.OnSaveAs,  id=ID_TOOLBAR_SAVEAS)
        
        
        self.Bind(wx.EVT_TOOL, self.onStartCapture, id=ID_TOOLBAR_START)
        self.Bind(wx.EVT_TOOL, self.onStopCapture,  id=ID_TOOLBAR_STOP)
        self.Bind(wx.EVT_TOOL, self.onClearCapture, id=ID_TOOLBAR_CLEAR)
        self.Bind(wx.EVT_TOOL, self.onAutoScroll,   id=ID_TOOLBAR_AUTOSCROLL)
    

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
     


    def OnSaveAs(self, event): 
        print "Event handler `OnSaveAs' not implemented!"
        event.Skip()

    def OnLoad(self, event): 
        print "Event handler `Load' not implemented!"
        event.Skip()

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



