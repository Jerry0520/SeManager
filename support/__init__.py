# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore
from flask_admin import Admin
from flask_restful import Api
from config import config

db = SQLAlchemy()
security = Security()
admin = Admin(name= '多应用TSM')

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    admin.init_app(app)

    from support import xadmin
    from support.views import main
    app.register_blueprint(main)
    
    #register restful api
    from .restful import restful
    app.register_blueprint(restful, url_prefix='/api')

    return app
