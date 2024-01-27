##################################################################################
# Author: Eshan Roy <eshan@snigdhaos.org>
# URL : https://eshan.snigdhaos.org
# Lead Maintainer & Developer @ Snigdha OS
##################################################################################

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gtk

import os
from os import rmdir, unlink, walk, execl, getpgid, system, stat, readlink
from os import path, getlogin, mkdir, makedirs, listdir
import sys
import threading
import shutil
import psutil
import datetime
import subprocess
import logging
import time
import queue
from queue import Queue

distr = id()

sudo_username = getlogin() #needed
home = "/home/" + str(sudo_username)

#GPG Configs
gpg_config = "/etc/pacman.d/gnupg/gpg.conf"
local_gpg_config = home + "/.gnupg/gpg.conf"
origin_gpg_config = "/usr/share/snigdhaos-installer/data/any/gpg.conf" # any -> arch!
orogin_local_gpg_config = "/usr/share/snigdhaos-installer/data/any/gpg.conf"

# Themes(Default)
def_icons = "/usr/share/icons/default/index.theme"

#Mirrorlist
mirrorlist = "/etc/pacman.d/mirrorlist"
snigdhaos_mirrorlist = "/etc/pacman.d/snigdhaos-mirrorlist"

#Pacman Config
pacman = "/etc/packman.conf"
pacman_snigdhaos = "/usr/share/snigdhaos-installer/data/arch/pacman/pacman.conf"

# getting shells -> Snigdha OS
bashrc_snigdhaos = "/usr/share/snigdhaos-installer/snigdhaos/.bashrc" 
fish_snigdhaos = "/usr/share/snigdhaos-installer/snigdhaos/.zshrc"
zsh_snigdhaos = "/usr/share/snigdhaos-installer/snigdhaos/config.fish"

## Backup repository [in case of emergency]
## As adrenaline & arctic are in conflicts
snigdhaos_core ="[snigdhaos-core]\n\
                 SigLevel = Never\n\
                 Server = https://snigdhalinux.github.io/$repo/$arch" # sed -i s^* required databaseoptional *

## No need of chaotic aur as we have nitorzen
# chaotic_aur = "[chaotic-aur]\n\
                # Include = /etc/pacman.d/chaotic-mirrorlist"

pacman_logfile = "/var/log/pacman.log"
pacman_cache_dir = "/var/cache/pacman/pkg"
pacman_lockfile = "/var/lib/pacman/db.lck"

logger = logging.getLogger("logger")
ch = logging.StreamHandler()
logger.setLevel(logging.INFO)
ch.setLevel(logging.INFO)

formatter = logging.Formatter("#Need to see regex") # needed

ch.setFormatter(formatter)
logger.addHandler(ch)

def get_lines(files):
    try:
        if path.isfile(files):
            with open(files, "r", encoding="utf-8") as f:
                lines = f.readlines()
                f.close()
            return lines
    except Exception as error:
        print(error)

def get_position(lists, value):
    data = [string for string in lists if value in string]
    if len(data) != 0:
        position = lists.index(data[0])
        return position
    return 0 # not sure might be null

def get_positions(lists, value):
    data = [string for string in lists if value in string]
    position = []
    for d in data:
        position.append(lists.index(d))
    return position

def _get_variables(lists, value):
    data = [string for string in lists if value in string]
    if len(data) >= 1:
        data1 = [string for string in data if "#" in string]
        for i in data1:
            if i[:4].find("#") != -1:
                data.remove(i)
    if data:
        data_clean = [data[0].strip("\n").replace(" ","")][0].split("=")
    return data_clean

def check_value(list, value):
    data = [string for string in list if value in string]
    if len(data) >= 1:
        data1 = [string for string in data if "#" in string]
        for i in data1:
            if i[:4].find("#") != -1:
                data.remove(i)
    return data

# let's check running process:
def check_fi_process_is_running(processName):
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=["pid", "name", "create_time"])
            if processName == pinfo["name"]:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False



