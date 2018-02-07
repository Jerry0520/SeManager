# -*- coding: utf-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = False

# CSRF
#CSRF_ENABLED = True
SECRET_KEY = 'nrebojisvdjopsdjvdfbjdldfvsji'

# salt
SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
SECURITY_PASSWORD_SALT = 'nrebojisvdjopsdjvdfbjdldfvsji'
PASSWORD_SINGLE_HASH=False
# ����ע�� register���ݲ���Ҫ�ʼ�ȷ��
SECURITY_REGISTERABLE = True
SECURITY_SEND_REGISTER_EMAIL = False

# Flask-User settings
USER_APP_NAME = "Tech_Support"