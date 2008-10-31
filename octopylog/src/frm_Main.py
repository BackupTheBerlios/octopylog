# -*- coding: UTF-8 -*-
###########################################################
# Project  : Octopylog                                    #
# License  : GNU General Public License (GPL)             #
# Author   : JMB                                          #
# Date     : 21/10/08                                     #
###########################################################


__version__ = "$Revision: 1.2 $"
__author__ = "$Author: octopy $"

import wx

import network.oc_fifo as oc_fifo
import network.oc_message as oc_message
import wxcustom.oc_wxLogCtrl as oc_wxLogCtrl


import oc_manager
import oc_logserver


import logging.handlers



[ID_MENU_NEW,ID_MENU_OPEN,ID_MENU_SAVE,ID_MENU_PRINT,ID_MENU_QUIT,ID_MENU_CUT,\
ID_MENU_COPY,ID_MENU_PASTE,ID_MENU_HELP,ID_MENU_About,ID_TOOL_START_CAPTURE,ID_TOOL_STOP,\
ID_TOOL_AUTOSCROLL] = 6,7,8,9,10,11,12,13,15,16,10052,10053,10051



class frm_Main(wx.Frame):
    def __init__(self,parent,id = -1,title='',pos = wx.Point(1,1),size = wx.Size(495,420),style = wx.DEFAULT_FRAME_STYLE,name = 'frame'):
        pre=wx.PreFrame()
        self.OnPreCreate()
        pre.Create(parent,id,title,pos,size,style,name)
        self.PostCreate(pre)
        self.initBefore()
        self.VwXinit()
        self.initAfter()

    def __del__(self):
        self.Ddel()
        return


    def VwXinit(self):
        #self.SetIcon(wx.Icon("images/arrow_in.png",wx.BITMAP_TYPE_PNG));
        self.SetIcon(wx.Icon("images/octopussy.png",wx.BITMAP_TYPE_PNG));
        
        self.SetTitle('PyTrace')
        self.Show(False)
        self.MainFrameStBar = self.CreateStatusBar(1,wx.ST_SIZEGRIP)
        self.MainFrameStBar.SetStatusWidths([-1])
        self.MainFrameStBar.SetStatusText('',0)
        self.Bind(wx.EVT_SIZING,self.VwXEvOnSizing)
        self.MenuBar= wx.MenuBar()
        self.menuFile = wx.Menu()
        self.MenuBar.Append(self.menuFile,"File")
        self.menuEdit = wx.Menu()
        self.MenuBar.Append(self.menuEdit,"Edit")
        self.menuHelp = wx.Menu()
        self.MenuBar.Append(self.menuHelp,"Help")
        itemmenu = wx.MenuItem(self.menuFile,ID_MENU_NEW,"New","New File",wx.ITEM_NORMAL)
        itemmenu.SetBitmaps(wx.Bitmap("images/new.xpm",wx.BITMAP_TYPE_XPM),wx.NullBitmap)
        self.menuFile.AppendItem(itemmenu)
        itemmenu = wx.MenuItem(self.menuFile,ID_MENU_OPEN,"Open\tCtrl+F12","Open File",wx.ITEM_NORMAL)
        itemmenu.SetBitmaps(wx.Bitmap("images/open.xpm",wx.BITMAP_TYPE_XPM),wx.NullBitmap)
        self.menuFile.AppendItem(itemmenu)
        itemmenu = wx.MenuItem(self.menuFile,ID_MENU_SAVE,"Save\tShift+F12","Save File",wx.ITEM_NORMAL)
        itemmenu.SetBitmaps(wx.Bitmap("images/save.xpm",wx.BITMAP_TYPE_XPM),wx.NullBitmap)
        self.menuFile.AppendItem(itemmenu)
        self.menuFile.AppendSeparator()
        itemmenu = wx.MenuItem(self.menuFile,ID_MENU_PRINT,"Print","Print",wx.ITEM_NORMAL)
        itemmenu.SetBitmaps(wx.Bitmap("images/print.xpm",wx.BITMAP_TYPE_XPM),wx.NullBitmap)
        self.menuFile.AppendItem(itemmenu)
        self.menuFile.AppendSeparator()
        itemmenu = wx.MenuItem(self.menuFile,ID_MENU_QUIT,"Exit","Exit",wx.ITEM_NORMAL)
        self.menuFile.AppendItem(itemmenu)
        itemmenu = wx.MenuItem(self.menuEdit,ID_MENU_CUT,"Cut\tCtrl+X","",wx.ITEM_NORMAL)
        itemmenu.SetBitmaps(wx.Bitmap("images/cut.xpm",wx.BITMAP_TYPE_XPM),wx.NullBitmap)
        self.menuEdit.AppendItem(itemmenu)
        itemmenu = wx.MenuItem(self.menuEdit,ID_MENU_COPY,"Copy\tCtrl+C","",wx.ITEM_NORMAL)
        itemmenu.SetBitmaps(wx.Bitmap("images/copy.xpm",wx.BITMAP_TYPE_XPM),wx.NullBitmap)
        self.menuEdit.AppendItem(itemmenu)
        itemmenu = wx.MenuItem(self.menuEdit,ID_MENU_PASTE,"Paste\tCtrl+V","",wx.ITEM_NORMAL)
        itemmenu.SetBitmaps(wx.Bitmap("images/paste.xpm",wx.BITMAP_TYPE_XPM),wx.NullBitmap)
        self.menuEdit.AppendItem(itemmenu)
        itemmenu = wx.MenuItem(self.menuHelp,ID_MENU_HELP,"Help\tF1","",wx.ITEM_NORMAL)
        itemmenu.SetBitmaps(wx.Bitmap("images/help.xpm",wx.BITMAP_TYPE_XPM),wx.NullBitmap)
        self.menuHelp.AppendItem(itemmenu)
        self.menuHelp.AppendSeparator()
        itemmenu = wx.MenuItem(self.menuHelp,ID_MENU_About,"About","",wx.ITEM_NORMAL)
        self.menuHelp.AppendItem(itemmenu)
        self.SetMenuBar(self.MenuBar)
        self.Bind(wx.EVT_MENU,self.OnMenuSave,id=ID_MENU_SAVE)
        self.Bind(wx.EVT_MENU,self.OnMenuPrint,id=ID_MENU_PRINT)
        self.Bind(wx.EVT_MENU,self.OnMenuPaste,id=ID_MENU_PASTE)
        self.Bind(wx.EVT_MENU,self.OnMenuNew,id=ID_MENU_NEW)
        self.Bind(wx.EVT_MENU,self.OnMenuHelp,id=ID_MENU_HELP)
        self.Bind(wx.EVT_MENU,self.OnMenuExit,id=ID_MENU_QUIT)
        self.Bind(wx.EVT_MENU,self.OnMenuCut,id=ID_MENU_CUT)
        self.Bind(wx.EVT_MENU,self.OnMenuCopy,id=ID_MENU_COPY)
        self.Bind(wx.EVT_MENU,self.OnMenuAbout,id=ID_MENU_About)
        
        
        self.Bind(wx.EVT_CLOSE,self.Destroy)
         
        self.wxToolBar_main = wx.ToolBar(self,-1,wx.Point(30,60),wx.Size(489,27))

        self.SetToolBar(self.wxToolBar_main)
        self.wxToolBar_main.SetMargins((2,-1))
        self.wxToolBar_main.AddLabelTool(ID_TOOL_START_CAPTURE,"",wx.Bitmap("images/control_play_blue.png",wx.BITMAP_TYPE_PNG),wx.NullBitmap,wx.ITEM_NORMAL,"Start Capture","Start Capture")
        self.Bind(wx.EVT_TOOL,self.Tool2c_VwXEvOnTool,id=ID_TOOL_START_CAPTURE)
        self.wxToolBar_main.AddLabelTool(ID_TOOL_STOP,"",wx.Bitmap("images/control_stop_blue.png",wx.BITMAP_TYPE_PNG),wx.NullBitmap,wx.ITEM_NORMAL,"Stop Capture","Stop Capture")
        self.Bind(wx.EVT_TOOL,self.Tool3c_VwXEvOnTool,id=ID_TOOL_STOP)
        self.wxToolBar_main.AddSeparator()
        self.wxToolBar_main.AddLabelTool(ID_TOOL_AUTOSCROLL,"",wx.Bitmap("images/arrow_down.png",wx.BITMAP_TYPE_PNG),wx.NullBitmap,wx.ITEM_CHECK,"Active/Desactivate AutoScroll","Active/Desactivate AutoScroll")
        self.Bind(wx.EVT_TOOL,self.Tool_AutoScroll,id=ID_TOOL_AUTOSCROLL)
        self.wxSplitter_Main = wx.SplitterWindow(self,-1,wx.Point(0,0),wx.Size(20,20))
        self.pn130c = wx.Panel(self.wxSplitter_Main,-1,wx.Point(2,2),wx.Size(485,137))
        self.pn131c = wx.Panel(self.wxSplitter_Main,-1,wx.Point(0,0),wx.Size(20,20))
        self.txm134c = wx.TextCtrl(self.pn131c,-1,"",wx.Point(0,0),wx.Size(100,60),wx.TE_MULTILINE)
        self.wxSplitter_Log = wx.SplitterWindow(self.pn130c,-1,wx.Point(0,0),wx.Size(20,20))
        self.pn136c = wx.Panel(self.wxSplitter_Log,-1,wx.Point(0,0),wx.Size(483,106))
        self.pn137c = wx.Panel(self.wxSplitter_Log,-1,wx.Point(0,109),wx.Size(477,97))
        self.txm140c = wx.TextCtrl(self.pn137c,-1,"",wx.Point(0,0),wx.Size(100,60),wx.TE_MULTILINE)
        self.wxLogCtrl = oc_wxLogCtrl.LogCtrl(self.pn136c,-1,wx.Point(0,0),wx.Size(20,20))
        self.wxToolBar_main.Realize()
        self.wxSplitter_Main.SplitHorizontally(self.pn130c,self.pn131c)
        self.wxSplitter_Main.SetMinimumPaneSize(3)
        self.wxSplitter_Main.SetSplitMode(1)
        self.wxSplitter_Main.SetSashPosition(259)
        self.wxSplitter_Log.SplitHorizontally(self.pn136c,self.pn137c)
        self.wxSplitter_Log.SetMinimumPaneSize(2)
        self.wxSplitter_Log.SetSplitMode(1)
        self.wxSplitter_Log.SetSashPosition(153)

        self.sz70s = wx.BoxSizer(wx.VERTICAL)
        self.sz132s = wx.BoxSizer(wx.HORIZONTAL)
        self.sz133s = wx.BoxSizer(wx.HORIZONTAL)
        self.sz138s = wx.BoxSizer(wx.HORIZONTAL)
        self.sz139s = wx.BoxSizer(wx.HORIZONTAL)
        self.sz70s.Add(self.wxSplitter_Main,1,wx.ALIGN_CENTER|wx.EXPAND|wx.FIXED_MINSIZE,3)
        self.sz132s.Add(self.txm134c,1,wx.EXPAND|wx.FIXED_MINSIZE,3)
        self.sz133s.Add(self.wxSplitter_Log,1,wx.EXPAND|wx.FIXED_MINSIZE,3)
        self.sz138s.Add(self.txm140c,1,wx.EXPAND|wx.FIXED_MINSIZE,3)
        self.sz139s.Add(self.wxLogCtrl,1,wx.EXPAND|wx.FIXED_MINSIZE,3)
        self.SetSizer(self.sz70s);self.SetAutoLayout(1);self.Layout();
        self.pn131c.SetSizer(self.sz132s);self.pn131c.SetAutoLayout(1);self.pn131c.Layout();
        self.pn130c.SetSizer(self.sz133s);self.pn130c.SetAutoLayout(1);self.pn130c.Layout();
        self.pn137c.SetSizer(self.sz138s);self.pn137c.SetAutoLayout(1);self.pn137c.Layout();
        self.pn136c.SetSizer(self.sz139s);self.pn136c.SetAutoLayout(1);self.pn136c.Layout();
        self.Refresh()
        return
    def VwXDelComp(self):
        return
    
    
    def Destroy(self,event): #init function
        #[ b9]Code event VwX...Don't modify[ b9]#
        #add your code here
        self.stopManager()
        
        event.Skip()
        return #end function
    
    def VwXEvOnSizingAll(self,event): #init function
        #add your code here

        return True;
        #end function

    def VwXEvOnSizing(self,event): #init function
        #[64f]Code event VwX...Don't modify[64f]#
        #add your code here
        event.Skip()
        return #end function

    def Tool_AutoScroll(self,event): #init function
        #[65b]Code event VwX...Don't modify[65b]#
        #add your code here
        oc_message.postMessage(self.fifoManager,"LOGCTRL.AUTOSCROLL", True)
        return #end function

    def Tool3c_VwXEvOnTool(self,event): #init function
        #[65a]Code event VwX...Don't modify[65a]#
        #add your code here

        return #end function

    def Tool2c_VwXEvOnTool(self,event): #init function
        #[659]Code event VwX...Don't modify[659]#
        #add your code here

        return #end function

    def OnPreCreate(self):
        #add your code here

        return

    def OnMenuSave(self,event): #init function
        #[651]Code menu VwX...Don't modify[651]#
        #add your code here

        return #end function

    def OnMenuPrint(self,event): #init function
        #[652]Code menu VwX...Don't modify[652]#
        #add your code here

        return #end function

    def OnMenuPaste(self,event): #init function
        #[656]Code menu VwX...Don't modify[656]#
        #add your code here

        return #end function

    def OnMenuNew(self,event): #init function
        #[650]Code menu VwX...Don't modify[650]#
        #add your code here

        return #end function

    def OnMenuHelp(self,event): #init function
        #[657]Code menu VwX...Don't modify[657]#
        #add your code here

        return #end function

    def OnMenuExit(self,event): #init function
        #[653]Code menu VwX...Don't modify[653]#
        #add your code here

        
        return #end function

    def OnMenuCut(self,event): #init function
        #[654]Code menu VwX...Don't modify[654]#
        #add your code here

        return #end function

    def OnMenuCopy(self,event): #init function
        #[655]Code menu VwX...Don't modify[655]#
        #add your code here

        return #end function

    def OnMenuAbout(self,event): #init function
        #[658]Code menu VwX...Don't modify[658]#
        #add your code here

        return #end function

    def initBefore(self):
        #add your code here

        return

    def initAfter(self):
        #add your code here
        self.initManager()
        return

    def Ddel(self): #init function
        #[64e]Code VwX...Don't modify[64e]#
        #add your code here
        

        
        return #end function


    def postManager(self, typename, param):
        oc_message.postMessage(self.fifoManager, typename, param)

    
    def stopManager(self):
        self.ocLogserver.stop()
        self.ocManager.stop()
        
            
    def initManager(self):
        # create fifo
        self.fifoManager = oc_fifo.Fifo(32)
        # Create Manager
        self.ocManager = oc_manager.Manager(self.fifoManager, self.wxLogCtrl, self.txm140c )
        self.ocManager.initView()
        self.ocManager.start()
        # Create logserver
        self.ocLogserver = oc_logserver.Logserver( self.fifoManager, self.fifoManager,"localhost", logging.handlers.DEFAULT_TCP_LOGGING_PORT,5)
        self.ocLogserver.start()
        
        

