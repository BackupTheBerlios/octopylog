




import wx





class DesCtrl(wx.TextCtrl):
    

    def __init__(self, parent, id):
        wx.TextCtrl.__init__(self, parent, wx.NewId(), "", style=wx.TE_MULTILINE|wx.NO_BORDER)
        self.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        
    def parse_item(self, data):
        self.Clear()
        
        try :
            msg = data["msg"]
            del data["msg"]
        
            for k, v in data.iteritems():
                self.AppendText(self.format(k, v))
            
            
            
            try :
                scope, dict = self.msg_extract(msg)
                self.AppendText("\n")
                self.AppendText("%s :\n" % scope)
                for item in dict.iteritems():
                    self.AppendText("%s\n" % item)

            except :
                self.AppendText("\n")
                self.AppendText("%s" % msg)       
            
                
                
        except (Exception), (error):
            self.Clear()
            self.AppendText("Error in parsing :\n")
            self.AppendText("%s" % error.__str__())
    
   
   
    def format(self, item1, item2):        
        item1 = item1.strip()
        item1 = item1.ljust(24)
        item2 = item2.strip()
        return "%s::%s\n"  % (item1, item2)              

   
    
    def msg_extract(self, msg):
        
        pos = msg.find(":")
        scope = msg[0:pos]
        dict  = self.conv_dict(msg[pos+1:-1])
        return (scope, dict)

    def conv_dict(self, data):
        import UserDict
        try:
            return UserDict.UserDict(eval(data))
        except Exception , error:
            print data
            raise error   
        
        
        

    
    
    
    
    
    