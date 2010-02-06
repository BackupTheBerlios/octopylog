# -*- coding: UTF-8 -*-

"""
OctopyLog Project :
"""

__author__      = "$Author: octopy $"
__version__     = "$Revision: 1.1 $"
__copyright__   = "Copyright 2009, The OctopyLog Project"
__license__     = "GPL"
__email__       = "octopy@gmail.com"




import app
import stdout


from optparse import OptionParser





interface = {}


INTERFACE_DEFAULT = 0
INTERFACE_LIST = 1


interface["result"] = (("standalone"),
                       ("none", "standalone", "stdout"))
interface["trace"] =  ([],
                       ("none", "octopylog", "txt"))


parser = OptionParser()
parser.add_option("-g", "--gui",
                    action="store_true", dest="gui", default=False,
                    help="enable gui")

parser.add_option("-c", "--stdout",
                    action="store_true", dest="stdout", default=False,
                    help="enable stdout")




(options, args) = parser.parse_args()




if options.gui :
    print "run octopylog gui"
    app.run_gui()
else :
    print "run octopylog stdout"
    stdout.run_cmd()




