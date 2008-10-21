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
provider = wx.SimpleHelpProvider()
wx.HelpProvider_Set(provider)

import frm_Main

class App(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        self.main = frm_Main.frm_Main(None,-1,'')
        self.main.Show()
        self.SetTopWindow(self.main)
        return 1

def main():
    application = App(0)
    application.MainLoop()
    print "end app"

if __name__ == '__main__':
    main()
