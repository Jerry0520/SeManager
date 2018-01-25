#-*- coding:utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore
from flask_admin import Admin
from flask_cors import CORS
from flask_excel import init_excel

db = SQLAlchemy()
security = Security()
admin = Admin(name= u'�˻�����')

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_name)
    db.init_app(app)

    return app
