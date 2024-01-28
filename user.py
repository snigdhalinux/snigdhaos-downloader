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