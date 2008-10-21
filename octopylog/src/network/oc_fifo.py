# -*- coding: UTF-8 -*-
###########################################################
# Project  : Octopylog                                    #
# License  : GNU General Public License (GPL)             #
# Author   : JMB                                          #
# Date     : 21/10/08                                     #
###########################################################


__version__ = "$Revision: 1.1 $"
__author__ = "$Author: octopy $"



import threading
import Queue
import time






class Overrun(Exception):
    "Exception raised by Fifo when is full, all pending item(s) are lost"
    pass

class Fifo(Queue.Queue):
     def __init__( self, maxsize, name = ""):
        self._name = name
        self._maxsize = maxsize
        Queue.Queue.__init__(self, maxsize) 
     
     
     def clear(self):
         try:
            while self.empty() is not True :
                self.get_nowait()
         except Queue.Empty:
             pass
     
     
     def putitem(self, item):
        try:
            #self.put_nowait(item)
            self.put(item, True, None)
        except Queue.Full:
            try :
                # Clear queue
                while self.empty() is not True :
                    self.get_nowait()
                # Add msg
                self.put_nowait(item)
                raise Overrun
            except (Queue.Empty, Queue.Full) :
                raise Exception("Fifo no recoverable error")
     
     def getitem(self, block=False, timeout=None):
         try:
             return self.get(block,timeout)
         except (Queue.Empty):
             return None
    
     def unblock(self):
         # Put a dummy item to force get to return
         self.putitem(None)

            
     def getmaxsize(self):
         return self._maxsize
     
     def getsize(self):
         return self.qsize()   
     


        

if __name__ == '__main__':
    pass
    
    
    