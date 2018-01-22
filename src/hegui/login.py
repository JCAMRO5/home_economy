#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from hegui.mainscreen import MainPanel

class Login(BoxLayout):
    def do_login(self, loginText, passwordText):
        app = App.get_running_app()

        app.username = loginText
        app.password = passwordText

        if app.runserver:
            from twisted.internet import reactor
            from hesync.hesync import EchoServerFactory
            reactor.listenTCP(8000, EchoServerFactory(self))

        app._switch_main_page('MainPanel', MainPanel)

        #app.config.read(app.get_application_config())
        #app.config.write()

    def resetForm(self):
        self.ids['login'].text = ""
        self.ids['password'].text = ""


class PaginaCuentas(BoxLayout):
    pass