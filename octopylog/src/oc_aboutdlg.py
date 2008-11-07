# -*- coding: UTF-8 -*-
###########################################################
# Project  : Octopylog                                    #
# License  : GNU General Public License (GPL)             #
# Author   : JMB                                          #
# Date     : 06/11/08                                     #
###########################################################


__version__ = "$Revision: 1.2 $"
__author__ = "$Author: octopy $"



import wx


aboutText = """
Version : 0.1.0
License : GPL
"""

urllink = "http://developer.berlios.de/projects/octopylog/"


class About(wx.Dialog):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE|wx.STAY_ON_TOP
        wx.Dialog.__init__(self, *args, **kwds)
        self.logo = wx.StaticBitmap(self, -1, wx.Bitmap("images\\octopylog_logo.png", wx.BITMAP_TYPE_ANY))
        self.info = wx.StaticText(self, -1, aboutText)
        self.Close = wx.Button(self, -1, "Close")
        
        self.visit = wx.StaticText(self, -1, "Visit : ")
        self.link = wx.HyperlinkCtrl(self, -1, urllink, urllink)
        
        self.__set_properties()
        self.__do_layout()
        
        self.Bind(wx.EVT_BUTTON, self.onClose, self.Close)
        
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: About.__set_properties
        self.SetTitle("About")
        _icon = wx.EmptyIcon()
        _icon.CopyFromBitmap(wx.Bitmap("images\\octopylog_icone.png", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)
        # end wxGlade

    def __do_layout(self):

        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)

        sizer_1.Add((200, 20), 0, 0, 0)
        sizer_1.Add(self.logo, 0, wx.ALL|wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_1.Add(self.info, 0, wx.ALL, 5)
        sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)
        sizer_1.Add((200, 20), 0, 0, 0)
        sizer_1.Add(self.Close, 0, wx.ALL|wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        
        sizer_2.Add(self.visit, 0, wx.ALL, 5)
        sizer_2.Add(self.link, 0, wx.ALL, 5)
        
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
       

    def onClose(self, event): 
        self.EndModal(0)
        event.Skip()



if __name__ == "__main__":
    
    class MyApp(wx.App):
        def OnInit(self):
            wx.InitAllImageHandlers()
            about = About(None, -1, "")
            about.ShowModal()
            return 1    
    App = MyApp(0)
    # App.MainLoop()




