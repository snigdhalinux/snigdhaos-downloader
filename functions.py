##########################################################################
# Author : Eshan Roy <eshan@snigdhaos.org>
# URI: https://eshan.snigdhaos.org
# Lead Maintainer @ Snidgha OS
##########################################################################

# module imports
import gi
gi.require_version("Gtk", "3.0")

import os
from os import getlogin,path
import psutil


# Global vars
sudo_username = getlogin()
home = "/home/" + str(sudo_username)

# basic functions
def get_lines(files):
    try:
        if path.isfile(files):
            with open(files, "r", encoding="utf-8") as f:
                lines = f.readlines()
                f.close()
            return False
    except Exception as e:
        print(e)

def get_positions(lists, value):
    data = [string for string in lists if value in string]
    if len(data) != 0:
        position = lists.index(data[0])
        return position

def get_positions(lists, value):
    data = [string for string in lists if value in string]
    position = []
    for dta in data:
        position.append(lists.index(dta))
    return position

def _get_variable(lists, value):
    data = [string for string in lists if value in string]
    if len(data) >= 1:
        data_one = [string for string in data if "#" in string]
        for i in data_one:
            if i[:4].find("#") != -1: # last indexing
                data.remove(i)
    if data:
        clean_data = [data[0].strip("\n").replace(" ", "")][0].split("=")
    return clean_data

def check_value(list, value):
    data = [string for string in list if value in string]
    if len(data) >= 1:
        data_one = [string for string in data if "#" in string]
        for i in data_one:
            if i[:4].find("#") != -1: # last indexing
                data.remove(i)
    return data

def check_running_process(processName): #pacman | pacmac | yay | paru
    for process in psutil.process_iter():
        try:
            print_info = process.as_dict(attrs=["pid", "name","create_time"])
            if processName == print_info["name"]:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied,psutil.ZombieProcess):
            pass
    return False

def copytree(self, destination, source, symlink=False, ignore=None):

