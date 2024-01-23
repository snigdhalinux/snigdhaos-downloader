#####################################################################
# Author    : Eshan Roy <eshan@snigdhaos.org>                       #
# Web       : eshan.snigdhaos.org                                   #
# Lead Maintainer & Developer @ Snigdha OS!                         #
#####################################################################

import gi
gi.require_version('Gtk', '3.0')
from os import path, getlogin
# from gi.repository import

get_distro = id()
superuser = getlogin()
home = "/home/" + str(superuser)