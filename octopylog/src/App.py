# -*- coding: UTF-8 -*-

""" 
OctopyLog Project : 
"""

__author__      = "$Author: octopy $"
__version__     = "$Revision: 1.4 $"
__copyright__   = "Copyright 2009, The OctopyLog Project"
__license__     = "GPL"
__email__       = "octopy@gmail.com"



import wx
import oc_mainframe

class MyApp(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        frameMain = oc_mainframe.MainFrame(None, -1, "")
        self.SetTopWindow(frameMain)
        frameMain.Show()
        return 1

# end of class MyApp

if __name__ == "__main__":
    App = MyApp(0)
    App.MainLoop()


