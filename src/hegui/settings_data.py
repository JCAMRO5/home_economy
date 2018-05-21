# -*- coding: utf-8 -*-

import json
import os
import random
import string
from kivy.app import App
from kivy.uix.settings import SettingString
from kivy.uix.label import Label
from kivy.config import ConfigParser

from hecore.crypt_functions import AESCipher, password_file

# ver https://gist.github.com/kived/610386b5181219622e33 para entry tipo password

settings_data = {
    "Session Settings": json.dumps([
        {"type": "path",
         "title": "database",
         "desc": "Path to the database to use to store data.",
         "section": "last_session",
         "key": "dbpath"
         },
        {"type": "bool",
         "title": "keep me logged in",
         "desc": "If you switch on this option, you will automatically login.",
         "section": "last_session",
         "key": "keeplogged"
         },
        {"type": "path",
         "title": "password filename",
         "desc": "Path to the file to use to store password for encrypted ini settings.",
         "section": "last_session",
         "key": "pwd_filename"
         },
    ]),
    "Email Parser Settings": json.dumps([
        {"type": "string",
         "title": "mail account",
         "desc": "Specify the mail account for the email parsing plugins.",
         "section": "mail_parser",
         "key": "email"
         },
        {"type": "password",
         "title": "mail password",
         "desc": "Specify the mail password for the email parsing plugins.",
         "section": "mail_parser",
         "key": "password"
         }
    ]),
}


# this classes are for using a password field in settings
class SettingPassword(SettingString):
    def _create_popup(self, instance):
        super(SettingPassword, self)._create_popup(instance)
        self.textinput.password = True

    def _validate(self, instance):
        self._dismiss()
        value = self.textinput.text.strip()
        pwd_text = password_file().get(self._get_pw_path())
        aci = AESCipher(pwd_text, 32)
        self.value = aci.encrypt(value)
        print(self.value)  # Just for debugging

    def add_widget(self, widget, *largs):
        if self.content is None:
            super(SettingString, self).add_widget(widget, *largs)
        if isinstance(widget, PasswordLabel):
            return self.content.add_widget(widget, *largs)

    def _get_pw_path(self):
        app = App.get_running_app()
        pwpath = app.config.get('last_session', 'pwd_filename')
        if not os.path.isfile(pwpath):
            Config = ConfigParser.get_configparser("kivy")
            folder = os.path.dirname(Config.filename)
            rand_name = self._get_random_chars(10)
            pwpath = os.path.join(folder, rand_name)
            app.config.set('last_session', 'pwd_filename', pwpath)
        return pwpath

    def _get_random_chars(self, lenght):
        return ''.join(random.choice(string.ascii_letters) for x in range(lenght))


class PasswordLabel(Label):
    pass