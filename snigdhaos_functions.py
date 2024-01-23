#####################################################################
# Author    : Eshan Roy <eshan@snigdhaos.org>                       #
# Web       : eshan.snigdhaos.org                                   #
# Lead Maintainer & Developer @ Snigdha OS!                         #
#####################################################################

import gi
import subprocess
import psutil
import shutil
import os
gi.require_version('Gtk', '3.0')
from os import path, getlogin, mkdir, makedirs, listdir, unlink
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

## Misc
backup = ".snigdhaos"

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
    return 0


def get_positions(lists, value):
    data = [string for string in lists if value in string]
    position = []
    for d in data:
        position.append(lists.index(d))
    return position


def _get_variable(lists, value):
    data = [string for string in lists if value in string]

    if len(data) >= 1:
        data1 = [string for string in data if "#" in string]

        for i in data1:
            if i[:4].find("#") != -1:
                data.remove(i)
    if data:
        data_clean = [data[0].strip("\n").replace(" ", "")][0].split("=")
    return data_clean


def check_value(list, value):
    data = [string for string in list if value in string]
    if len(data) >= 1:
        data1 = [string for string in data if "#" in string]
        for i in data1:
            if i[:4].find("#") != -1:
                data.remove(i)
    return data

def permissions(dst):
    try:
        groups = subprocess.run(
            ["sh", "-c", "id " + superuser],
            check=True,
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        for x in groups.stdout.decode().split(" "):
            if "gid" in x:
                g = x.split("(")[1]
                group = g.replace(")", "").strip()
        subprocess.call(["chown", "-R", superuser + ":" + group, dst], shell=False)
    except Exception as error:
        print(error)

def check_backups(now):
    if not path.exists(home + "/" + backup + "/Backup-" + now.strftime("%Y-%m-%d %H")):
        makedirs(home + "/" + backup + "/Backup-" + now.strftime("%Y-%m-%d %H"), 0o777)
        permissions(home + "/" + backup + "/Backup-" + now.strftime("%Y-%m-%d %H"))


def check_if_process_is_running(processName):
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=["pid", "name", "create_time"])
            if processName == pinfo["name"]:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


def copytree(self, src, dst, symlinks=False, ignore=None):  # noqa
    if not path.exists(dst):
        makedirs(dst)
    for item in listdir(src):
        s = path.join(src, item)
        d = path.join(dst, item)
        if path.exists(d):
            try:
                shutil.rmtree(d)
            except Exception as error:
                print(error)
                unlink(d)
        if path.isdir(s):
            try:
                shutil.copytree(s, d, symlinks, ignore)
            except Exception as error:
                print(error)
                print("ERROR2")
                self.ecode = 1
        else:
            try:
                shutil.copy2(s, d)
            except:  # noqa
                print("ERROR3")
                self.ecode = 1
            

def file_check(file):
    if path.isfile(file):
        return True

    return False


def path_check(path):
    if os.path.isdir(path):
        return True

    return False


def is_empty_directory(path):
    if os.path.exists(path) and not os.path.isfile(path):
        if not os.listdir(path):
            # print("Empty directory")
            return True
        else:
            # print("Not empty directory")
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


def check_package_installed(package):  # noqa
    try:
        subprocess.check_output(
            "pacman -Qi " + package, shell=True, stderr=subprocess.STDOUT
        )
        # package is installed
        return True
    except subprocess.CalledProcessError:
        # package is not installed
        return False

def check_service(service):  # noqa
    try:
        command = "systemctl is-active " + service + ".service"
        output = subprocess.run(
            command.split(" "),
            check=True,
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        status = output.stdout.decode().strip()
        if status == "active":
            # print("Service is active")
            return True
        else:
            # print("Service is inactive")
            return False
    except Exception:
        return False


def check_socket(socket):  # noqa
    try:
        command = "systemctl is-active " + socket + ".socket"
        output = subprocess.run(
            command.split(" "),
            check=True,
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        status = output.stdout.decode().strip()
        if status == "active":
            # print("Service is active")
            return True
        else:
            # print("Service is inactive")
            return False
    except Exception:
        return False


def list_users(filename):  # noqa
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
    except Exception as error:
        print(error)


def check_group(group):
    try:
        groups = subprocess.run(
            ["sh", "-c", "id " + superuser],
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        for x in groups.stdout.decode().split(" "):
            if group in x:
                return True
            else:
                return False
    except Exception as error:
        print(error)