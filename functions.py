##########################################################################
# Author : Eshan Roy <eshan@snigdhaos.org>
# URI: https://eshan.snigdhaos.org
# Lead Maintainer @ Snidgha OS
##########################################################################

# module imports
import gi
gi.require_version("Gtk", "3.0")

import os
from os import getlogin,path,makedirs,listdir, unlink, symlink
import psutil
import shutil


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
    if not path.exists(destination):
        makedirs(destination)
    for item in listdir(source):
        s = path.join(source, item)
        d = path.join(destination, item)
        if path.exists(d):
            try:
                shutil.rmtree(d)
            except Exception as e:
                print(e)
                unlink(d)
        if path.isdir(s):
            try:
                shutil.copy(s, d, symlink, ignore)
            except Exception as e:
                print(e)
                print("*Error!")
                self.ecode = 1
        else:
            try:
                shutil.copy2(s, d)
            except:
                print("**Error!")
                self.ecode = 1

def file_check(file):
    if path.isfile(file):
        return True
    return False

def path_check(path):
    if os.path.isdir(path):
        return True
    return False

def empty_dir_check(path):
    if os.path.exists(path) and not os.path.isfile(path):
        if not os.listdir(path):
            return True
        else:
            return False

def content_check(value, file):
    try:
        with open(file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            f.close()
        for line in lines:
            if value in line:
                return True
            else:
                return False
        return False
    except:
        return False

 