# -*- coding: UTF-8 -*-

"""
OctopyLog Project :
"""

__author__      = "$Author: octopy $"
__version__     = "$Revision: 1.1 $"
__copyright__   = "Copyright 2009, The OctopyLog Project"
__license__     = "GPL"
__email__       = "octopy@gmail.com"



import time
import logging
import threading

import oc_logserver

import network.oc_fifo as oc_fifo
import network.oc_server as oc_server
import network.oc_message as oc_message

# create message
oc_message.addMessageType("LOG.RAW")
oc_message.addMessageType("LOGCTRL.AUTOSCROLL")
oc_message.addMessageType("LOGCTRL.CLEAR")
oc_message.addMessageType("LOGCTRL.WRITEFILE")

# connection
oc_message.addMessageType("CONNECTION.INFO")
oc_message.addMessageType("CONNECTION.CLOSE")
oc_message.addMessageType("CONNECTION.STARTCAPTURE")
oc_message.addMessageType("CONNECTION.STOPCAPTURE")


# general application log
oc_message.addMessageType("APP.LOG")
oc_message.addMessageType("APP.CRITICALERROR")
oc_message.addMessageType("APP.DROPFIFO")
oc_message.addMessageType("PARSEUR.ITEM")


oc_message.addMessageType("EXPORT.TXT")



class Manager:
    """ """

    def __init__(self, fifoIn):

        self.fifoIn             = fifoIn


        self.finished = threading.Event()
        self.thd = None

        # event => callback
        self._dispatch = {}
        self._dispatch[ oc_message.getId("LOG.RAW") ]              = self.logRaw
        self._dispatch[ oc_message.getId("CONNECTION.INFO") ]      = self.connectionInfo
        self._dispatch[ oc_message.getId("CONNECTION.CLOSE") ]     = self.connectionClose
        self._dispatch[ oc_message.getId("APP.LOG") ]              = self.appLog
        self._dispatch[ oc_message.getId("APP.CRITICALERROR") ]    = self.appCriticalError
        self._dispatch[ oc_message.getId("APP.DROPFIFO") ]         = self.appDropFifo

        self._dispatch[ oc_message.getId("PARSEUR.ITEM") ]         = self.parseurItem






        # wx.log



    def parseurItem(self, param):
        pass


    def logRaw(self, param):


        try :

            print u"%s%s%s" % (param["connectionID"].__str__().ljust(3),\
                               param["name"].ljust(24),\
                               param["msg"].decode("utf-8"))

        except Exception, ex:
            print "Drop one raw : %s" % ex.__str__()


    def connectionInfo(self, param):
        # use Application log
        self.appLog(param)

    def connectionClose(self, param):
        pass




    def appLog(self, param):
        """ Application log view """
        pass

    def appCriticalError(self, param):
        self.appLog("Critical Error for application")
        self.appLog("ToDo : add a debug trace system")

    def appDropFifo(self, param):
        self.appLog("FIFO full, one item was lost in : %s" % param)



    def stop(self):
        print "try to stop oc_manager"
        self.finished.set()
        self.fifoIn.unblock()
        self.thd.join()

    def start(self):
        self.thd = threading.Thread(target=self.run,  name="AppControler")
        self.thd.start()

    def run(self):
        while not self.finished.isSet():
            item = self.fifoIn.getitem(True, None)
            if item is not None :
                self._dispatch[item.type](item.obj)
            else:
                break
        print "exit run oc_manager"

    def run_no_blocking(self):
        for i in range(10):
            item = self.fifoIn.getitem(False, 0)
            if item is not None :
                self._dispatch[item.type](item.obj)
            else :
                break



def run_cmd():
    try :
        fifoManager = oc_fifo.Fifo(128)
        ocManager = Manager(fifoManager )
        ocManager.start()
        ocLogserver = oc_logserver.Logserver(fifoManager, fifoManager, \
                                            "localhost", logging.handlers.DEFAULT_TCP_LOGGING_PORT, 5)
        ocLogserver.start()
        ocLogserver.startLog()
    except Exception, ex:
        try:
            ocManager.stop()
            ocLogserver.stop()
        except:
            pass
        raise ex
    print "Started"
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt, ex:
        print "User Ctrl+C, exit"
        ocManager.stop()
        ocLogserver.stop()
    except Exception, ex:
        ocManager.stop()
        ocLogserver.stop()
        raise




if __name__ == '__main__':

    run_cmd()





