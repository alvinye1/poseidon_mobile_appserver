# -*-coding: utf-8 -*-
'''
Created by jojo at 2018/9/7
'''
import flask
from flask import jsonify
import time
from flask import request
import json
from backend.modules.db_util_118_alarm import MSSoup118alarm
from backend.modules.db_util import MSSoup
from backend.modules.db_util_118 import MSSoup118
news_bp = flask.Blueprint(
    'news',
    __name__,
    url_prefix='/api'
)



@news_bp.route('/currentUser', methods=['GET'])
def get_currentUser():
    ms = MSSoup()
    res = ms.get_name()
    print('dddd')
    response = {
    'name': 'Serati Ma',
    'avatar': 'https://gw.alipayobjects.com/zos/rmsportal/BiazfanxmamNRoxxVxka.png',
    'userid': '00000001',
    'email': 'antdesign@alipay.com',
    'signature': '海纳百川，有容乃大',
    'title': '交互专家',
    'group': '蚂蚁金服－某某某事业群－某某平台部－某某技术部－UED',
    'tags': [
    {
      'key': '0',
      'label': '很有想法的',
    },
    {
      'key': '1',
      'label': '专注设计',
    },
    {
      'key': '2',
      'label': '辣~',
    },
    {
      'key': '3',
      'label': '大长腿',
    },
    {
      'key': '4',
      'label': '川妹子',
    },
    {
      'key': '5',
      'label': '海纳百川',
    },
    ],
    'notifyCount': 12,
    'country': 'China',
    'geographic': {
    'province': {
      'label': '浙江省',
      'key': '330000',
    },
    'city': {
      'label': '杭州市',
      'key': '330100',
    },
    },
    'address': '西湖区工专路 77 号',
    'phone': '0752-268888888',
    }
    return jsonify(response)
@news_bp.route('/test20181011', methods=['GET'])
def get_appname():
    app = MSSoup118()
    appname = app.get_appname()
    response = []
    print appname
    for i in appname:
        NAME = {}
        NAME['ENAME'] = i[0]
        response.append(NAME)
    return jsonify(response
    )   

@news_bp.route('/detail', methods=['GET'])
def get_machinedetail():
    detail = MSSoup118()
    machinedetail = detail.get_machine_detail()
    print machinedetail
    #response =[]
    for i in machinedetail:
	Detail = {}
	Detail['IP_ADDR'] = i[2]
	Detail['HOSTNAME'] = i[3]
	Detail['DEV_SN'] = i[4]
	Detail['CPU_AMT'] = i[5]
	Detail['CPU_CORE_AMT'] = i[6]
	Detail['MEM_CONTENT'] = i[7]
	Detail['DEV_POSITION'] = i[9]
	Detail['PART_TYPE'] = i[10]
	Detail['SOFT_VERSION'] = i[11]
	Detail['CI_DEPT'] = i[12]
	Detail['APPNAME'] = i[14]
	Detail['ENNAME_SIMPLE'] = i[15]
	Detail['APPNODE_DESC'] = i[16]
	Detail['DEPLOYMENT'] = i[18]
	Detail['MODEL'] = i[8]
	#response.append(Detail)
    return jsonify(Detail
    )



@news_bp.route('/detail2', methods=['GET'])
def get_machinedetail2():
    detail = MSSoup118()
    machinedetail = detail.get_machine_detail2()
    #print machinedetail
    response =[]
    id = 1
    for i in machinedetail:
	    Detail = {}
	    Detail['IP_ADDR'] = i[2]
	    # Detail['HOSTNAME'] = i[3]
	    # Detail['DEV_SN'] = i[4]
	    # Detail['CPU_AMT'] = i[5]
	    # Detail['CPU_CORE_AMT'] = i[6]
	    # Detail['MEM_CONTENT'] = i[7]
	    # Detail['DEV_POSITION'] = i[9]
	    # Detail['PART_TYPE'] = i[10]
	    # Detail['SOFT_VERSION'] = i[11]
	    # Detail['CI_DEPT'] = i[12]
	    # Detail['APPNAME'] = i[14]
	    # Detail['ENNAME_SIMPLE'] = i[15]
	    # Detail['APPNODE_DESC'] = i[16]
	    # Detail['DEPLOYMENT'] = i[18]
	    # Detail['MODEL'] = i[8]
	    # Detail['ID'] = id
	    # id += 1
	    response.append(Detail)
    return jsonify(response
    )

@news_bp.route('/detail3', methods=['GET','POST'])
def test2222():
    print "test"
    ip = request.args
    ip2 = ip.to_dict()
    ip3 = ip2['ip']
    detail = MSSoup118()
    machinedetail = detail.get_machine_detail3(ip3)
    # print machinedetail
    response = []
    machinedetail2 = machinedetail[0]
    Detail = {}
    Detail['IP_ADDR'] = machinedetail2[2]
    Detail['HOSTNAME'] = machinedetail2[3]
    Detail['DEV_SN'] = machinedetail2[4]
    Detail['CPU_AMT'] = machinedetail2[5]
    Detail['CPU_CORE_AMT'] = machinedetail2[6]
    Detail['MEM_CONTENT'] = machinedetail2[7]
    Detail['DEV_POSITION'] = machinedetail2[9]
    Detail['PART_TYPE'] = machinedetail2[10]
    Detail['SOFT_VERSION'] = machinedetail2[11]
    Detail['CI_DEPT'] = machinedetail2[12]
    Detail['APPNAME'] = machinedetail2[14]
    Detail['ENNAME_SIMPLE'] = machinedetail2[15]
    Detail['APPNODE_DESC'] = machinedetail2[16]
    Detail['DEPLOYMENT'] = machinedetail2[18]
    Detail['MODEL'] = machinedetail2[8]
    # print Detail
    response.append(Detail)
    return jsonify(response
    )

@news_bp.route('/ename3', methods=['GET','POST'])
def test3333():
    print "test======================================================="
    ip = request.args(type=unicode)
    print(ip)
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    ip2 = ip.to_dict()
    ip3 = ip2['ename']
    print (ip3)
    # detail = MSSoup118()
    # machinedetail = detail.get_machine_detail3(ip3)
    # print ip
    # # print machinedetail
    # response = []
    # machinedetail2 = machinedetail[0]
    # Detail = {}
    # Detail['IP_ADDR'] = machinedetail2[2]
    # Detail['HOSTNAME'] = machinedetail2[3]
    # Detail['DEV_SN'] = machinedetail2[4]
    # Detail['CPU_AMT'] = machinedetail2[5]
    # Detail['CPU_CORE_AMT'] = machinedetail2[6]
    # Detail['MEM_CONTENT'] = machinedetail2[7]
    # Detail['DEV_POSITION'] = machinedetail2[9]
    # Detail['PART_TYPE'] = machinedetail2[10]
    # Detail['SOFT_VERSION'] = machinedetail2[11]
    # Detail['CI_DEPT'] = machinedetail2[12]
    # Detail['APPNAME'] = machinedetail2[14]
    # Detail['ENNAME_SIMPLE'] = machinedetail2[15]
    # Detail['APPNODE_DESC'] = machinedetail2[16]
    # Detail['DEPLOYMENT'] = machinedetail2[18]
    # Detail['MODEL'] = machinedetail2[8]
    # # print Detail
    # response.append(Detail)

@news_bp.route('/rule', methods=['POST'])
def postRule():
    data = json.dumps(request.get_json())
    data_dict = json.loads(data.encode("utf-8"))
    print (data_dict)
    data1 = data_dict['SyslogID']
    ms = MSSoup118alarm()
    for i in data1:
        print (i)
        ms.get_del(i)
    # response = {"test":"aaaa"}
    # return jsonify(response)
    res = ms.get_alarmname()
    response = {"list": []}
    print "res"
    print(res)
    key = 0
    for i in res:
        test = {}
        test['key'] = key
        test['NodeIP'] = i[0]
        test['NodeAlias'] = i[1]
        test['Component'] = i[2]
        test['SummaryCN'] = i[3]
        test['EventType'] = i[4]
        test['START_TIME'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(i[5])))
        test['Occurence'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(i[6])))
        test['FREQUENCY'] = i[7]
        test['EventNameCN'] = i[8]
        test['CustomerSeverity'] = i[9]
        test['SyslogID'] = i[10]
        print "test", test
        key += 1
        response['list'].append(test)
    print (response)
    return jsonify(response
                   )



    # data_dict = json.loads(data.encode("utf-8"))
    # if data_dict['method'] == 'merge':
    #     print data
#
#
# @news_bp.route('/rule', methods=['GET'])
# def get_github_trend():
#     ms = MSSoup118alarm()
#     num = ms.get_num()
#     response = {"list": []}
#     key = 0
#     for i in num:
#         test_father = {}
#         ress = ms.get_context(i[1])
#         key += 1
#         for item in ress:
#             key_child = key*1000
#             test = {}
#             test['NodeIP'] = item[0]
#             test['NodeAlias'] = item[1]
#             test['Component'] = item[2]
#             test['SummaryCN'] = item[3]
#             test['EventType'] = item[4]
#             test['START_TIME'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(item[5])))
#             test['Occurence'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(item[6])))
#             test['FREQUENCY'] = item[7]
#             test['EventNameCN'] = item[8]
#             test['SyslogID'] = item[9]
#             test['FatherEvent'] = item[10]
#             if item[9] == item[10]:
#                 test['key'] = key
#                 test_father = test
#                 if i[0] > 1:
#                     test_children = []
#             else:
#                 key_child += 1
#                 test['key'] = key_child
#                 test_children.append(test)
#                 test_father['children'] = test_children
#
#         response['list'].append(test_father)
#
#     return jsonify(response)





# @news_bp.route('/detail3',methods=['GET'])
# def test2222():
#     ip = request.args
#     ip2 = ip.to_dict()
#     ip3 = ip2['ip']
#     detail = MSSoup118()
#     machinedetail = detail.get_machine_detail3(ip3)
#     # print machinedetail
#     print "test"
#     print machinedetail
#     # print machinedetail
#     response = []
#     # id = 1
#     Detail = {}
#     Detail['IP_ADDR'] = machinedetail[2]
#     Detail['HOSTNAME'] = machinedetail[3]
#     Detail['DEV_SN'] = machinedetail[4]
#     Detail['CPU_AMT'] = machinedetail[5]
#     Detail['CPU_CORE_AMT'] = machinedetail[6]
#     Detail['MEM_CONTENT'] = machinedetail[7]
#     Detail['DEV_POSITION'] = machinedetail[9]
#     Detail['PART_TYPE'] = machinedetail[10]
#     Detail['SOFT_VERSION'] = machinedetail[11]
#     Detail['CI_DEPT'] = machinedetail[12]
#     Detail['APPNAME'] = machinedetail[14]
#     Detail['ENNAME_SIMPLE'] = machinedetail[15]
#     Detail['APPNODE_DESC'] = machinedetail[16]
#     Detail['DEPLOYMENT'] = machinedetail[18]
#     Detail['MODEL'] = machinedetail[8]
#     # Detail['ID'] = id
#
#     response.append(Detail)
#     return jsonify(response)

@news_bp.route('/detail3',methods=['GET'])
def get_machinedetail3():
    detail = MSSoup118()
    machinedetail = detail.get_machine_detail2()
    print machinedetail
    response = []
    for i in machinedetail:
        Detail = {}
        Detail['IP_ADDR'] = i[2]
        Detail['APPNAME'] = i[14]
        # if i[14] == Detail['APPNAME']:
        #     Detail['IP_ADDR'] = i[2]
        #     Detail['APPNAME'] = i[14]
        # print Detail
        response.append(Detail)
    print response
    # for z in response;
    #     Detail2 = {}
    #     Detail2[]
    return jsonify(response)

@news_bp.route('/fake_list', methods=['GET'])
def get_appname_info():
    ms = MSSoup118()
    name = ms.get_appname()
    print name
    response = []
    for i in name:
        test = {"test1":{}}
        test['title'] = i[0]
	test['cpu'] = "10"
        test['IP_ADDR'] = "1"
        test['HOSTNAME'] = "2"
        test['DEV_SN'] = "3"
        test['CPU_AMT'] = "4"
        test['CPU_CORE_AMT'] = "5"
        test['MEM_CONTENT'] = "6"
        test['DEV_POSITION'] = "7"
        test['PART_TYPE'] = "8"
        test['SOFT_VERSION'] = "9"
        test['CI_DEPT'] = "10"
        test['APPNAME'] = "1"
        test['ENNAME_SIMPLE'] = "12"
        test['APPNODE_DESC'] = "13"
        test['DEPLOYMENT'] = "14"
        test['MODEL'] = "15"
	response.append(test)
    return jsonify(response)

@news_bp.route('/ename', methods=['GET'])
def get_ename_info():
    ms = MSSoup118()
    ename = ms.get_appname()
    print ename
    response = {}
    for i in ename:
	response['0'] = i[0]
	response.append(response)
    return jsonify(response)

@news_bp.route('/ename2', methods=['GET'])
def get_enameip2_info():
    ms = MSSoup118()
    ename = ms.get_machine_enameandip()
    #print ename
    response = []
    response1 = {"title": [],"ip":[]}
    #print response1['title']
    #print ename
    for i in ename:
        if i[0] in response1['title']:
            b = [1]
            b.append(response1['ip'])
            response1['ip'].append(i[1])
        else:
            response1['title'] = i[0]
            response1['ip'] = i[1]
            print a
            a.append(response1['ip'])
            response1['ip'] = a
            print response1
            # print response1
        response.append(response1)
        #print response
    return jsonify(response)

@news_bp.route('/rule', methods=['GET'])
def get_github_trend():
    ms = MSSoup118alarm()
    res = ms.get_alarmname()
    response = {"list":[]}
    print "res"
    print(res)
    key = 0
    for i in res:
        test = {}
        test['key'] = key
        test['NodeIP'] = i[0]
        test['NodeAlias'] = i[1]
        test['Component'] = i[2]
        test['SummaryCN'] = i[3]
        test['EventType'] = i[4]
        test['START_TIME'] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(int(i[5])))
        test['Occurence'] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(int(i[6])))
        test['FREQUENCY'] = i[7]
        test['EventNameCN'] = i[8]
        test['CustomerSeverity'] = i[9]
        test['SyslogID'] = i[10]
        print "test",test
        key += 1
        response['list'].append(test)
    print (response)
    return jsonify(response
    )

@news_bp.route('/toutiao/posts', methods=['GET'])
def get_toutiao_posts():
    toutiao = Toutiao()
    post_list = toutiao.get_posts()

    return jsonify(
        message='OK',
        data=post_list
    )





# def after_request(response):
#     response.headers['Access-Control-Allow-Origin'] = '*'
#     response.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
#     response.headers['Access-Control-Allow-Headers'] ='Content-Type.Authorization'
#     return response
# def create_app():
#     app = Flask(__name__)
#     app.after_request(after_request())
