# -*- coding:utf-8 -*-
from datetime import datetime
from .. import db

    
class CapPkgInfo(db.Model):
    __tablename__ = 'cappkginfo'
    
    id = db.Column(db.Integer, primary_key=True)
    cap_name = db.Column(db.String(100), nullable=False)
    cap_version = db.Column(db.String(20), nullable=False)
    cap_perso = db.Column(db.String(1000), nullable=False)
    cap_aid = db.Column(db.String(100))
    
class CapPerso(db.Model):
    __tablename__ = 'capperso'
    
    id = db.Column(db.Integer, primary_key=True)
    cplc = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(10), default='')
    cap_aid = db.Column(db.String(100))
     
class BlackList(db.Model):
    __tablename__ = 'blacklist'
    
    id = db.Column(db.Integer, primary_key=True)
    cplc = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    
    
class WhiteList(db.Model):
    __tablename__ = 'whitelist'
    
    id = db.Column(db.Integer, primary_key=True)
    _cplc = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    
    
class CapCfg(db.Model):
    __tablename__ = 'capcfg'
    
    id = db.Column(db.Integer, primary_key=True)
    cap_aid = db.Column(db.String(50), nullable=False, unique=True)
    status = db.Column(db.String(2), default='')