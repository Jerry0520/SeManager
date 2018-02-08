# -*- coding:utf-8 -*-
import unittest
import json
from flask import current_app, url_for, jsonify
from support import create_app, db
from support.models.users import *
from support.models.applets import *
from test_data import *


class ApiTestCase(unittest.TestCase):
    def setUp(self):
        print("Init test！")
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        cap1 = CapPkgInfo(cap_name=dict_cap1['cap_name'], cap_version=dict_cap1['cap_version'], cap_perso=dict_cap1['cap_perso'], cap_aid=dict_cap1['cap_aid'])
        cap2 = CapPkgInfo(cap_name=dict_cap2['cap_name'], cap_version=dict_cap2['cap_version'], cap_perso=dict_cap2['cap_perso'], cap_aid=dict_cap2['cap_aid'])
        cap3 = CapPkgInfo(cap_name=dict_cap3['cap_name'], cap_version=dict_cap3['cap_version'], cap_perso=dict_cap3['cap_perso'], cap_aid=dict_cap3['cap_aid'])
        perso1 = CapPerso(cplc=dict_perso1['cplc'], status=dict_perso1['status'], cap_aid=dict_perso1['cap_aid'])
        black1 = BlackList(cplc=dict_black1['cplc'], description=dict_black1['description'])
        cfg1 = CapCfg(cap_aid=dict_cfg1['cap_aid'], status=dict_cfg1['status'])
        db.session.add_all([cap1, cap2, cap3, perso1, black1, cfg1])
        db.session.commit()
        self.client = self.app.test_client()

    def tearDown(self):
        print("close worker!")
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    #check_data
    def test_01(self):
        print("01:check data!")
        capList = CapPkgInfo.query.all()
        self.assertIsNotNone(capList)
        perso1 = CapPerso.query.first()
        self.assertEqual(perso1.cplc, dict_perso1['cplc'])
        black1 = BlackList.query.first()
        self.assertEqual(black1.cplc, dict_black1['cplc'])
        cfg1 = CapCfg.query.first()
        self.assertIsNotNone(cfg1)

    #check_register
    def test_02(self):
        print("02:check register!")
        response = self.client.post(url_for('restful.register'), 
                                    content_type='application/json', 
                                    data=json.dumps({
                                        "username":"Andy",
                                        "mobile":"13312341234",
                                        "password":"12345678",
                                    }))
        self.assertTrue(response.status_code == 200)
        response = self.client.post(url_for('restful.register'), 
                                    content_type='application/json', 
                                    data=json.dumps({
                                        "username":"Andy",
                                        "mobile":"13312341234",
                                        "password":"12345678",
                                    }))
        self.assertTrue(response.status_code == 400)

    #check login
    def test_03(self):
        print("03:check login!")
        response = self.client.post(url_for('restful.login'),
                                    content_type='application/json', 
                                    data=json.dumps({
                                        "username":"Andy",
                                        "password":"12345678",
                                    }))
        print(response.data)
        self.assertTrue(response.status_code == 200)
        self.token = response.data.decode()['token']
        self.assertIsNotNone(self.token)
                                    

    #check init key
    def test_04(self):
        print("04:check init key!")

    #check down cap
    def test_05(self):
        print("04:check down cap!")

    #check delete cap
    def test_04(self):
        print("04:check delete cap!")
        