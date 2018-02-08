# -*- coding: utf-8 -*-
from flask import jsonify
from . import main


@main.route('/citylist', methods=['GET'])
def CityList():
    list_data = [
        {'label': '天府通', 'value': 'Tianfutong'},
        {'label': '广西一卡通', 'value': 'Guangxi'}
    ]
    return jsonify(code=0, msg='', data=list_data)


@main.route('/oemlist', methods=['GET'])
def OemList():
    list_data = [
        {'value': 'xiaomi', 'label': '小米'},
        {'value': 'huawei', 'label': '华为'},
        {'value': 'samsung', 'label': '三星'},
        {'value': 'oneplus', 'label': '一加'},
        {'value': 'meizu', 'label': '魅族'}
    ]
    return jsonify(code=0, msg='', data=list_data)
