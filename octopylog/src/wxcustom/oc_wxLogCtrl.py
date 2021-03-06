# -*- coding: UTF-8 -*-

"""
OctopyLog Project :
"""

__author__      = "$Author: octopy $"
__version__     = "$Revision: 1.14 $"
__copyright__   = "Copyright 2009, The OctopyLog Project"
__license__     = "GPL"
__email__       = "octopy@gmail.com"




import wx

import network.oc_message as oc_message

class wxColourManager:
    """" Manage color : associate an object to a color """
#    _listcolour = ["RED",
#                   "DARK TURQUOISE",
#                   "YELLOW GREEN",
#                   "MEDIUM ORCHID",
#                   "MEDIUM AQUAMARINE",
#                   "GREEN YELLOW",
#                   "MEDIUM GOLDENROD",
#                   "PALE GREEN",
#                   "MEDIUM VIOLET RED",
#                   "PLUM",
#                   "GOLDENROD",
#                   "PINK",
#                   "TURQUOISE",
#                   "YELLOW",
#                   "MEDIUM TURQUOISE",]
    _listcolour = ["RED",
                   "BLACK",
                   "BLUE",
                   "YELLOW",
                   "DARK TURQUOISE",]

    def __init__(self):
        self.dic = {}
        self.index = 0
        self.wxColourDatabase = wx.ColourDatabase()

    def clear(self):
        self.dic = {}

    def allocate(self, item):
        if self.index >= len(wxColourManager._listcolour) :
            self.index = 0
        ret = self.dic[item] = wxColourManager._listcolour[self.index]
        self.index += 1
        return ret

    def findcolour(self, colourname):
        return self.wxColourDatabase.Find(colourname)

    def getcolour(self, item):
        colourname = self.dic.get(item,None)
        if colourname is None :
            colourname = self.allocate(item)
        return self.wxColourDatabase.Find(colourname)







EVT_CUSTOM_MSG_LOGCTRL_ID = wx.NewId()


def EVT_CUSTOM_MSG_LOGCTRL(win, func):
    win.Connect(-1, -1, EVT_CUSTOM_MSG_LOGCTRL_ID, func)



class EventMsgLogCtrl(wx.PyEvent):
    def __init__(self, msg):
        wx.PyEvent.__init__(self)
        self.msg = msg
        self.SetEventType(EVT_CUSTOM_MSG_LOGCTRL_ID)
    def clone(self):
        return EventMsgLogCtrl(self.msg)









class LogCtrl(wx.ListCtrl):


    def __init__(self, parent, id, pos = wx.DefaultPosition, size = wx.DefaultSize):

        wx.ListCtrl.__init__(self, parent, wx.NewId(), pos, size, style = (wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_HRULES))

        self.colourManager =  wxColourManager()


        self.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.autoscroll = False


        self.number = 0 # assign at each log an incremental number

        # Event binding
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)
        self.Bind(wx.EVT_COMMAND_RIGHT_CLICK, self.OnRightClick)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected)


        EVT_CUSTOM_MSG_LOGCTRL(self, self.on_new_msg)

        self.selectedItem = -1
        self.title = []

        self.fifoManager = None


    def on_new_msg(self, event):
        msg = event.msg
        self.addLogItem(msg)
        #event.Skip()



    def getColumnText(self, index, col):
        item = self.GetItem(index, col)
        return item.GetText()



    def OnItemSelected(self, event):

        data = {}
        for i in range(len(self.title)):
            data[self.title[i]] = self.getColumnText(event.m_itemIndex, i)
        self.toParseur(data)

        #event.Skip()


    def OnItemDeselected(self, event):
        self.selectedItem = -1
        #event.Skip()

    def toParseur(self, data):

        oc_message.postMessage(self.fifoManager, "PARSEUR.ITEM", data)


    def OnRightClick(self, event):

        # only do this part the first time so the events are only bound once
        if not hasattr(self, "popupID1"):
            self.popupID1 = wx.NewId()
            self.popupID2 = wx.NewId()

            self.Bind(wx.EVT_MENU, self.OnPopupOne, id=self.popupID1)
            self.Bind(wx.EVT_MENU, self.OnPopupTwo, id=self.popupID2)

        # make a menu
        menu = wx.Menu()
        # add some items
        menu.Append(self.popupID1, "Mark")
        menu.Append(self.popupID2, "UnMark")


        # Popup the menu.  If an item is selected then its handler
        # will be called before PopupMenu returns.
        self.PopupMenu(menu)
        menu.Destroy()
        #event.Skip()


    def OnPopupOne(self, event):
        self.mark(self.selectedItem)

    def OnPopupTwo(self, event):
        self.unMark(self.selectedItem)


    def newnumber(self):
        c = self.number
        self.number += 1
        return c


    def mark(self, index):

        font =  self.GetFont()
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        #colour = self.colourManager.findcolour("ORANGE")
        #self.SetItemBackgroundColour(index,colour)
        self.SetItemFont(index, font)


    def unMark(self, index):
        font =  self.GetFont()
        font.SetWeight(wx.FONTWEIGHT_NORMAL)
        #colour = self.colourManager.findcolour("ORANGE")
        #self.SetItemBackgroundColour(index,colour)
        self.SetItemFont(index, font)



    def clear(self):
        self.DeleteAllItems()

    def setAutoscroll(self, value):
        self.autoscroll = value



    def setHeader(self, item):

        self.DeleteAllItems()
        self.ClearAll()

        # number
        self.InsertColumn(0, "Number", wx.LIST_FORMAT_LEFT, -1)
        self.SetColumnWidth(0, 96)
        self.title.append("Number")

        # log data
        for i in range(len(item)):
            self.InsertColumn(1+i, item[i], wx.LIST_FORMAT_LEFT, -1)
            self.SetColumnWidth(1+i, 128*(i+1))
            self.title.append(item[i])



    def addLogItem(self, data):

        # create item (format)
        newItem = wx.ListItem()
        newItem.SetMask(wx.LIST_MASK_TEXT)
        newItem.SetState(wx.LIST_STATE_FOCUSED)
        newItem.SetId(self.GetItemCount())
        newItem.SetColumn(0)
        # ask to the colour manager for the backgroundcolour
        colour = self.colourManager.getcolour((data[0],data[1]))
        newItem.SetBackgroundColour(colour)
         # insert item in ctrlList
        index = self.InsertItem(newItem)


        # number
        self.SetStringItem(index,0,"%6d" % self.newnumber(),0)
        # log data
        for i in range(len(data)):
            self.SetStringItem(index, 1+i, data[i], 0)

        # autoscroll management
        if self.autoscroll is True :
            self.EnsureVisible(index)
        else :
            pass

    def export_txt(self, filename):

        try :
            f = open(filename, "w")
        except :
            raise

        nb = self.GetItemCount()

        for index in range(nb):
            d = []
            num = self.getColumnText(index, 0).strip()
            con = self.getColumnText(index, 1).strip()
            name = self.getColumnText(index, 2).strip()
            msg = self.getColumnText(index, 3).strip()
            line = "%s%s%s%s\n".encode("utf-8") % (num.ljust(8),\
                                 con.ljust(4),\
                                 name.ljust(32),\
                                 msg.__str__())
            try:
                f.write(line)
            except :
                raise
        try:
            f.close()
        except :
            raise




class LogCtrl3(wx.TextCtrl):


    def __init__(self, parent, id, pos = wx.DefaultPosition, size = wx.DefaultSize):

        wx.TextCtrl.__init__(self,parent, style=wx.TE_MULTILINE|wx.TE_DONTWRAP|wx.TE_READONLY)

        self.colourManager =  wxColourManager()


        self.SetBackgroundColour((200,180,160))
        self.SetFont(wx.Font(10, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        self.autoscroll = False


        self.number = 0 # assign at each log an incremental number

        EVT_CUSTOM_MSG_LOGCTRL(self, self.on_new_msg)

        self.selectedItem = -1
        self.title = []

        self.fifoManager = None


    def on_new_msg(self, event):
        msg = event.msg
        self.addLogItem(msg)
        #event.Skip()




    def toParseur(self, data):
        oc_message.postMessage(self.fifoManager, "PARSEUR.ITEM", data)


    def newnumber(self):
        c = self.number
        self.number += 1
        return c




    def clear(self):
        self.SetValue("")

    def setAutoscroll(self, value):
        self.autoscroll = value



    def setHeader(self, item):

        self.Clear()



    def addLogItem(self, data):

        # ask to the colour manager for the backgroundcolour
        colour = self.colourManager.getcolour((data[0],data[1]))
        ta = wx.TextAttr()
        ta.SetTextColour(colour)
        self.SetDefaultStyle(ta)


        # id line
        idl = "%6d".ljust(10) % self.newnumber()
        # id con
        idc = "%s" % data[0].ljust(3)
        # module
        mod = "%s" % data[1].ljust(24)
        # value
        val = "%s" % data[2]


        line = " ".join((idl, idc, mod, val))
        self.AppendText(line + "\n")

        # autoscroll management
        if self.autoscroll is True :
            pass
        else :
            pass

    def export_txt(self, filename):

        try :
            f = open(filename, "w")
        except :
            raise

        try:
            f.write(self.GetValue().encode("utf-8"))
        except :
            raise
        try:
            f.close()
        except :
            raise



if __name__ == "__main__":

    app = wx.App(0)
    colourManager =  wxColourManager()
    print colourManager.getcolour("dfd")
    print colourManager.getcolour("dfds")
    print colourManager.getcolour("dfd")





