# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore
from flask_admin import Admin
from flask_restful import Api

db = SQLAlchemy()
security = Security()
admin = Admin(name= u'多应用TSM')

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_name)
    db.init_app(app)

    from support.views import main
    app.register_blueprint(main)
    
    #register restful api
    from .restful import restful
    app.register_blueprint(restful, url_prefix='/api')

    return app
