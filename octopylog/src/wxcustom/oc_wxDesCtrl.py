




import wx





class DesCtrl(wx.TextCtrl):
    

    def __init__(self, parent, id):
        wx.TextCtrl.__init__(self, parent, wx.NewId(), "", style=wx.TE_MULTILINE|wx.NO_BORDER)
        
        
    def parse_item(self, data):
        self.Clear()
        for item in data:
            self.AppendText("%s\n" % item)
        
    
    
    

    
    
    
    
    
    