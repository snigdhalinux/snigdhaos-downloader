# Author : Eshan Roy <esha@snigdhaos.org>

import functions as fn
from functions import GLib

def create_user(self):
    username = self.hbox_username.get_text()
    name = self.hbox_name.get_text()
    actype = self.combo_account_type.get_active_text()
    password = self.hbox_password().get_text()
    confirm_password = self.hbox_confirm_password().get_text()

    if (
        len(username) > 0 and len(name) > 0 and len(password) > 0 and len(confirm_password) > 0
    ):
        if password == confirm_password:
            user_pass = "echo " + username + ":" + password
            try:
                command = "groupadd -r sambashare"
                fn.subprocess.call(command.split(" "), shell=False,stdout=fn.subprocess.PIPE, stderr=fn.subprocess.STDOUT,)
            except Exception as e:
                print(e)
            
            if password == confirm_password:
                if actype == "Administrator":
                    useradd = ('useradd -m -G audio, video,network,storage,rfkill,wheel,smabashare -c "' + name + '" -s /bin/bash ' + username)
                    fn.system(useradd)
                    fn.system(user_pass + " | " + "chpasswd -c SHA512")
                    print("User Created Successfully!")
                    GLib.idle_add(fn.show_app_notification, self, "User Created Successfully!")
                else:
                    fn.show_app_notification(self, "Password Didn't Match!")
                    fn.messagebox(self, "Message", "Password Didn't Match!")
            else:
                fn.show_app_notification(self, "Fill All The Fields!")
                fn.messagebox(self, "Message", "Fill All The Fields!")

def on_click_delete_all_user(self):
    username = self.cbt_users.get_active_text()
    if username is not None:
        userdel = "userl -r -f " + username
        fn.system(userdel)
        print("User Deleted Successfully!")
        GLib.idle_add(fn.show_app_notification, self, "User Deleted Successfully!")

def pop_cbt_users(self, combo):
    combo.get_model().clear()
    users = fn.list_users("/etc/passwd")
    for user in users:
        self.cbt_users.append_text(user)
        self.cbt_users.set_active(0) 