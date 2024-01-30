##########################################################################
# Author : Eshan Roy <eshan@snigdhaos.org>
# URI: https://eshan.snigdhaos.org
# Lead Maintainer @ Snidgha OS
##########################################################################

# module imports
import gi
gi.require_version("Gtk", "3.0")

import os
from os import getlogin,makedirs,listdir, unlink, symlink, execl, rmdir, walk, getpid
from os import path
import psutil
import shutil
import subprocess
import datetime
from datetime import datetime
from gi.repository import Gtk, GLib
import sys


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

def get_position(lists, value):
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

def check_installed_package(package):
    try:
        subprocess.check_output("pacman -Qi " + package, shell=True, stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError:
        return False
    
def check_service(service):
    try:
        cmd = "systemctl is-active " + service + ".service"
        output = subprocess.run(cmd.split(" "),check=True,shell=False,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        status = output.stdout.decode().strip()
        if status == "active":
            return True
        else:
            return False
    except Exception:
        # print(e) # bool -> we don't need trace
        return False

def check_socket(socket):
    try:
        cmd = "systemctl is-active " + socket + ".socket"
        output = subprocess.run(cmd.split(" "),check=True,shell=False,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        status = output.stdout.decode().strip()
        if status == "active":
            return True
        else:
            return False
    except Exception:
        # print(e) # bool -> we don't need trace
        return False

def list_users(fname):
    try:
        data = []
        with open(fname, "r", encoding="utf-8") as f:
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
        groups = subprocess.run(["sh", "-c", "id " + sudo_username], shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
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

######## End Base Function

####### Start misc function
def copy_function(source, destination, isdir=False):
    if isdir:
        subprocess.run(["cp", "-Rp", source, destination], check=True, shell=False)
    else:
        subprocess.run(["cp", "-p", source, destination], check=True, shell=False)

log_directory = "/var/log/archlinux/"
sin_log_directory = "/var/log/archlinux/sin" 

def create_log(self):
    print("Creating Log 👀")
    now = datetime.datetime.now()
    time = now.strftime("%Y-%m-%d-%H-%M-%S")
    destination = sin_log_directory + "sin-log-" + time
    cmd = "sudo pacman -Q > " + destination
    subprocess.call(cmd, shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

def messagebox(self, title, message):
    md = Gtk.MessageDialog(parent=self, falgs=0, message_type = Gtk.MessageType.INFO, buttons = Gtk.ButtonsType.OK, text=title)
    md.format_secondary_markup(message)
    md.run()
    md.destroy()

def show_app_notification(self, message):
    if self.timeout_id is not None:
        GLib.source_remove(self.timeout_id)
        self.timeout_id = None
    self.notification_label.set_markup('<span foreground = "white">' + message + '</span>')
    self.notification_revealer.set_reveal_child(True)
    self.timeout_id = GLib.timeout_add(3000, timeOut, self)

def timeOut(self):
    close_app_notification()

def close_app_notification(self):
    self.notification_revealer.set_reveal_child(False)
    GLib.source_remove(self.timeout_id)
    self.timeout_id = None

def get_shortcuts(configlist):
    shortcuts = _get_variable(configlist, "shortcuts")
    shortcuts_index = get_position(configlist, shortcuts[0])
    return shortcuts_index

def get_commands(configlist):
    cmds = _get_variable(configlist, "commands")
    cmd_insdex = get_position(configlist, cmds[0])
    return cmd_insdex

def test(destination):
    for root, dirs, filesr in walk(destination):
        print(root)
        for folders in dirs:
            pass
            for file in filesr:
                pass
        for file in filesr:
            pass

def permission(destination):
    try:
        groups = subprocess.run(["sh", "-c", "id " + sudo_username], check=True,shell=False,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        for i in groups.stdout.decode().split(" "):
            if "gid" in i:
                j = i.split("(")[1]
                group = j.replace(")", "").strip()
        subprocess.call(["chown", "-R", sudo_username + ":" + group, destination], shell=False)
    except Exception as e:
        print(e)

def restart_snigdhaos_installer():
    if path.exists("/tmp/sin.lock"):
        unlink("/tmp/sin.lock")
        python = sys.executable
        execl(python, python, sys.argv)

def enable_service(service):
    try:
        cmd = "systemctl enable " + service + ".service -f -now"
        subprocess.call(cmd.split(" "),shell=False,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        print("Enabling Service: " + service + "😉")
    except Exception as e:
        print(e)

def restart_service(service):
    try:
        cmd = "systemctl reload-or-restart " + service + ".service"
        subprocess.call(cmd.split(" "),shell=False,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        print("Reloading: " + service + "😉")
    except Exception as e:
        print(e)

def disbale_service(service):
    try:
        cmd = "systemctl stop " + service
        subprocess.call(cmd.split(" "),shell=False,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        cmd = "systemctl disable " + service
        subprocess.call(cmd.split(" "),shell=False,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        print("Diabled: " + service + "😉")
    except Exception as e:
        print(e)

