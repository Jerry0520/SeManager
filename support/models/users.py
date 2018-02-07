# -*- coding: utf-8 -*-

from flask import current_app
from datetime import datetime
from flask_security import UserMixin, RoleMixin
from itsdangerous import TimedJSONWebSignatureSerializer
from werkzeug.security import generate_password_hash, check_password_hash
from flask_httpauth import HTTPTokenAuth
from support import db


auth = HTTPTokenAuth()

roles_users = db.Table('roles_users',
                       db.Column('users', db.Integer, db.ForeignKey('user.id')),
                       db.Column('roles', db.Integer, db.ForeignKey('role.id')))


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    nickname = db.Column(db.String(50), nullable=False, default='')
    password_hash = db.Column(db.String(255), nullable=False)
    mobile = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=1)
    confirmed_at = db.Column(db.DateTime(), default=datetime.now())
    last_login_at = db.Column(db.DateTime())
    login_count = db.Column(db.Integer, default=0)

    roles = db.relationship('Role', secondary='roles_users', backref=db.backref('user', lazy='dynamic'))

    def __str__(self):
        return self.username
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def generate_auth_token(self, expiration= 6000):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'], expires_in= expiration)
        return s.dumps({"username":self.username})
    
    @auth.verify_token
    def verify_auth_token(token):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        data_username = User.query.filter_by(username= data['username']).first()
        if data_username ==None:
            return False
        return True

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class SupportInfo(db.Model):
    issue_no = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.DateTime(), nullable=False)
    oem_vendor = db.Column(db.String(64), nullable=False)
    device_model = db.Column(db.String(64))
    sp_id = db.Column(db.String(16), nullable=False)
    environment = db.Column(db.String(64), nullable=False)
    issue_trace = db.Column(db.String(128), nullable=False)
    message = db.Column(db.String(1000))
    module_name = db.Column(db.String(128))
    handle_person = db.Column(db.String(64))
    description = db.Column(db.String(1000))
    status = db.Column(db.String(3))
    reason = db.Column(db.String(1000))
    solution = db.Column(db.String(1000))
    advice = db.Column(db.String(1000))
    notes = db.Column(db.String(1000))
    jira = db.Column(db.String(256))

    def __str__(self):
        return self.issue_no
