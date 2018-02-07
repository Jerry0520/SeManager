# -*- coding: utf-8 -*-

from support import db

class ErrorLog(db.Model):
    __tablename__ = 'errorlog'
    
    id = db.Column(db.Integer, primary_key=True)
    user_cplc = db.Column(db.String(50), nullable=False)
    cap_aid = db.Column(db.String(50), nullable=False)
    cap_version = db.Column(db.String(20), nullable=False)
    log = db.Column(db.Text, nullable=False)
    
    def __repr__(self):
        return self.user_cplc