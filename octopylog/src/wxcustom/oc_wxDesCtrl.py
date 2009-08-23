# -*- coding: UTF-8 -*-

""" 
OctopyLog Project : 
"""

__author__      = "$Author: octopy $"
__version__     = "$Revision: 1.6 $"
__copyright__   = "Copyright 2009, The OctopyLog Project"
__license__     = "GPL"
__email__       = "octopy@gmail.com"





import wx





        
        




class DesCtrl(wx.TextCtrl):
    

    def __init__(self, parent, id):
        wx.TextCtrl.__init__(self, parent, wx.NewId(), "", style=wx.TE_MULTILINE|wx.NO_BORDER)
        self.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
    

    
    def clear_view(self):
        self.Clear()
    
    
    def parse_item(self, data):
        self.Clear()
        
        try :
            msg = data["msg"]
            del data["msg"]
        
            for k, v in data.iteritems():
                self.AppendText(self.format(k, v))
              
            try :
                scope, dict = self.msg_extract(msg)       
                dis = "+ [msg] :: \"%s\"\n" % scope
                for k,v in dict.iteritems():
                    dis += "    + [%s] :: %s\n" % (k,v.__str__())
                self.AppendText(dis)
            except :
                
                self.AppendText("+ [msg] ::\n")
                self.AppendText("    + %s" % msg)       
                
                     
        except (Exception), (error):
            
            self.Clear()
            self.AppendText("Error in parsing :\n")
            self.AppendText("%s" % error.__str__())
    
    @staticmethod
    def display_dict(dic, level=1):
        import UserDict
        import UserList
        dis = ""
        for k,v in dic.iteritems():
            if      isinstance(v, UserDict.UserDict) :
                dis += "%s+ [%s] ::\n" % ((" "*(level*4)),k)  
                dis += DesCtrl.display_dict(v, level+1)
            elif    isinstance(v, UserList.UserList):
                dis += "%s+ [%s] ::\n" % ((" "*level),k)  
                for item in v:
                    #tmp = item.__str__()
                    dis += DesCtrl.display_dict(item, level+1)
                    #dis += "%s+ %s\n" % ((" "*(level*4*2)), tmp) 
            else:
                dis += "%s+ [%s] :: %s\n" % ((" "*level),k,v.__str__())    
        return dis
   
   
    def format(self, item1, item2):        
        item1 = item1.strip()
        item2 = item2.strip()
        return "+ [%s] :: %s\n"  % (item1, item2)              

   
    @staticmethod
    def msg_extract(msg):
        
        pos = msg.find(":")
        scope = msg[0:pos]
        dict  = conv_dict(msg[pos+1:])
                    
        return (scope, dict)



def conv_dict(data):
    import UserDict
    try:
        return UserDict.UserDict(eval(data))
    except Exception , error:
        raise error  
        


 
if __name__ == "__main__":
     
     
    data_asser_ko = """assert_ko : {'function': 'case_08', 'file': 'C:\\CVS_Local\\PyTestEmb\\test\\script_cases.py', 'time': 0.70326535914480759, 'msg': '1==2', 'line': 42, 'expression': 'test.assert_true(1==2, "1==2")'}"""
    data_exception = """py_exception : {'exception_info': "'module' object has no attribute 'trace_msg'", 'exception_class': 'AttributeError', 'stack': [{'function': 'boundValue', 'path': 'C:\\CVS_Local\\PyTestEmb\\test\\folder_01\\script_01.py', 'line': 17, 'code': '    test.trace_msg("No wait")'}], 'time': 0.61336231280791276}"""
     
    
    scope, dict = DesCtrl.msg_extract(data_exception)
    
    print DesCtrl.display_dict(dict)
 
 
    
    
    
    
    
    