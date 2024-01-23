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

# GPG Configurations
gpg_config = "/etc/pacman.d/gnupg/gpg.conf"
gpg_config_local = home + "/.gnupg/gpg.conf"
gpg_config_original = "/usr/share/snigdhaos-downloader/snigdhaos/any/gpg.conf"
gpg_config_local_original = "/usr/share/snigdhaos-downloader/snigdhaos/any/gpg.conf"

## Pacman Configurations
mirrorlist = "/etc/pacman.d/mirrorlist"
pacman = "/etc/pacman.conf"
pacman_archlinux = "/usr/share/snigdhaos-downloader/snigdhaos/arch/pacman/pacman.conf"
pacman_eos = "/usr/share/snigdhaos-downloader/snigdhaos/eos/pacman/pacman.conf"
pacman_garuda = "/usr/share/snigdhaos-downloader/snigdhaos/garuda/pacman/pacman.conf"
blank_pacman_arch = "/usr/share/snigdhaos-downloader/snigdhaos/arch/pacman/blank/pacman.conf"
blank_pacman_eos = "/usr/share/snigdhaos-downloader/snigdhaos/eos/pacman/blank/pacman.conf"
blank_pacman_garuda = "/usr/share/snigdhaos-downloader/snigdhaos/garuda/pacman/blank/pacman.conf"

## Pacman File Configurations
pacman_logfile = "/var/log/pacman.log"
pacman_cache_dir = "/var/cache/pacman/pkg/"
pacman_lockfile = "/var/lib/pacman/db.lck"


def get_lines(files):
    try:
        if path.isfile(files):
            with open(files, "r", encoding="utf-8") as f:
                lines = f.readlines()
                f.close()
            return lines
    except Exception as error:
        print(error)

