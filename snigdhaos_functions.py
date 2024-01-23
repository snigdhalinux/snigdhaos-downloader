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
gpg_config = "/etc/pacman.d/gnupg/gpg.conf"
gpg_config_local = home + "/.gnupg/gpg.conf"

gpg_config_original = "/usr/share/snigdhaos-downloader/data/any/gpg.conf"
gpg_config_local_original = "/usr/share/snigdhaos-downloader/data/any/gpg.conf"

def get_lines(files):
    try:
        if path.isfile(files):
            with open(files, "r", encoding="utf-8") as f:
                lines = f.readlines()
                f.close()
            return lines
    except Exception as error:
        print(error)

