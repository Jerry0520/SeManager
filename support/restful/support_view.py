# -*- coding: utf-8 -*-
from flask import jsonify, session
from flask_restful import Resource, marshal_with, fields, reqparse
from ..models.users import User, Role, SupportInfo
from ..models.applets import CapPerso, CapPkgInfo, BlackList, WhiteList, CapCfg
from .. import db
from ..utils.contants import dict_isd_key, dict_perso_status, dict_cap_status
from support.utils.gp.GlobalPlatform import gp
from binascii import hexlify, unhexlify

gp = gp()

#response serializer
api_fields = {
    "APDUList": fields.String()
}

class Register(Resource):
    
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type= str, location= 'json')
        self.reqparse.add_argument('mobile', type= str, location= 'json')
        self.reqparse.add_argument('password',type=str, location= 'json')
        super(Register, self).__init__()
        
    def post(self):
        args = self.reqparse.parse_args()
        username = User.query.filter_by(username=args['username']).first()
        if username:
            message = {
                "message": "username is exist"
            }
            return message,400
        
        user = User(username=args['username'], password=args['password'], mobile=args['mobile'])
        db.session.add(user)
        db.session.commit()
        message = {
            "username": args['username'],
            "mobile": args['mobile'],  
        }
        return message,200
    

class Login(Resource):
    
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type= str, location= 'json')
        self.reqparse.add_argument('password',type=str, location= 'json')
        super(Login, self).__init__()        

    def post(self):
        args = self.reqparse.parse_args()
        user = User.query.filter_by(username=args['username']).first()
        if not user:
            message = {
                "message": "username is not exist,please regist at first"
            }
            return message,400
        if not user.verify_password(args['password']):
            message = {
                "message": "bad password"
            }
            return message,400
        token = user.generate_auth_token()
        data = {
            "token": token.decode('ascii')
        }
        return data,200
    

class InitCap(Resource):
    
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('cplc', type=str, location='json')
        self.reqparse.add_argument('initdata',type=str, location='json')
        super(InitCap, self).__init__()
        
    def post(self):
        args = self.reqparse.parse_args()
        cplc = BlackList.query.filter(BlackList.cplc==args['cplc']).first()
        if cplc:
            message = {
                "message": "in Blacklist"
            }
            return message,400
        response = args['initdata']
        
        KENC, KMAC, KDEK = gp.initkey(args['cplc'])
        hostCryptogram, S_ENC, S_DEK, S_MAC = gp.gpexternalauthenticate(response, KENC, KMAC, KDEK)
        eaAPDU = gp.externalauthenticateCommad(P1='01', P2='00', DATA=hostCryptogram, random='0000000000000000', DES3key=S_MAC)
        seri_data = {
            "APDUList": eaAPDU
        }
        session["cplc"] = args["cplc"]
        #session["KENC"] = S_ENC
        #session["KDEK"] = S_DEK
        session["KMAC"] = S_MAC
        session["initdata"] = gp.sessionkey(eaAPDU[-16:], S_MAC[:16])
        return seri_data, 200
            
            
class InstallCap(Resource):
    
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('cplc', type=str, location='json')
        self.reqparse.add_argument('sw', type=str, location='json')
        self.reqparse.add_argument('app', type=str, location='json')
        super(InstallCap, self).__init__()
        
    def post(self):
        args = self.reqparse.pars_args()
        cplc = BlackList.query.filter_by(_cplc=args['cplc']).first()
        if cplc:
            message = {
                "message": "in Blacklist"
            }
            return message,400
        
        if args['cplc'] != session["cplc"]:
            message = {
                    "message": "please initcap at first"
                }
            return message,400 
        elif args[sw] != '9000':
            message = {
                        "message": "init Error"
                    }
            return message,400            
        cplc = CapPerso.query.filter_by(cplc=args['cplc'])
        for item_cplc in cplc:
            if item_cplc.cap_aid == args["app"]:
                if item_cplc.status == 1:
                    message = {
                        "message": dict_perso_status[1]
                    }
                    return message,400
                elif item_cplc.status == 2:
                    #个人化异常，走异常流程，待完善
                    return 0
            else:
                capList = CapPkgInfo.query.filter_by(cap_aid=args["app"]).order_by(CapPkgInfo.cap_version.desc()).first()
                APDU = capList.split(',')[:-1]
                gp = gp()
                apduList = []
                for subAPDU in APDU:
                    temp = gp.adpumac(session["initdata"], subAPDU, session["KMAC"])
                    apduList.append(temp)
                    
                seri_data = {
                    "APDUList": apduList
                }
                return seri_data, 200
                
                

class DeleteCap(Resource):
    
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self. reqparse.add_argument('cplc', type=str, location='json')
        self.reqparse.add_argument('app', type=str, location='json')
        self.reqparse.add_argument('sw', type=str, location='json')
        super(DeleteCap, self).__init__()
        
    def post(self):
        args = self.reqparse.parsr_args()
        cplc = BlackList.query.filter_by(_cplc=args['cplc']).first()
        if cplc:
            message = {
                "message": "in Blacklist"
            }
            return message,400
        
        if args['cplc'] != session["cplc"]:
            message = {
                    "message": "please initcap at first"
                }
            return message,400 
        elif args[sw] != '9000':
            message = {
                        "message": "init Error"
                    }
            return message,400            
        cplc = CapPerso.query.filter_by(cplc=args['cplc'])
        for item_cplc in cplc:
            if item_cplc.cap_pkg_info == args["app"]&item_cplc.status == 1:
                gp = gp()
                apduList = []
                command = gp.deleteCommand(P1='00', P2='80', AID=args['app'],random=session['initdata'], DES3key=session['KMAC'])
                apduList.append(command)
                seri_data = {
                    "APDUList": apduList
                }
                return seri_data, 200                
            else:
                message = {
                    "message": "个人化状态异常"
                }
                return message,400
                    

"""
#response serializer
api_fields_list_support = {
    'issueNo': fields.String(),
    'createTime': fields.String(),
    'oemVendor': fields.String(),
    'deviceModel': fields.String(),
    'spId': fields.String(),
    'environment': fields.String(),
    'issueTrace': fields.String(),
    'message': fields.String(),
    'moduleName': fields.String(),
    'handlePerson': fields.String(),
    'description': fields.String(),
    'status': fields.String(),
    'reason': fields.String(),
    'solution': fields.String(),
    'advice': fields.String(),
    'notes': fields.String(),
    'jira': fields.String(),   
}


class ListSupport(Resource):
    #serializer请求数据
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('description', type=str, help='No description', location='json')
        self.reqparse.add_argument('page', type=int, help='No page', location='json')
        self.reqparse.add_argument('perPage', type=int, help='No perPage', location='json')
        super(ListSupport, self).__init__()
        
    #对输出字段serializer
    @marshal_with(api_fields_list_support)
    def post(self):
        #初始化数据，拿到SupportInfo句柄
        args = self.reqparse.parse_args()
        print(args['description'])
        handle = db.session.query(SupportInfo)
        #判断description，并按照该字段模糊查询进行分页
        if args['description'] !='':
            handle = handle.filter(SupportInfo.description.like(args['description']))
        handle = handle.order_by(SupportInfo.create_time.desc())
        handle = handle.paginate(args['page'],args['perPage'])
        
        #取分页结果
        list_models = handle.items
        total_page = handle.total
        
        res_data = []
        #循环将要response的数据
        for item in list_models:
            #分割module名称存为列表
            list_module_name = []
            if item.module_name != '':
                list_module_name = item.module_name.split(',')
                #初始化response json数据
                dict_data = {
                    'issueNo': item.issue_no,
                    'createTime': item.create_time,
                    'oemVendor': item.oem_vendor,
                    'deviceModel': item.device_model,
                    'spId': item.sp_id,
                    'environment': item.environment,
                    'issueTrace': item.issue_trace,
                    'message': item.message,
                    'moduleName': list_module_name,
                    'handlePerson': item.handle_person,
                    'description': item.description,
                    'status': item.status,
                    'reason': item.reason,
                    'solution': item.solution,
                    'advice': item.advice,
                    'notes': item.notes,
                    'jira': item.jira
                }
                res_data.append(dict_data)
                
        return res_data,200
            
            
class AddSupport(Resource):
    #serializer请求数据
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('createTime', type=str, help='No createTime', location='json')
        self.reqparse.add_argument('oemVendor', type=str, help='No oemVendor', location='json')
        self.reqparse.add_argument('deviceModel', type=str, help='No deviceModel', location='json')
        self.reqparse.add_argument('spId', type=str, help='No spId', location='json')
        self.reqparse.add_argument('environment', type=str, help='No environment', location='json')
        self.reqparse.add_argument('issueTrace', type=str, help='No issueTrace', location='json')
        self.reqparse.add_argument('message', type=str, help='No message', location='json')
        self.reqparse.add_argument('moduleName', type=str, help='No moduleName', location='json')
        self.reqparse.add_argument('handlePerson', type=str, help='No handlePerson', location='json')
        self.reqparse.add_argument('description', type=str, help='No description', location='json')
        self.reqparse.add_argument('status', type=str, help='No status', location='json')
        self.reqparse.add_argument('reason', type=str, help='No reason', location='json')
        self.reqparse.add_argument('solution', type=str, help='No solution', location='json')
        self.reqparse.add_argument('advice', type=str, help='No advice', location='json')
        self.reqparse.add_argument('notes', type=str, help='No notes', location='json')
        self.reqparse.add_argument('jira', type=str, help='No jira', location='json')
        super(AddSupport, self).__init__
        
    def post(self):
        #取request句柄
        value = ''
        args = self.reqparse.parse_args()
        #将moduleName格式初始化
        for module in args['moduleName']:
            module += module + ','
        if module.rfind(','):
            module = module[:-1]
        
        #存入db
        SupportInfo = SupportInfo()
        SupportInfo.create_time = args['createTime']
        SupportInfo.oem_vendor = args['oemVendor']
        SupportInfo.device_model = args['deviceModel']
        SupportInfo.sp_id = args['spId']
        SupportInfo.environment = args['environment']
        SupportInfo.issue_trace = args['issueTrace']
        SupportInfo.message = args['message']
        SupportInfo.module_name = args['moduleName']
        SupportInfo.handle_person = args['handlePerson']
        SupportInfo.description = args['description']
        SupportInfo.status = args['status']
        SupportInfo.reason = args['reason']
        SupportInfo.solution = args['solution']
        SupportInfo.advice = args['advice']
        SupportInfo.notes = args['notes']
        SupportInfo.jira = args['jira']
        try:
            db.session.add(SupportInfo)
            db.session.commit()
        except InvalidRequestError as e:
            message = {
                'ERROR': e.message
            }
            return message, 401
        
    
        return 201
    
    
class EditSupport(Resource):
    #serializer请求数据
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('issueNo', type=int, help='No issueNo', location='json')
        self.reqparse.add_argument('createTime', type=str, help='No createTime', location='json')
        self.reqparse.add_argument('oemVendor', type=str, help='No oemVendor', location='json')
        self.reqparse.add_argument('deviceModel', type=str, help='No deviceModel', location='json')
        self.reqparse.add_argument('spId', type=str, help='No spId', location='json')
        self.reqparse.add_argument('environment', type=str, help='No environment', location='json')
        self.reqparse.add_argument('issueTrace', type=str, help='No issueTrace', location='json')
        self.reqparse.add_argument('message', type=str, help='No message', location='json')
        self.reqparse.add_argument('moduleName', type=str, help='No moduleName', location='json')
        self.reqparse.add_argument('handlePerson', type=str, help='No handlePerson', location='json')
        self.reqparse.add_argument('description', type=str, help='No description', location='json')
        self.reqparse.add_argument('status', type=str, help='No status', location='json')
        self.reqparse.add_argument('reason', type=str, help='No reason', location='json')
        self.reqparse.add_argument('solution', type=str, help='No solution', location='json')
        self.reqparse.add_argument('advice', type=str, help='No advice', location='json')
        self.reqparse.add_argument('notes', type=str, help='No notes', location='json')
        self.reqparse.add_argument('jira', type=str, help='No jira', location='json')
        super(EditSupport, self).__init__
        
    def post(self):
        #取request句柄
        value = ''
        args = self.reqparse.parse_args()
        #将moduleName格式初始化
        for module in args['moduleName']:
            module += module + ','
        if module.rfind(','):
            module = module[:-1]
        
        #存入db
        handle = db.session.query(SupportInfo)
        SupportInfo = handle.filte(SupportInfo.issue_no.in_(args['issueNo']))
        SupportInfo.create_time = args['createTime']
        SupportInfo.oem_vendor = args['oemVendor']
        SupportInfo.device_model = args['deviceModel']
        SupportInfo.sp_id = args['spId']
        SupportInfo.environment = args['environment']
        SupportInfo.issue_trace = args['issueTrace']
        SupportInfo.message = args['message']
        SupportInfo.module_name = args['moduleName']
        SupportInfo.handle_person = args['handlePerson']
        SupportInfo.description = args['description']
        SupportInfo.status = args['status']
        SupportInfo.reason = args['reason']
        SupportInfo.solution = args['solution']
        SupportInfo.advice = args['advice']
        SupportInfo.notes = args['notes']
        SupportInfo.jira = args['jira']
        try:
            db.session.add(SupportInfo)
            db.session.commit()
        except InvalidRequestError as e:
            message = {
                'ERROR': e.message
            }
            return message, 401
        return  args, 201
    
    
class DeleteSupport(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('issueNo', type=str, help='No issueNo', location='json')
        super(DeleteSupport, self).__init__
        
    def post(self):
        args = self.reqparse.parse_args()
        if args['issueNo'] == '':
            return {"ERROR": "No issueNo"}, 404
        handle = db.session.query(SupportInfo)
        handle.filter(SupportInfo.issue_no == args['issueNo']).delete()
        db.session.add(handle)
        db.session.commit()
        message = 'DELETE' + args['issueNo'] + 'SUCCESS'
        return {"message": message},200
        
"""