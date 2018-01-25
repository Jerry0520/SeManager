#-*- coding:uft-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = True

# ASSET包管理模式配置
ASSETS_DEBUG = False

# 配置CSRF
CSRF_ENABLED = True
SECRET_KEY = 'nrebojisvdjopsdjvdfbjdldfvsji'

# 允许追踪 login activities
SECURITY_TRACKABLE = True
# 密码加密存储
SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
SECURITY_PASSWORD_SALT = 'nrebojisvdjopsdjvdfbjdldfvsji'
PASSWORD_SINGLE_HASH=False
# 允许注册 register，暂不需要邮件确认
SECURITY_REGISTERABLE = True
SECURITY_SEND_REGISTER_EMAIL = False

# Flask-User settings
USER_APP_NAME = "Tech_Support"