# -*- coding: utf-8 -*-

from flask import Blueprint
from flask_restful import Api
from .support_view import *

restful = Blueprint('restful', __name__)
api = Api(restful)


api.add_resource(Register, '/register', endpoint='register')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(InitCap, '/initcap', endpoint='initcap')
api.add_resource(InstallCap, '/installcap', endpoint='installcap')
api.add_resource(DeleteCap, '/deletecap', endpoint='deletecap')
#api.add_resource(ListSupport, '/support/list')
#api.add_resource(AddSupport, '/support/add')
#api.add_resource(EditSupport, '/support/edit')
#api.add_resource(DeleteSupport, '/support/del')
