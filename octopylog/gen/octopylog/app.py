# -*- coding: UTF-8 -*-

"""
OctopyLog Project :
"""

__author__      = "$Author: octopy $"
__version__     = "$Revision: 1.1 $"
__copyright__   = "Copyright 2009, The OctopyLog Project"
__license__     = "GPL"
__email__       = "octopy@gmail.com"




import os.path
import platform


import wx
import oc_mainframe
import wxcustom.exceptlog as exceptlog


APP_NAME    = "Octopylog"
APP_VERSION = "1.0.0 RC1"

# TRACE_DEBUG :
#  True   = Debug Trace Activate
#  False  = Debug Trace DeActivate
TRACE_DEBUG     = True
# EXCEPT_DEBUG :
# True    = std.err for exception output
# False   = GUI exception handler
EXCEPT_DEBUG    = False


def get_app_path():
    if      platform.system() == "Linux":
        path = "/tmp"
    elif    platform.system() == "Windows":
        path = "c:\\temp"
    else:
        raise Exception("Platform not supported")
    if not(os.path.lexists(path)):
        os.mkdir(path)
    return path




class MyApp(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        frameMain = oc_mainframe.MainFrame(None, -1, "")
        self.SetTopWindow(frameMain)
        frameMain.Show()
        return 1


def run_gui():
    if not(EXCEPT_DEBUG) :
        exceptlog.add_exception_hook(get_app_path(), APP_VERSION, __email__)
    App = MyApp(0)
    App.MainLoop()



if __name__ == "__main__":

    run_gui()

