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

#Grub
grub_theme_conf = "/boot/grub/themes/snigdhaos-grub-themes/theme.txt"
default_grub_conf = "/etc/defaul/grub"

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
## bump nitrozen -> arctic
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
        nitrozen_mirror = "[nitrozen]"
    for line in lines:
        if nitrozen_mirror in line:
            if "#" + nitrozen_mirror in line:
                return False
            else:
                return True
    for line in lines:
        if snigdhaos_base in line:
            if "#" + snigdhaos_base in line:
                return False
            else:
                return True

def install_package(self, package):
    command = "pacman -S " + package + " --noconfirm --needed"
    if check_package_installed(package):
        print(package + " already installed!")
        GLib.idle_add(show_in_app_notfication, self, package + " already installed!",) #needed
    else:
        try:
            print(command)
            subprocess.call(command.split(" "), shell=False,stdout=subprocess.PIPE, stderr=subprocess.STDOUT,)
            print(package + " installed successfully :)")
            GLib.idle_add(show_in_app_notfication,self,package + " installed successfully :)")
        except Exception as e:
            print(e)

def install_local_package(self, package):
    command = "pacman -U " + package + " --noconfirm"
    try:
        print(command)
        subprocess.call(command.split(" "), shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,)
        print(package + "installed successfully :)")
        GLib.idle_add(show_in_app_notfication,self, package + " installed successfully :)")
    except Exception as e:
        print(e)

def install_snigdhaos_package(self, package):
    if check_snigdhaos_mirror_active():
        command = "pacman -S " + package + " --noconfirm --needed"
        if check_package_installed(package):
            print(package + " already installed!")
            GLib.idle_add(show_in_app_notfication, self, package + " already installed!",)
        else:
            try:
                print(command)
                subprocess.call(command.split(" "),shell=False,stdout=subprocess.PIPE, stderr=subprocess.STDOUT,)
                print(package + " installed sucessfully :)")
                GLib.idle_add(show_in_app_notfication,self, package + " installed successfully :)")
            except Exception as e:
                print(e)
    else:
        print("Snigdha OS Mirror is not active!")
        print("Activate Snigdha OS Mirror First!")
        GLib.idle_add(show_in_app_notfication, self, "Snigdha OS Mirror is not active!")

#remove package without dependencies
def remove_package(self, package):
    command = "pacman -R " + package + " --noconfirm"
    if check_package_installed(package):
        print(command)
        try:
            subprocess.call(command.split(" "),shell=False,stdout=subprocess.PIPE, stderr=subprocess.STDOUT,)
            print(package + " removed successfully ;)")
            GLib.idle_add(show_in_app_notfication, self, " removed successfully ;)")
        except Exception as e:
            print(e)
    else:
        print(package + " already removed!")
        GLib.idle_add(show_in_app_notfication, self, " already removed!")

#let's remove package with dependencies
def remove_package_s(self, package):
    command = "pacman -Rs " + package + " --noconfirm"
    if check_package_installed(package):
        print(command)
        try:
            subprocess.call(command.split(" "),shell=False,stdout=subprocess.PIPE, stderr=subprocess.STDOUT,)
            print(package + " removed successfully ;)")
            GLib.idle_add(show_in_app_notfication, self, " removed successfully ;)")
        except Exception as e:
            print(e)
    else:
        print(package + " already removed!")
        GLib.idle_add(show_in_app_notfication, self, " already removed!")

def remove_package_ss(self, package):
    command = "pacman -Rss " + package + " --noconfirm"
    if check_package_installed(package):
        print(command)
        try:
            subprocess.call(command.split(" "),shell=False,stdout=subprocess.PIPE, stderr=subprocess.STDOUT,)
            print(package + " removed successfully ;)")
            GLib.idle_add(show_in_app_notfication, self, " removed successfully ;)")
        except Exception as e:
            print(e)
    else:
        print(package + " already removed!")
        GLib.idle_add(show_in_app_notfication, self, " already removed!")

def remove_package_dd(self, package):
    command = "pacman -Rdd " + package + " --noconfirm"
    if check_package_installed(package):
        print(command)
        try:
            subprocess.call(command.split(" "),shell=False,stdout=subprocess.PIPE, stderr=subprocess.STDOUT,)
            print(package + " removed successfully ;)")
            GLib.idle_add(show_in_app_notfication, self, " removed successfully ;)")
        except Exception as e:
            print(e)
    else:
        print(package + " already removed!")
        GLib.idle_add(show_in_app_notfication, self, " already removed!")

def enable_login_manager(self, loginmanager):
    if check_package_installed(loginmanager):
        try:
            command = "systemctl enable " + loginmanager + " .service -f"
            print(command)
            subprocess.call(command.split(" "),shell=False,stdout=subprocess.PIPE, stderr=subprocess.STDOUT,)
            print(loginmanager + " enabled :) - Reboot!")
            GLib.idle_add(show_in_app_notfication, self, loginmanager + " enabled :) - Reboot!")
        except Exception as e:
            print(e)
    else:
        print(loginmanager + " not installed :(")
        GLib.idle_add(show_in_app_notfication, self, loginmanager + " not installed :(")

def add_autologin_group(self):
    command = subprocess.run(["sh","-c", "su - " + sudo_username + " -c groups"], check=True,shell=False,stdout=subprocess.PIPE)
    groups = command.stdout.decode().strip().split(" ")
    if "autologin" not in groups:
        command2 = "groupadd autologin"
        try:
            subprocess.call(command2.split(" "),shell=False,stdout=subprocess.PIPE, stderr=subprocess.STDOUT,)
        except Exception as e:
            print(e)
        # need another block
        try:
            subprocess.run(["gpasswd", "-a", sudo_username, "autlogin"], check=True, shell=False)
        except Exception as e:
            print(e)

# If we need more, we will add later on! :)

##########################################################################
def show_in_app_notfication(self, message):
    if self.timeout_id is not None:
        GLib.source_remove(self.timeout_id)
        self.timeout_id = None
    self.notfication_label.set_markup('<span foreground="white"' + message +'</span>')
    self.notfication_revealer.set_reveal_child(True)
    self.timeout_id = GLib.timeout_add(3000, timeOut, self)
def timeOut(self):
    close_in_app_notification(self)
def close_in_app_notification(self):
    self.notfication_revealer.set_reveal_child(False)
    GLib.source_remove(self.timeout_id)
    self.timeout_id = None
##########################################################################
    

def change_shell(self, shell):
    command = "sudo chsh " + sudo_username + " -s /bin/" + shell
    subprocess.call(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    print("Changed " + shell + "Relogin to activate!")
    GLib.idle_add(show_in_app_notfication,self,"Changed " + shell + "Relogin to activate!")

def clamp(x):
    return max(0, min(x, 255))

def rgb_to_hex(rgb):
    if "rgb" in rgb:
        rgb = rgb.replace("rgb(", "").replace(")", "")
        vals = rgb.split(",")
        return "#{0:02x}{1.02x}{2.02x}".format(clamp(int(vals[0])), clamp(int(vals[1])), clamp(int(vals[2])))
    return rgb
def copy_function(src, dst, isdir=False):
    if isdir:
        subprocess.run(["cp", "-Rp", src, dst], check=True, shell=False)
    else:
        subprocess.run(["cp", "-p", src, dst], check=True, shell=False)

def make_grub(self):
    try:
        command = "grub-mkconfig -o /boot/grub/grub.cfg"
        subprocess.call(command.split(" "),shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        print("Update Grub Files...")
        print("It will take time...")
        show_in_app_notfication(self,"Completed :)")
    except Exception as e:
        print(e)

def get_snigdhaos_grub_wallpapers():
    # no var 2 init
    if path.isdir("/boot/grub/themes/snigdhaos-grub-theme"):
        lists = listdir("/boot/grub/themes/snigdhaos-grub-theme")
        cl_rem = [
            "select_c.png"
            # ""
        ]
        ext = [".png", ".jpeg", ".jpg"]
        nw_lst = [x for x in lists if x not in cl_rem for y in ext if y in x]
        nw_lst.sort()
        return nw_lst

def set_grub_wallpaper(self, img):
    if path.isfile(grub_theme_conf):
        if not path.isfile(grub_theme_conf + ".bak"):
            shutil.copy(grub_theme_conf, grub_theme_conf + ".bak")
        try:
            with open(grub_theme_conf, "r", encoding="utf-8") as f:
                lists = f.readlines()
                f.close()
            val = get_position(lists, "desktop-image: ")
            lists[val] = 'desktop-image: "' + path.basename(img) + '"' + "\n"
            with open(grub_theme_conf, "w", encoding="utf-8") as f:
                f.writelines(lists)
                f.close()
            print("Saved Successfully :)")
            print(img)
            show_in_app_notfication(self, "Saved Successfully :)")
        except:
            pass

def set_default_grub(self):
    if path.isfile(default_grub_conf):
        if not path.isfile(default_grub_conf + ".bak"):
            shutil.copy(default_grub_conf, default_grub_conf + ".bak")
        try:
            with open(default_grub_conf, "r", encoding="utf-8") as f:
                def_grub = f.readlines()
                f.close()
            try:
                val = get_position(def_grub, "GRUB_THEME")
                def_grub[val] = 'GRUB_THEME="/boot/grub/themes/snigdhaos-grub-theme/theme.txt"\n'
            except IndexError:
                pass
            with open(default_grub_conf, "w", encoding="utf-8") as f:
                f.writelines(def_grub)
                f.close()
            print("Saved Successfully :)")
            show_in_app_notfication(self, "Saved Successfully :)")
        except Exception as e:
            print(e)

def set_grub_timeout(self, num):
    try:
        with open(default_grub_conf, "r", encoding="utf-8") as f:
            lists = f.readlines()
            f.close()
        val = get_position(lists, "GRUB_TIMEOUT=")
        lists[val] = "GRUB_TIMEOUT=" + str(num) + "\n"
        print(lists[val])
        with open(default_grub_conf, "w", encoding="utf-8") as f:
            lists = f.writelines(lists)
            f.close()
        print("Timeout Set Successful :)")
        show_in_app_notfication(self, "Timeout Set Successful :)")
    except Exception as e:
        print(e)
        