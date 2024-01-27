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

def copytree(self, src, dst, symlinks=False, ignore=None):
    if not path.exists(dst):
        makedirs(dst)
    for item in listdir(src):
        s = path.join(src, item)
        d = path.join(dst, item)
        if path.exists(d):
            # try catch block will work I think if not <--
            try:
                shutil.rmtree(d)
            except Exception as e:
                print(e)
                unlink(d)
        if path.isdir(s):
            try:
                shutil.copytree(s, d, symlinks, ignore)
            except Exception as e:
                print(e)
                print("ERROR#2!") # debugging purpose ig get errors
                self.ecode = 1
        else:
            try:
                shutil.copy2(s, d)
            except:
                print("ERROR#3")
                self.ecode = 1

def file_check(path):
    if os.path.isdir(path):
        return True
    return False

def path_check(path):
    if os.path.isdir(path):
        return True
    return False

def is_empty_directory(path):
    if os.path.exists(path) and not os.path.isfile(path):
        if not os.listdir(path):
            return True
        else:
            return False

def check_content(value, file):
    try:
        with open(file, "r", encoding="utf-8") as myfile:
            lines = myfile.readlines()
            myfile.close()
        for line in lines:
            if value in line:
                if value in line:
                    return True
                else:
                    return False
        return False
    except:
        return False

def check_package_installed(package):
    try:
        subprocess.check_output("pacman -Qi " + package, shell=True, stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError:
        return False

def check_service(service):
    try:
        command = "systemctl is-active " + service + ".service"
        output = subprocess.run(command.split(" "), check=True, shell=False,stdout=subprocess.PIPE, stderr=subprocess.STDOUT,)
        status = output.stdout.decode().strip()
        if status == "active":
            return True
        else:
            return False
    except Exception:
        return False #nothing to print here 

def check_socket(socket):
    try:
        command = "systemctl is-active " + socket + ".socket"
        output = subprocess.run(command.split(" "), check=True,shell=False,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,)
        status = output.stdout.decode().strip()
        if status == "active":
            return True
        else:
            return False
    except Exception:
        return False

def list_users(filename):
    try:
        data = []
        with open(filename, "r", encoding="utf-8") as f:
            for line in f.readlines():
                if "1001" in line.split(":")[2]:
                    data.append(line.split(":")[0])
                if "1002" in line.split(":")[2]:
                    data.append(line.split(":")[0])
                if "1003" in line.split(":")[2]:
                    data.append(line.split(":")[0])
                if "1004" in line.split(":")[2]:
                    data.append(line.split(":")[0])
                if "1005" in line.split(":")[2]:
                    data.append(line.split(":")[0])
            data.sort()
            return data
    except Exception as e:
        print(e)

def check_group(group):
    try:
        groups = subprocess.run(["sh", "-c", "id " + sudo_username], shell=False,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,)
        for i in groups.stdout.decode().split(" "):
            if group in i:
                return True
            else:
                return False
    except Exception as e:
        print(e)
def check_systemd_boot():
    if (path_check("/boot/loader") is True and file_check("/boot/loader/loader.conf") is True):
        return True
    else:
        return False
    
def check_snigdhaos_mirror_active():
    with open(pacman, "r", encoding="utf-8") as f:
        lines = f.readlines()
        f.close()
        snigdhaos_base = "[snigdhaos-core]"
        ntrozen_mirror = "[nitrozen]"
    