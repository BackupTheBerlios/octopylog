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
