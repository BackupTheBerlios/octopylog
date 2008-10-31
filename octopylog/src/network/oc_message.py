# -*- coding: UTF-8 -*-
###########################################################
# Project  : Octopylog                                    #
# License  : GNU General Public License (GPL)             #
# Author   : JMB                                          #
# Date     : 21/10/08                                     #
###########################################################


__version__ = "$Revision: 1.2 $"
__author__ = "$Author: octopy $"



def make_gen():
    """ Unique id for event identification """
    x = 0
    while True :
        yield x
        x += 1
        
        
_id = make_gen()
_msg_type = {}


def addMessageType(name):
    """ create a new type of event """
    id = _id.next()
    _msg_type[name]   = id
    _msg_type[id]     = name




class Message:
    """" define an message type :
            - ID -> int number
            - obj -> an object for parameters """
    def __init__(self, type, obj):
        self.type   = _msg_type[type]
        self.obj    = obj


def postMessage(fifo, typename, param):
    """ post an event in a fifo """
    fifo.putitem(Message(typename,param))

def testMessageType(evt, typename):
    """ test the type of one event """
    return _msg_type[typename] == evt.type
    
def getNameMessage(evt):
    return  _msg_type[evt.type]  

def getId(name):
    return _msg_type[name]

def getName(id):
    return _msg_type[id]


if __name__ == '__main__':
    
    addMessageType("DUMMY")
    addMessageType("START")
    addMessageType("STOP")
    
    msg1 = Message("START",None)
    msg2 = Message("STOP",None)    
    
    print msg1.type
    print getNameMessage(msg1)
    print msg2.type
    print getNameMessage(msg2)

    print getId(1)
