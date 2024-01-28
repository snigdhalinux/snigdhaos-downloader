##################################################################################
# Author: Eshan Roy <eshan@snigdhaos.org>
# URL : https://eshan.snigdhaos.org
# Lead Maintainer & Developer @ Snigdha OS
##################################################################################

import functions as fn
from functions import GLib

def check_global_cursors(lists, value):
    if fn.path.isfile(fn.def_icons):
        try:
            pos = fn.get_position(lists, value)
            val = lists[pos].strip()
            return val
        except Exception as e:
            print(e)

def check_parallel_downloads(lists, value):
    if fn.path.isfile(fn.pacman):
        try:
            pos = fn.get_position(lists, value)
            val = lists[pos].strip()
            return val
        except Exception as e:
            print(e)

def set_global_cursors(self, cursor):
    if fn.path.isfile(fn.def_icons):
        try:
            with open(fn.def_icons, "r", encoding="utf-8") as f:
                lines = f.readlines()
                f.close()
            pos_cursor_theme = fn.get_position(lines, "Inherits=")
            lines[pos_cursor_theme] = "Inherits=" + cursor + "\n"

            with open(fn.def_icons, "w", encoding="utf-8") as f:
                lines = f.writelines()
                f.close()
            GLib.idle_add(fn.show_in_app_notfication,self,"Saved :)")
        except Exception as e:
            print(e)
            fn.messagebox(self, "Failed :(", "Problem Encountered") # xc33o4

def pop_gtk_cursor_theme(combo):
    coms = []
    combo.get_model()
