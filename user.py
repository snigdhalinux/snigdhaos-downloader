# Author : Eshan Roy <esha@snigdhaos.org>

import functions as fn
from functions import GLib

def create_user(self):
    username = self.hbox_username.get_text()
    name = self.hbox_name.get_text()
    actype = self.combo_account_type.get_active_text()
    password = self.hbox_password().get_text()
    confirm_password = self.hbox_confirm_password().get_text()
