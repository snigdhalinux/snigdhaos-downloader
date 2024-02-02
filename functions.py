##########################################################################
# Author : Eshan Roy <eshan@snigdhaos.org>
# URI: https://eshan.snigdhaos.org
# Lead Maintainer @ Snidgha OS
##########################################################################

# module imports
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib

import os
from os import getlogin,makedirs,listdir, unlink, symlink, execl, rmdir, walk, getpid
from os import path
import threading
import psutil
import shutil
import subprocess
import datetime
from datetime import datetime
import sys
import time
import logging


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

# End Base Function

# Start misc function
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

def clamp(i):
    return max(0, min(i, 255))

def rgb2hex(rgb):
    if "rgb" in rgb:
        rgb = rgb.replace("rgb(", "").replace(")", "")
        values = rgb.split(",")
        return "#regex".format(clamp(int(values[1])), clamp(int(values[2])))
    return rgb

def change_shell(self, shell):
    cmd = "sudo chsh " + sudo_username + " -s /bin/" + shell
    subprocess.call(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    print("Shell Changed: " + shell + "Relogin to activate!")
    GLib.idle_add(show_app_notification,self,"Shell Changed: " + shell + "Relogin to activate!")

def source_shell(self):
    process = subprocess.run(["sh", "-c", 'echo "$SHELL"'], check=True, stdout=subprocess.PIPE)
    output = process.stdout.decode().strip()
    if output == "/bin/bash":
        subprocess.run(["bash","-c","su - " + sudo_username + ' -c "source ' + home + '/.bashrc"',], check=True, stdout=subprocess.PIPE)
    elif output == "/bin/fish":
        subprocess.run(["fish","-c","su - " + sudo_username + ' -c "source ' + home + '/.config/fish/config.fish"',], check=True, stdout=subprocess.PIPE)
    elif output == "/bin/zsh":
        subprocess.run(["zsh","-c","su - " + sudo_username + ' -c "source ' + home + '/.zshrc"',], check=True, stdout=subprocess.PIPE)

def get_shell():
    try:
        process = subprocess.run(["su", "-", sudo_username, "-c", 'echo "$SHELL"'], check=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = process.stdout.decode().strip().strip("\n")
        if output in ("/bin/bash", "/usr/bin/bash"):
            return "bash"
        elif output in ("/bin/zsh", "/usr/bin/zsh"):
            return "zsh"
        elif output in ("/bin/fish", "/usr/bin/fish"):
            return "fish"
    except Exception as e:
        print(e)
def run_as_user(script):
    subprocess.call(["su - " + sudo_username + " -c " + script], shell=False)

def is_thread_alive(thread_name):
    for thread in threading.enumerate():
        if thread.name == thread_name and thread.is_alive():
            return True
    return False

def _add_pacmanlog_queue(self):
    logger = logging.getLogger("logger")
    pacman_logfile = "/var/log/pacman.log"
    try:
        lines = []
        with open(pacman_logfile, "r", encoding="utf-8") as f:
            while True:
                line = f.readline()
                if line:
                    lines.append(line.encode("utf-8"))
                    self.pacmanlog_queue.put(lines)
                else:
                    time.sleep(0.5)
    except Exception as e:
        # print(e)
        logger.error("Exception in add_pacmanlog_queue() : %s" %e)
    finally:
        logger.debug("No new lines found inside the pacman log file")

def _update_tv_plog(self, tb_plog, tv_plog):
    lines = self.pacmanlog_queue.get()
    logger = logging.getLogger("logger")
    try:
        if len(lines) > 0:
            end_iter = tb_plog.get_end_iter()
            for line in lines:
                if len(line) > 0:
                    tb_plog.insert(
                        end_iter,
                        line.decode("utf-8"),
                        len(line),
                    )

    except Exception as e:
        logger.error("Exception in update_tv_plog() : %s" % e)
    finally:
        self.pacmanlog_queue.task_done()
        if len(lines) > 0:
            text_mark_end = tb_plog.create_mark("END", tb_plog.get_end_iter(), False)
            tv_plog.scroll_mark_onscreen(text_mark_end)
        lines.clear()

def _start_log_timer(self, tb_plog, tv_plog):
    while True:
        if self.start_logtimer is False:
            break
        GLib.idle_add()

# End Misc Functions

# GRUB

def make_grub(self):
    try:
        cmd = "grub-mkconfig -o /boot/grub/grub.cfg"
        subprocess.call(cmd.split(" "), shell=False,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        print("Updating Grub...🖕🏻")
        print("It will Take Time!")
        show_app_notification(self,"Updated Successfully👶🏻")
    except Exception as e:
        print(e)

def get_snigdhaos_grub_wallpaper():
    if path.isdir("/boot/grub/themes/snigdhaos-grub-theme"):
        lists = listdir("/boot/grub/themes/snigdhaos-grub-theme")
        rems = [
            "select" #rcsx2b
        ]
        extensions = [".png", "jpeg", "jpg"]
        re_list = [i for i in lists if i not in rems for j in extensions if j in i]
        re_list.sort()
        return re_list
    
grub_theme_config = ""
def set_snigdhaos_grub_wallpaper(self, image):
    if path.isfile(grub_theme_config):
        if not path.isfile(grub_theme_config + ".bak"):
            shutil.copy(grub_theme_config, grub_theme_config + ".bak")
        try:
            with open(grub_theme_config, "r", encoding="utf-8") as f:
                lists = f.readlines()
                f.close()
            value = get_position(lists, "desktop-image: ")
            lists[value] = 'desktop-image: "' + path.basename(image) + '"' + "\n"
            with open(grub_theme_config, "w", encoding="utf-8") as f:
                f.writelines(lists)
                f.close()
            print("Grub Wallpaper Has Been Set!")
            print(image)
            show_app_notification(self,"Grub Wallpaper Has Been Set!")
        except:
            pass

default_grub_config = ""
def set_snigdhaos_defualt_grub(self):
    if path.isfile(default_grub_config + ".bak"):
        shutil.copy(default_grub_config, default_grub_config + ".bak")
    try:
        with open(default_grub_config, "r", encoding="utf-8") as f:
            lists = f.readlines()
            f.close()
        try:
            value2 = get_position(lists, "GRUB_THEME=")
            lists[value2] = 'GRUB_THEME="/boot/grub/themes/snigdhaos-grub-theme/theme.txt"\n'
        except IndexError:
            pass
        with open(default_grub_config, "w", encoding="utf-8") as f:
            f.writelines(lists)
            f.close()
        print("Bump -> Snigdha OS Default Grub Theme")
        show_app_notification(self,"Bump -> Snigdha OS Default Grub Theme")
    except Exception as e:
        print(e)

defautl_grub_timeout = ""
def set_grub_timeout(self, num):
    try:
        with open(defautl_grub_timeout, "r", encoding="utf-8") as f:
            lists = f.readlines()
            f.close()
        value = get_position(lists, "GRUB_TIMEOUT=")
        lists[value] = "GRUB_TIMEOUT=" + str(num) +"\n"
        print(lists[value])
        with open(defautl_grub_timeout, "w", encoding="utf-8") as f:
            f.writelines(lists)
            f.close()
        print("Grub Time Out: " + num + "s")
        show_app_notification(self,"Grub Time Out: " + num + "s")
    except Exception as e:
        print(e)

# end grub :) ->

def install_packages(self, package):
    command = "pacman -S " + package + " --noconfirm --needed"
    if check_installed_package(package):
        print(package + "already installed!")
        GLib.idle_add(show_app_notification,self,package + " already installed!")
    else:
        try:
            print(command)
            subprocess.call(command.split(" "),shell=False,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            print(package + "installed successfully!")
            GLib.idle_add(show_app_notification,self,package + " installed successfully!")
        except Exception as e:
            print(e)

def install_local_packages(self, package):
    command = "pacman -U " + package + " --noconfirm --needed"
    if check_installed_package(package):
        print(package + "already installed!")
        GLib.idle_add(show_app_notification,self,package + " already installed!")
    else:
        try:
            print(command)
            subprocess.call(command.split(" "),shell=False,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            print(package + "installed successfully!")
            GLib.idle_add(show_app_notification,self,package + " installed successfully!")
        except Exception as e:
            print(e)

def install_snigdhaos_package(self, package):
    command = "pacman -S " + package + " --noconfirm --needed"
    if check_installed_package(package):
        print(package + "already installed!")
        GLib.idle_add(show_app_notification,self,package + " already installed!")
    else:
        try:
            print(command)
            subprocess.call(command.split(" "),shell=False,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            print(package + "installed successfully!")
            GLib.idle_add(show_app_notification,self,package + " installed successfully!")
        except Exception as e:
            print(e)

def remove_package(self, package):
    command = "pacman -R " + package + " --noconfirm"
    if check_installed_package(package):
        print(command)
        # GLib.idle_add(show_app_notification,self,package + " already installed!")
        try:
            print(command)
            subprocess.call(command.split(" "),shell=False,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            print(package + "removed successfully!")
            GLib.idle_add(show_app_notification,self,package + " removed successfully!")
        except Exception as e:
            print(e)
    else:
        print(package + " already removed!")
        GLib.idle_add(show_app_notification, self, package + " already removed!")

def remove_package_rs(self, package):
    command = "pacman -Rs " + package + " --noconfirm"
    if check_installed_package(package):
        print(command)
        # GLib.idle_add(show_app_notification,self,package + " already installed!")
        try:
            print(command)
            subprocess.call(command.split(" "),shell=False,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            print(package + "removed successfully!")
            GLib.idle_add(show_app_notification,self,package + " removed successfully!")
        except Exception as e:
            print(e)
    else:
        print(package + " already removed!")
        GLib.idle_add(show_app_notification, self, package + " already removed!")

def remove_package_rss(self, package):
    command = "pacman -Rss " + package + " --noconfirm"
    if check_installed_package(package):
        print(command)
        # GLib.idle_add(show_app_notification,self,package + " already installed!")
        try:
            print(command)
            subprocess.call(command.split(" "),shell=False,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            print(package + "removed successfully!")
            GLib.idle_add(show_app_notification,self,package + " removed successfully!")
        except Exception as e:
            print(e)
    else:
        print(package + " already removed!")
        GLib.idle_add(show_app_notification, self, package + " already removed!")

def remove_package_rdd(self, package):
    command = "pacman -Rdd " + package + " --noconfirm"
    if check_installed_package(package):
        print(command)
        # GLib.idle_add(show_app_notification,self,package + " already installed!")
        try:
            print(command)
            subprocess.call(command.split(" "),shell=False,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            print(package + "removed successfully!")
            GLib.idle_add(show_app_notification,self,package + " removed successfully!")
        except Exception as e:
            print(e)
    else:
        print(package + " already removed!")
        GLib.idle_add(show_app_notification, self, package + " already removed!")

def enable_login_manager(self, loginmanager):
    command = "systemctl enable " + loginmanager + ".service -f"
    if check_installed_package(loginmanager):
        try:
            print(command)
            subprocess.call(command.split(" "), shell=False,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            print(loginmanager + " has been activated - reboot system!")
            GLib.idle_add(show_app_notification,self,loginmanager + " has been activated - reboot system!")
        except Exception as e:
            print(e)
            # GLib.idle_add(show_app_notification, self, loginmanager + " is not installed!")
    else:
        print(loginmanager + " not installed!")
        GLib.idle_add(show_app_notification, self, loginmanager + " is not installed!")

# def set_login_wallpaper(self, wallpaper):


def auto_login_group(self):
    command = subprocess.run(["sh", "-c", "su - " + sudo_username + " -c groups"], check=True, shell=False, stdout=subprocess.PIPE)
    groups = command.stdout.decode().strip().split(" ")
    if "autologin" not in groups:
        try:
            subprocess.call(command.split(" "), shell= False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except Exception as e:
            print(e)
        try:
            subprocess.run(["gpasswd", "-a", sudo_username, "autologin"], check=True, shell=False)
        except Exception as e:
            print(e)