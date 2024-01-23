#####################################################################
# Author    : Eshan Roy <eshan@snigdhaos.org>                       #
# Web       : eshan.snigdhaos.org                                   #
# Lead Maintainer & Developer @ Snigdha OS!                         #
#####################################################################

import snigdhaos_functions as func


def snigdha_repo_add(self, txt):
    """Append a new repo"""
    with open(func.pacman, "a", encoding="utf-8") as file:
        file.write("\n\n")
        file.write(txt)

    func.show_in_app_notification(self, "Settings Saved Successfully")


def append_mirror(self, text):
    """Append a new mirror"""
    with open(func.arcolinux_mirrorlist, "a", encoding="utf-8") as file:
        file.write("\n\n")
        file.write(text)

    func.show_in_app_notification(self, "Settings Saved Successfully")