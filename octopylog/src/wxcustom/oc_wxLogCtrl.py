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



class wxColourManager:
    """" Manage colour : associate an object to a colour """
    _listcolour = ["DARK TURQUOISE", 
                   "YELLOW GREEN",
                   "MEDIUM ORCHID",
                   "MEDIUM AQUAMARINE", 
                   "GREEN YELLOW",
                   "MEDIUM GOLDENROD",
                   "PALE GREEN",
                   "MEDIUM VIOLET RED",    
                   "PLUM",
                   "GOLDENROD",
                   "PINK",    
                   "TURQUOISE",
                   "YELLOW",
                   "MEDIUM TURQUOISE",]   
    
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
    
    def getcolour(self, item):
        colourname = self.dic.get(item,None)
        if colourname is None :
            colourname = self.allocate(item)
        return self.wxColourDatabase.Find(colourname)
         
        
        




class LogCtrl(wx.ListCtrl):
    
    
    def __init__(self, parent, id, pos = wx.DefaultPosition, size = wx.DefaultSize):
        id = 1111
        wx.ListCtrl.__init__(self, parent, id, pos, size, style = (wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_HRULES))
        
        self.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.autoscroll = False
        self.colourManager =  wxColourManager()
        
        self.number = 0 # assign at each log an incremental number

        # Event binding
        #self.Bind(wx.EVT_SIZE, self.sizeMe, id=1111)
        #self.Bind(wx.EVT_MOTION, self.motion, id=1111)
        
    def newnumber(self):
        c = self.number
        self.number += 1
        return c    
        
        
    def clear(self):
        pass
    
    
    def setAutoscroll(self, value):
        self.autoscroll = value



    def setHeader(self, item):
        
        self.DeleteAllItems()
        self.ClearAll()
        
        # number 
        self.InsertColumn(0, "Number", wx.LIST_FORMAT_LEFT, -1)
        self.SetColumnWidth(0, 96)       
        
        # log data
        for i in range(len(item)):
            self.InsertColumn(1+i, item[i], wx.LIST_FORMAT_LEFT, -1)
            self.SetColumnWidth(1+i, 128*(i+1))
            
    

    def addLogItem(self, data):
        

         # create item (format)      
         NewItem = wx.ListItem()
         NewItem.SetMask(wx.LIST_MASK_TEXT)
         NewItem.SetState(wx.LIST_STATE_FOCUSED)
         NewItem.SetId(self.GetItemCount())
         NewItem.SetColumn(0)
         # ask to the colour manager for the backgroundcolour
         colour = self.colourManager.getcolour((data[0],data[1]))
         NewItem.SetBackgroundColour(colour)
         # insert item in ctrlList
         index = self.InsertItem(NewItem)
         
         # fill column
         
         # number
         self.SetStringItem(index,0,"%6d" % self.newnumber(),0)
         # log data
         for i in range(len(data)):
             self.SetStringItem(index,1+i,data[i],0)

         # autoscroll management
         if self.autoscroll is True :
             self.EnsureVisible(index)
         else :
             pass
        



    def sizeMe( self, event ):
        event.Skip()
        
        
    def motion( self, event ):
        event.Skip()    
    


        
        
if __name__ == "__main__":
    
    app = wx.App(0)
    colourManager =  wxColourManager()
    print colourManager.getcolour("dfd")
    print colourManager.getcolour("dfds")
    print colourManager.getcolour("dfd")
    
    
    
    
         
        