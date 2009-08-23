
import  wx


class TestVirtualList(wx.ListCtrl):
    def __init__(self, parent, data):
        wx.ListCtrl.__init__(
            self, parent, -1, 
            style=wx.LC_REPORT|wx.LC_VIRTUAL|wx.LC_HRULES|wx.LC_VRULES
            )


        self.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

        self.data = data


        self.filename = "data.txt"
        self.fd = open(self.filename, "w")
        self.fd.close()

        self.InsertColumn(0, "First")
        self.InsertColumn(1, "Second")
        self.InsertColumn(2, "Third")
        self.SetColumnWidth(0, 175)
        self.SetColumnWidth(1, 175)
        self.SetColumnWidth(2, 175)

        self.SetItemCount(len(self.data))

        self.attr1 = wx.ListItemAttr()
        self.attr1.SetBackgroundColour("yellow")

        self.attr2 = wx.ListItemAttr()
        self.attr2.SetBackgroundColour("light blue")

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected)


    def OnItemSelected(self, event):
        self.currentItem = event.m_itemIndex
        print ('OnItemSelected: "%s", "%s", "%s", "%s"\n' %
                           (self.currentItem,
                            self.GetItemText(self.currentItem),
                            self.getColumnText(self.currentItem, 1),
                            self.getColumnText(self.currentItem, 2)))

    def OnItemActivated(self, event):
        self.currentItem = event.m_itemIndex
        print ("OnItemActivated: %s\nTopItem: %s\n" %
                           (self.GetItemText(self.currentItem), self.GetTopItem()))

    def getColumnText(self, index, col):
        item = self.GetItem(index, col)
        return item.GetText()

    def OnItemDeselected(self, evt):
        print ("OnItemDeselected: %s" % evt.m_itemIndex)




    def AppendItem(self, *info):
        
        
        l = ["%d" % len(self.data)]
        l.extend(info)
        self.data.append(l)
        
        self.fd = open(self.filename, "a")
        self.fd.write("%s\n" % l)
        self.fd.close()
        self.SetItemCount(len(self.data))

    #---------------------------------------------------
    # These methods are callbacks for implementing the
    # "virtualness" of the list...  Normally you would
    # determine the text, attributes and/or image based
    # on values from some external data source, but for
    # this demo we'll just calculate them
    def OnGetItemText(self, item, col):
        import linecache
        
        l = linecache.getline("/home/jmb/workspace/octopylog/test/client/data.txt", item)
        if l != "":
            print "Read : %s" % l
        
        return "%s" % self.data[item][col]


    def OnGetItemAttr(self, item):
        return None
        if item % 3 == 1:
            return self.attr1
        elif item % 3 == 2:
            return self.attr2
        else:
            return None


#---------------------------------------------------------------------------

class TestFrame(wx.Frame):
    def __init__(self, parent, log):
        wx.Frame.__init__(self, parent, -1, "Huge (virtual) Table Demo", size=(640,480))


        
        self.Bind(wx.EVT_IDLE, self.on_idle)
        
        self.data = []
        for i in range(10):
            self.data.append(["0" * 10,"1"*44,"2"*55])
        
        self.vl = TestVirtualList(self, self.data)


    def on_idle(self, event):
        self.vl.AppendItem("pp", "dodo")
        #self.data.append(["%d"%len(self.data),"pp", "doo"] )
        #self.vl.SetItemCount(len(self.data))
        #self.vl.EnsureVisible(len(self.data)-1)
        

                


#---------------------------------------------------------------------------

if __name__ == '__main__':
    import sys
    app = wx.PySimpleApp()
    frame = TestFrame(None, sys.stdout)
    frame.Show(True)
    app.MainLoop()


#---------------------------------------------------------------------------