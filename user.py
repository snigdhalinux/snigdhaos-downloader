##################################################################################
# Author: Eshan Roy <eshan@snigdhaos.org>
# URL : https://eshan.snigdhaos.org
# Lead Maintainer & Developer @ Snigdha OS
##################################################################################

import functions as fn
from functions import GLib

def create_user(self):
    """Create a new user"""
    username = self.hbox_username.get_text()
    name = self.hbox_name.get_text()
    atype = self.combo_account_type.get_active_text()
    password = self.hbox_password.get_text()
    confirm_password = self.hbox_confirm_password.get_text()

    if (len(username) > 0 and len(name) > 0 and len(password) > 0 and len(confirm_password) > 0):
        if password == confirm_password:
            user_password = "echo " + username + ":" + password
            try:
                command = "groupadd -r sambashare"
                fn.subprocess.call(command.split(" "),shell=False,stdout=fn.PIPE, stderr=fn.STDOUT,)
            except Exception as e:
                print(e)
            if password == confirm_password:
                if atype == "Administrator":
                    useradd = ('useradd -m -G audio,video,network,storage,rfkill,wheel,sambashare -c "' + name + '" -s /bin/bash ' + username)
                    fn.system(useradd)
                    fn.system(user_password + " | " + "chpasswd -c SHA512")
                else:
                    useradd = ('useradd -m -G audio,video,network,storage,rfkill,sambashare -c "' + name + '" -s /bin/bash ' + username)
                    fn.system(useradd)
                    fn.system(user_password + " | " + "chpasswd -c SHA512")
                print("User Created Successfully :)")
                GLib.idle_add(fn.show_in_app_notfication, self, "User Created Successfully :)")
            else:
                GLib.idle_add(fn.show_in_app_notfication, self, "Password Didn't match :(")
                GLib.messagebox(fn.show_in_app_notfication, self, "Password Didn't match :(")
    else:
        GLib.idle_add(fn.show_in_app_notfication, self, "Empty Fields :(")
        GLib.messagebox(fn.show_in_app_notfication, self, "Empty Fields :(")