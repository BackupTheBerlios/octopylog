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
#[inc]add your include files here

#[inc]end your include

class dlgAbout(wx.Dialog):
    def __init__(self,parent,id = -1,title = '',pos = wx.Point(1,1),size = wx.Size(430,225),style = wx.DEFAULT_DIALOG_STYLE,name = 'dialogBox'):
        pre=wx.PreDialog()
        self.OnPreCreate()
        pre.Create(parent,id,title,pos,size,wx.CLOSE_BOX|wx.DEFAULT_DIALOG_STYLE,name)
        self.PostCreate(pre)
        self.initBefore()
        self.VwXinit()
        self.initAfter()

    def __del__(self):
        self.Ddel()
        return


    def VwXinit(self):
        self.st5c = wx.StaticText(self,-1,"",wx.Point(3,3),wx.Size(418,78),wx.ST_NO_AUTORESIZE)
        self.st5c.SetLabel("wxLogging \r\nGraphical server for logging python module\r\n")
        self.sz4s = wx.BoxSizer(wx.VERTICAL)
        self.sz4s.Add(self.st5c,1,wx.TOP|wx.LEFT|wx.BOTTOM|wx.RIGHT|wx.EXPAND|wx.FIXED_MINSIZE,3)
        self.SetSizer(self.sz4s);self.SetAutoLayout(1);self.Layout();
        self.Refresh()
        return
    def VwXDelComp(self):
        return

#[win]add your code here

    def OnPreCreate(self):
        #add your code here

        return

    def initBefore(self):
        #add your code here

        return

    def initAfter(self):
        #add your code here

        return

    def Ddel(self): #init function
        #[751]Code VwX...Don't modify[751]#
        #add your code here

        return #end function

#[win]end your code
