# -*- coding: UTF-8 -*-

""" 
OctopyLog Project : 
"""

__author__      = "$Author: octopy $"
__version__     = "$Revision: 1.4 $"
__copyright__   = "Copyright 2009, The OctopyLog Project"
__license__     = "GPL"
__email__       = "octopy@gmail.com"


import cPickle
import SocketServer
import struct



import socket
import threading
import logging







class ConnectionManagerBase:
    """ Manager for the connection 
        Must be derived """
    def __init__(self, maxconnection):
        self._listhandle = list(None for i in range(0,maxconnection))
        self.allow = True
        self._sem = threading.Semaphore()
    
    def getPermissionClientConnection(self):
        self._sem.acquire()    
        val = self.allow
        self._sem.release()
        return val 
           
    def setPermissionClientConnection(self, value):
        self._sem.acquire()    
        self.allow = value
        self._sem.release() 
    
    def allocateId(self, handler):
        """ id allocation 
            fixed number of connection
            id are reused """
        self._sem.acquire()    
        for id in range(len(self._listhandle)) :
            if self._listhandle[id] == None : 
                self._listhandle[id] = handler
                ret = id
                break
        else :  ret = None
        self._sem.release() 
        return ret  
        
    def deallocateId(self, id):
        self._sem.acquire()
        self._listhandle[id] = None
        self._sem.release()    
    
    def disconnect(self, id):
        """ function that is called by the connection when it it closed """
        self.deallocateId(id)
        self.evtDisconnection(id)
        
    def connection(self, handler):
        """ handler that request a connection
            send_obj is the function that send an object an this connection
            return an id if connection is allowed """   
        if self.getPermissionClientConnection is False :
            return None
        
        id = self.allocateId(handler)     
        if id is None  :   self.evtReject()
        else           :   self.evtConnection(id)
        return id    
       
    def getConnectionInfo(self, id):
        """ Status of connection """
        self._sem.acquire()
        h = self._listhandle[id]
        if h is not None:
            ret = h.client_address
        else:
            ret = None
        self._sem.release()
        return ret
 
    def send(self, id, obj):
        """ send an objet on the connection identify by the id number """      
        self._sem.acquire()  
        callback = self._listhandle[id]
        self._sem.release()
        callback.send(obj) 
 
    def closeAll(self):
        # refuse all new connection
        self.setPermissionClientConnection(False)
        # close socket of all current connection
        self._sem.acquire()    
        try :
            for id in range(len(self._listhandle)) :
                if self._listhandle[id] is not None : 
                    self._listhandle[id].connection.close()
        except : 
            # connection can be closed by client
            pass   
        self._sem.release()        
        
        
        
    
    def evtConnection(self, id):
        """ User can overwrite this method """
        pass
    
    def evtDisconnection(self, id):
        """ User can overwrite this method """
        pass
    
    def evtReject(self):
        """ User can overwrite this method """
        pass    
        
    def evtReceived(self, id, obj):
        """ function that is called by the connection when an objet is received """
        pass
    

        


    


#
# Wrapping for one single instance of ConnectionManagerBase derivated
#   
# set_manager( inst_derivated class) must be called before server starting
#

class _wrapperConnection:
    def __init__(self):
        self._ConnectionManager = None
    def set_manager(self, inst_ConnectionManager):
        self._ConnectionManager = inst_ConnectionManager
    def get_manager(self):
        return self._ConnectionManager
    
wc = _wrapperConnection()
def set_manager(inst_ConnectionManager):
    wc.set_manager(inst_ConnectionManager)
def get_manager():
    return wc.get_manager()  




class ObjStreamHandler(SocketServer.StreamRequestHandler):
    """Handler for a streaming logging request.

    This basically logs the record using whatever logging policy is
    configured locally.
    """

    def handle(self):
        """
        Handle multiple requests - each expected to be a 4-byte length,
        followed by the LogRecord in pickle format. Logs the record
        according to whatever policy is configured locally.
        """
        
        self.manager = get_manager()
        
        self.id = self.manager.connection(self)

        if self.id is None :
            return  # connection not allowed
        
        # Loop for receiving data from client
        try :
            while 1:
                chunk = self.connection.recv(4)
                if len(chunk) < 4:
                    raise socket.error("Error on chunk length or socket disconnection") 
                slen = struct.unpack(">L", chunk)[0]
                chunk = self.connection.recv(slen)
                while len(chunk) < slen:
                    chunk = chunk + self.connection.recv(slen - len(chunk))
                obj = self.unPickle(chunk)
                self.manager.evtReceived(self.id, obj)
        except socket.error:
            # Client is disconnected
            self.manager.disconnect(self.id)
        except :
            # Other error, disconnect
            self.manager.disconnect(self.id)
            raise
        # Connection is closed


    def send(self, obj):
        s = self.Picle(obj)
        try:
            if hasattr(self.connection, "sendall"):
                self.connection.sendall(s)
            else:
                sentsofar = 0
                left = len(s)
                while left > 0:
                    sent = self.sock.send(s[sentsofar:])
                    sentsofar = sentsofar + sent
                    left = left - sent
        except socket.error:
             self.manager.disconnect(self.id)
   
    def Picle(self, obj):
        s = cPickle.dumps(obj,1)
        slen = struct.pack(">L", len(s))    
        return slen + s

    def unPickle(self, data):
        return cPickle.loads(data)

        
        
        

class ObjSocketReceiver(SocketServer.ThreadingTCPServer):
    """simple TCP socket-based logging receiver suitable for testing.
    """

    allow_reuse_address = 1

    def __init__(self, host, port):
        SocketServer.ThreadingTCPServer.__init__(self, (host, port), ObjStreamHandler)

        self.timeout = 1
        self._finished = threading.Event()
        
        
    def stop(self):
    
        self._finished.set()
        self.th.join()          
        self.server_close()   
        
    def start(self):   
        self.th = threading.Thread(target=self.serveUntilStopped, name="Server")
        self.th.start()        
        
        
    def serveUntilStopped(self):
        import select
        while not self._finished.isSet():
            rd, wr, ex = select.select([self.socket.fileno()],
                                       [], [],
                                       self.timeout)


            if rd != [] :
                self.handle_request()






def createServer(manager, host, port):
    set_manager(manager)
    return ObjSocketReceiver(host,port)
    

 

if __name__ == "__main__":
    
    pass
    
 
