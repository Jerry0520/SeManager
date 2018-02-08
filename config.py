# -*- coding: utf-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))
class Config:

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # CSRF
    #CSRF_ENABLED = True
    SECRET_KEY = 'nrebojisvdjopsdjvdfbjdldfvsji'

    # Flask-User settings
    USER_APP_NAME = "Tech_Support"

    @staticmethod
    def init_app(app):
        pass


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.test.sqlite')
    WTF_CSRF_ENABLED = False
    
class DevelopingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.dev.sqlite')
    
class ProductConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')   

config = {
    'testing':TestingConfig,
    'developing':DevelopingConfig,
    'product':ProductConfig,
    'default':DevelopingConfig,
} 
    