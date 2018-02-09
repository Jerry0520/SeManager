# -*- coding: utf-8 -*-
from flask_admin.contrib.sqla import ModelView
from support import admin, db
from support.models.users import User, Role, SupportInfo
from support.models.applets import CapPkgInfo, CapPerso, BlackList, WhiteList, CapCfg

class UserView(ModelView):
    
    # Disable model creation
    can_create = False
    can_delete = False
    can_edit = False   
    
    # Override displayed fields
    column_labels = {
        'id':'ID',
        'username':'用户名',
        'nickname':'昵称',
        'mobile':'手机号码',
        'active':'激活状态',
        'confirmed_at':'注册时间',
        'last_login_at':'最近登录',
        'login_count':'登录次数',
    }
    column_filters = ('id', 'username', 'nickname', 'mobile', 'active', 'confirmed_at', 'last_login_at', 'login_count')
    column_list = ('id', 'username', 'nickname', 'mobile', 'active', 'confirmed_at', 'last_login_at', 'login_count')
    
    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(UserView, self).__init__(User, session, **kwargs)
    

class RoleView(ModelView):
    
    # Disable model creation
    can_create = False
    can_delete = False
    can_edit = False   
    
    # Override displayed fields
    column_labels = {
        'id':'ID',
        'name':'角色名',
        'description':'描述',
    }
    column_filters = ('id', 'name', 'description')
    column_list = ('id', 'name', 'description')
    
    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(RoleView, self).__init__(Role, session, **kwargs)


class CapPkgInfoView(ModelView):
    # Disable model creation

    # Override displayed fields
    column_labels = {
    'id':'ID',
    'cap_name':'应用名称',
    'cap_version':'应用版本',
    'cap_perso':'应用指令',
    'cap_aid':'应用ID',
    }
    column_filters = ('id','cap_name','cap_version','cap_perso','cap_aid')
    column_list = ('id','cap_name','cap_version','cap_perso','cap_aid')

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(CapPkgInfoView, self).__init__(CapPkgInfo, session, **kwargs)


class CapPersoView(ModelView):
    # Disable model creation

    # Override displayed fields
    column_labels = {
    'id':'ID',
    'cplc':'终端标识',
    'status':'个人化状态',
    'cap_aid':'应用ID',
    }
    column_filters = ('id','cplc','status','cap_aid')
    column_list = ('id','cplc','status','cap_aid')

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(CapPersoView, self).__init__(CapPerso, session, **kwargs)


class BlackListView(ModelView):
    # Disable model creation

    # Override displayed fields
    column_labels = {
    'id':'ID',
    'cplc':'终端标识',
    'description':'描述',
    }
    column_filters = ('id','cplc','description')
    column_list = ('id','cplc','description')

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(BlackListView, self).__init__(BlackList, session, **kwargs)


class WhiteListView(ModelView):
    # Disable model creation

    # Override displayed fields
    column_labels = {
    'id':'ID',
    'cplc':'终端标识',
    'description':'描述',
    }
    column_filters = ('id','cplc','description')
    column_list = ('id','cplc','description')

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(WhiteListView, self).__init__(WhiteList, session, **kwargs)


class CapCfgView(ModelView):
    # Disable model creation

    # Override displayed fields
    column_labels = {
    'id':'ID',
    'cap_aid':'应用ID',
    'status':'应用状态',
    }
    column_filters = ('id','cap_aid','status')
    column_list = ('id','cap_aid','status')

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(CapCfgView, self).__init__(CapCfg, session, **kwargs)  

     
admin.add_view(UserView(db.session,name='用户管理'))
admin.add_view(RoleView(db.session,name='角色管理'))
admin.add_view(CapPkgInfoView(db.session,name='应用管理'))
admin.add_view(CapPersoView(db.session,name='个人化状态'))
admin.add_view(BlackListView(db.session,name='黑名单'))
admin.add_view(WhiteListView(db.session,name='白名单'))
admin.add_view(CapCfgView(db.session,name='应用状态管理'))
