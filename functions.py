##################################################################################
# Author: Eshan Roy <eshan@snigdhaos.org>
# URL : https://eshan.snigdhaos.org
# Lead Maintainer & Developer @ Snigdha OS
##################################################################################

import gi
gi.require_version("Gtk", "3.0")

import os

distr = id()

sudo_username = getlogin() #needed
home = "/home/" + str(sudo_username)
gpg_config = "/etc/pacman.d/gnupg/gpg.conf"
local_gpg_config = home + "/.gnupg/gpg.conf"
origin_gpg_config = "/usr/share/snigdhaos-installer/data/any/gpg.conf" # any -> arch!
