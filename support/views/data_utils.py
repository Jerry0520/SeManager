# -*- coding: utf-8 -*-
from flask import jsonify
from . import main


@main.route('/citylist', methods=['GET'])
def CityList():
    list_data = [
        {'label': u'天府通', 'value': 'Tianfutong'},
        {'label': u'广西一卡通', 'value': 'Guangxi'}
    ]
    return jsonify(code=0, msg=u'', data=list_data)


@main.route('/oemlist', methods=['GET'])
def OemList():
    list_data = [
        {'value': 'xiaomi', 'label': u'小米'},
        {'value': 'huawei', 'label': u'华为'},
        {'value': 'samsung', 'label': u'三星'},
        {'value': 'oneplus', 'label': u'一加'},
        {'value': 'meizu', 'label': u'魅族'}
    ]
    return jsonify(code=0, msg=u'', data=list_data)
