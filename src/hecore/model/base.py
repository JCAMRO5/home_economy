#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from functools import partial

from model import *
from hegui.login import Login

class Db:
    """Maneja las conexiones y model ode la base de datos con sqlalchemy"""
    app = None
    connection = None
    engine = None

    def __init__(self, app):
        self.app = app

    def connect(self, fileName=None):
        """Se conecta a la base de datos"""
        if not fileName:
            fileName = self.app.config.get('last_session', 'dbpath')
        cnnstr = "sqlite:///{}".format(fileName)
        print (cnnstr)
        self.engine = create_engine(cnnstr)
        DBSession = sessionmaker()
        DBSession.configure(bind=self.engine)
        session = DBSession()
        self.connection = session
        return True

    def create_db(self, fileName):
        """Crea la base de datos"""
        print ("creando la bd {}".format(fileName))
        DECLARATIVE_BASE.metadata.create_all(self.engine)

        # agrego un usuario llamado admin con clave admin
        hash = self.app.pwd_context.hash("admin")
        print(hash)
        id = str(uuid.uuid4())
        user = User(id=id, login='admin', password=hash, name='', surname='',
                    default_account='', password_type='default', state='A')
        self.connection.add(user)
        self.connection.commit()

        # TODO: agregar los registros iniciales como usuario principal y cuentas x defecto

    def no_action(self):
        pass

    def create_and_connect(self, fileName, loginText='', passwordText=''):
        if self.check_file_exists(fileName):
            self.get_connection()
        else:
            login = Login().make_db_and_finish_login
            strmsg = "La base de datos {} no existe, desea crearla?".format(fileName)
            self.app.open_popup(strmsg, action_yes=partial(login, loginText, passwordText, True, fileName),
            action_no=self.no_action)

    def create_and_connect_callback(self, fileName):
        self.connect(fileName)
        self.create_db(fileName)

    def get_connection(self):
        if self.connection:
            return self.connection
        else:
            return self.connect()

    def check_file_exists(self, filePath):
        return os.path.isfile(filePath)
