# -*-coding: utf-8 -*-
'''
Created by jojo at 2018/9/7
'''
import flask
import random
from flask import jsonify
from random import choice
from flask import request
from modules.datamachine import *
import simplejson
from modules.database_controller.db_util import MSSoup
from modules.database_controller.db_util_118 import MSSoup118
from modules.readfile import NMONfile
from modules.alarm_processor.Close_alarm import Close_alarm
from modules.minion_controller.signal import Signal
from modules.database_controller.Mongodb import *
from modules.piedata import *

news_bp = flask.Blueprint(
    'news',
    __name__,
    url_prefix='/api',
)


@news_bp.route('/test20181011', methods=['GET'])
def get_appname():
    app = MSSoup118()
    appname = app.get_appname()
    response = []
    appliststatus = "/appliststatus/"
    status = ['norm.svg']
    for i in appname:
        NAME = {}
        NAME['ENAME'] = i[0]
        NAME['APP_MAINT'] = i[1]
        NAME['DEPLOYMENT'] = i[2]
        NAME['ENNAME_SIMPLE'] = i[3]
        NAME['CPU'] = random.randint(1, 60)
        NAME['MEM'] = random.randint(1, 60)
        NAME['IO'] = random.randint(1, 60)
        NAME['CONNECT'] = random.randint(1, 60)
        NAME['STATUS'] = appliststatus + choice(status)
        NAME['status'] = "list"
        response.append(NAME)
    return jsonify(response
                   )


@news_bp.route('/detail2', methods=['GET'])
def get_machinedetail2():
    detail = MSSoup118()
    machinedetail = detail.get_machine_detail2()
    response = []
    id = 1
    for i in machinedetail:
        Detail = {}
        Detail['IP_ADDR'] = i[2]
        response.append(Detail)
    return jsonify(response
                   )


@news_bp.route('/detail3', methods=['GET', 'POST'])
def test2222():
    ip = request.args
    ip2 = ip.to_dict()
    ip3 = ip2['ip']
    detail = MSSoup118()
    machinedetail = detail.get_machine_detail3(ip3)
    response = []
    machinedetail2 = machinedetail[0]
    response = [{"IP_ADDR": "IP", "DEV_POSITION": machinedetail2[2]},
                {"IP_ADDR": "主机名", "DEV_POSITION": machinedetail2[3]},
                {"IP_ADDR": "内存", "DEV_POSITION": machinedetail2[7]},
                {"IP_ADDR": "CPU", "DEV_POSITION": machinedetail2[5]},
                {"IP_ADDR": "应用简称", "DEV_POSITION": machinedetail2[15]},
                {"IP_ADDR": "操作系统", "DEV_POSITION": machinedetail2[11]},
                {"IP_ADDR": "部署地", "DEV_POSITION": machinedetail2[18]},
                {"IP_ADDR": "CI负责部门", "DEV_POSITION": machinedetail2[12]}]
    return jsonify(response
                   )


@news_bp.route('/rule', methods=['GET'])
def get_github_trend():
    ms = MSSoup118alarm()
    res = ms.get_alarmname()
    dcap = ms.get_alarm_dcap()
    sum = res + dcap
    # print("=====================21321321321321312321321321213========================")
    # print(sum)
    if not sum:
        json = {"list": []}
        return jsonify(json)
    else:
        data = Alarmdata(("NodeIP", "NodeAlias", "Component", "SummaryCN", "EventType", "START_TIME", "Occurence",
                          "FREQUENCY", "EventNameCN", "CustomerSeverity", "SyslogID", "FatherEvent", "FLAGBIT",
                          "START_SORT", "END_SORT"),
                         "FatherEvent",
                         "SyslogID", sum)
        json = data.make_json()
        return jsonify(json)


@news_bp.route('/rule', methods=['POST'])
def postRule():
    data = simplejson.dumps(request.get_json())
    data_dict = simplejson.loads(data.encode("utf-8"))
    id = data_dict['SyslogID']
    print(id)
    flagbit = data_dict['AlarmType']
    cl = Close_alarm()
    for i in range(len(id)):
        cl.alarm_close(id[i], flagbit[i])
    ms = MSSoup118alarm()
    res = ms.get_alarmname()
    dcap = ms.get_alarm_dcap()
    sum = res + dcap
    # print("=====================21321321321321312321321321213========================")
    # print(sum)
    if not sum:
        jsons = {"list": []}
        return jsonify(jsons)
    else:
        data = Alarmdata(("NodeIP", "NodeAlias", "Component", "SummaryCN", "EventType", "START_TIME", "Occurence",
                          "FREQUENCY", "EventNameCN", "CustomerSeverity", "SyslogID", "FatherEvent", "FLAGBIT",
                          "START_SORT"),
                         "FatherEvent",
                         "SyslogID", sum)
        jsons = data.make_json()
        return jsonify(jsons)


@news_bp.route('/detail3', methods=['GET'])
def get_machinedetail3():
    detail = MSSoup118()
    machinedetail = detail.get_machine_detail2()
    print(machinedetail)
    response = []
    for i in machinedetail:
        Detail = {}
        Detail['IP_ADDR'] = i[2]
        Detail['APPNAME'] = i[14]
        response.append(Detail)
    print(response)

    return jsonify(response)


@news_bp.route('/ename', methods=['GET'])
def get_ename_info():
    ms = MSSoup118()
    ename = ms.get_appname()
    response = {}
    for i in ename:
        response['0'] = i[0]
        response.append(response)
    return jsonify(response)


@news_bp.route('/ename2', methods=['GET'])
def get_enameip2_info():
    ms = MSSoup118()
    ename = ms.get_machine_enameandip()
    # print ename
    response = []
    response1 = {"title": [], "ip": []}
    # print response1['title']
    # print ename
    for i in ename:
        if i[0] in response1['title']:
            b = [1]
            b.append(response1['ip'])
            response1['ip'].append(i[1])
        else:
            response1['title'] = i[0]
            response1['ip'] = i[1]
            a.append(response1['ip'])
            response1['ip'] = a
            # print response1
        response.append(response1)
        # print response
    return jsonify(response)


@news_bp.route('/merge', methods=['POST'])
def get_merge_posts():
    data = simplejson.dumps(request.get_json())
    data_dict = simplejson.loads(data.encode("utf-8"))
    ms = MSSoup118alarm()
    chlidrenid = data_dict["SyslogID"]
    childrentype = data_dict["AlarmType"]
    newfather = data_dict["newFahersyslogid"]
    for i in range(len(chlidrenid)):
        print(type(childrentype[i]), childrentype[i])
        if childrentype[i] == 1:
            ms.merge_alarm_dcap(newfather, chlidrenid[i])
        else:
            ms.merge_alarm_sys(newfather, chlidrenid[i])
    return jsonify(
        message='OK'
    )



@news_bp.route('/appenamesimple', methods=['POST'])  # get all ips from cardlist
def get_app_ips():
    # app =request.args.to_dict()
    # print("apppppppppppppppppppp",app)
    # app_dict = app
    app = simplejson.dumps(request.get_json())
    app_dict = simplejson.loads(app.encode("utf-8"))
    response = []
    lista = {}
    webnum = 0
    dbsnum = 0
    appnum = 0

    if len(app_dict) == 2:
        app_name = app_dict['ename']
        ms = MSSoup118()
        ips = ms.get_app_ip(app_name)
        for i in ips:
            # response.append(i)
            Cluster = {}
            Cluster['IP'] = i[0]
            Cluster['HOSTNAME'] = i[1]
            if "web" in i[1]:
                Cluster['Pic'] = "/clustersvg/web.svg"
                webnum += 1
            elif "dbs" in i[1]:
                Cluster['Pic'] = "/clustersvg/database.svg"
                dbsnum += 1
            elif "app" in i[1]:
                Cluster['Pic'] = "/clustersvg/APP.svg"
                appnum += 1
            else:
                Cluster['Pic'] = "/clustersvg/unknown.svg"
            response.append(Cluster)
        # print("===========================",response)
        # print(lista)
        testdata = [
            {
                "IP_ADDR": "APP",
                "total": appnum,
                "erro": "0",
                "normal": appnum,
            },
            {
                "IP_ADDR": "数据库",
                "total": dbsnum,
                "erro": "0",
                "normal": dbsnum,
            },
            {
                "IP_ADDR": "WEB",
                "total": webnum,
                "erro": "0",
                "normal": webnum,
            },
            {
                "IP_ADDR": "IASS",
                "total": "0",
                "erro": "0",
                "normal": "0",
            },
            {
                "IP_ADDR": "PASS",
                "total": "0",
                "erro": "0",
                "normal": "0",
            },
            {
                "IP_ADDR": "VMWARE",
                "total": "10",
                "erro": "0",
                "normal": "10",
            },

        ];
        lista['Cluster'] = response
        lista['Testdata'] = testdata
        return jsonify(lista)

    else:
        return jsonify(response)


@news_bp.route('/get_History_Alarm', methods=['POST'])
def get_History_Alarm_Cluster():
    fname = simplejson.dumps(request.get_json())
    app_dict = simplejson.loads(fname.encode("utf-8"))
    print("ssssssssssssssssssssss", app_dict['Fname'])
    ms = MSSoup118alarm()
    dcapalarm = ms.history_alarm_dcap_cluster(app_dict['Fname'])
    sysalarm = ms.history_alarm_sys_cluster(app_dict['Fname'])
    sum = dcapalarm + sysalarm
    if not sum:
        jsons = {"list": []}
        return jsonify(jsons)
    else:
        data = Alarmdata(("NodeIP", "NodeAlias", "Component", "SummaryCN", "EventType", "START_TIME", "Occurence",
                          "FREQUENCY", "EventNameCN", "CustomerSeverity", "SyslogID", "FatherEvent", "FLAGBIT"),
                         "FatherEvent",
                         "SyslogID", sum)
        jsons = data.make_json()
        return jsonify(jsons)


@news_bp.route('/get_History_Alarm_Detail', methods=['POST'])
def get_History_Alarm_Detail():
    fname = simplejson.dumps(request.get_json())
    app_dict = simplejson.loads(fname.encode("utf-8"))
    ms = MSSoup118alarm()
    dcapalarm = ms.history_alarm_dcap_detail(app_dict['Fname'])
    sysalarm = ms.history_alarm_sys_detail(app_dict['Fname'])
    sum = dcapalarm + sysalarm
    if not sum:
        jsons = {"list": []}
        return jsonify(jsons)
    else:
        data = Alarmdata(("NodeIP", "NodeAlias", "Component", "SummaryCN", "EventType", "START_TIME", "Occurence",
                          "FREQUENCY", "EventNameCN", "CustomerSeverity", "SyslogID", "FatherEvent", "FLAGBIT"),
                         "FatherEvent",
                         "SyslogID", sum)
        jsons = data.make_json()
        return jsonify(jsons)


@news_bp.route('/get_nmon_data', methods=['POST'])
def get_nmon_data():
    nmon = simplejson.dumps(request.get_json())
    nmon_dict = simplejson.loads(nmon.encode("utf-8"))
    nmon_param = nmon_dict['payload']
    nmon_ip = nmon_param[0]
    nmon_host = nmon_param[1]

    #nmon_host = "poseidon_YHZ"

    #nmon_ip = "80.2.238.218"
    # nmon_ip = "80.2.238.225"
    try:
        nmon = NMONfile(nmon_host)
        [files, cols, fields, files_content,type] = nmon.get_messages(nmon_ip, 8885,'')
        print(files)
        return jsonify([files, cols, fields, files_content,type])
    except:
        mess = [{"mess":"ok"}]
        print(mess)
        return jsonify(mess)


@news_bp.route('/get_Search_Info', methods=['POST'])
def get_search_data():
    fname2 = simplejson.dumps(request.get_json())
    app_dict2 = simplejson.loads(fname2.encode("utf-8"))
    ms = MSSoup118alarm()
    # print("app_dict['Searchid']app_dict['Searchid']", app_dict2['Searchid'])
    dcapalarm = ms.search_alarm_dcap(app_dict2['Searchid'])
    sysalarm = ms.search_alarm_sys(app_dict2['Searchid'])
    # print("dcapalarm",dcapalarm)
    # print("sysalarm",sysalarm)
    sum = dcapalarm + sysalarm
    # print("sumsumsumsumsumsumsum",sum)
    if not sum:
        jsons = {"list": []}
        return jsonify(jsons)
    else:
        data = Alarmdata(("NodeIP", "NodeAlias", "Component", "SummaryCN", "EventType", "START_TIME", "Occurence",
                          "FREQUENCY", "EventNameCN", "CustomerSeverity", "SyslogID", "FatherEvent", "FLAGBIT"),
                         "FatherEvent",
                         "SyslogID", sum)
        jsons = data.make_json()
        return jsonify(jsons)


# get_one_data
@news_bp.route('/get_one_data', methods=['POST'])
def get_one_data():
    command_origin = simplejson.dumps(request.get_json())
    command_dict = simplejson.loads(command_origin.encode("utf-8"))
    command_param = command_dict['payload']
    command_host = command_param[0]
    command_port = command_param[1]
    command = command_param[2]
    command_last = (command.splitlines())[-1]
    try:
        s = Signal(command_host,8885)
        result = s.run('instant_script', command_last)
        if result == []:
            result = "SUCCESS"
        return jsonify(result)
    except:
        err = "no minion"
        return jsonify(err)



# get_cardlistmasteripsearch
@news_bp.route('/cardlistmasteripsearch', methods=['POST'])
def cardlistmasteripsearch():
    ip = simplejson.dumps(request.get_json())
    ip2 = simplejson.loads(ip.encode("utf-8"))
    ip3 = ip2['ipinfosearch']
    detail = MSSoup118()
    machinedetail = detail.get_machine_detail3_cardlistsearch(ip3)
    respons = []
    appliststatus = "/appliststatus/"
    status = ['norm.svg']
    if machinedetail != {}:
        for i in machinedetail:
            NAME = {}
            NAME['ENAME'] = i[0]
            NAME['APP_MAINT'] = i[1]
            NAME['status'] = "detail"
            NAME['CPU'] = random.randint(1, 60)
            NAME['MEM'] = random.randint(1, 60)
            NAME['IO'] = random.randint(1, 60)
            NAME['CONNECT'] = random.randint(1, 60)
            NAME['STATUS'] = appliststatus + choice(status)
            respons.append(NAME)
        return jsonify(respons
                       )
    else:
        messs = [{"mess": "ok", "status": "detail"}]
        return jsonify(messs)



# get_cardlistipsearch
@news_bp.route('/cardlistipsearch', methods=['POST'])
def cardlistipsearch():
    app = simplejson.dumps(request.get_json())
    app_dict = simplejson.loads(app.encode("utf-8"))
    response = []
    lista = {}
    webnum = 0
    dbsnum = 0
    appnum = 0
    if len(app_dict) == 2:
        ms = MSSoup118()
        ips = ms.get_app_ip_hostname(app_dict['ipinfo'])
        for i in ips:
            # response.append(i)
            Cluster = {}
            Cluster['IP'] = app_dict['ipinfo']
            Cluster['HOSTNAME'] = i[0]
            if "web" in i[0]:
                Cluster['Pic'] = "/clustersvg/web.svg"
                webnum += 1
            elif "dbs" in i[0]:
                Cluster['Pic'] = "/clustersvg/database.svg"
                dbsnum += 1
            elif "app" in i[0]:
                Cluster['Pic'] = "/clustersvg/APP.svg"
                appnum += 1
            else:
                Cluster['Pic'] = "/clustersvg/unknown.svg"
            response.append(Cluster)
        # print("===========================",response)
        # print(lista)
        testdata = [
            {
                "IP_ADDR": "APP",
                "total": appnum,
                "erro": "0",
                "normal": appnum,
            },
            {
                "IP_ADDR": "数据库",
                "total": dbsnum,
                "erro": "0",
                "normal": dbsnum,
            },
            {
                "IP_ADDR": "WEB",
                "total": webnum,
                "erro": "0",
                "normal": webnum,
            },
            {
                "IP_ADDR": "IASS",
                "total": "0",
                "erro": "0",
                "normal": "0",
            },
            {
                "IP_ADDR": "PASS",
                "total": "0",
                "erro": "0",
                "normal": "0",
            },
            {
                "IP_ADDR": "VMWARE",
                "total": "10",
                "erro": "0",
                "normal": "10",
            },

        ];
        lista['Cluster'] = response
        lista['Testdata'] = testdata
        return jsonify(lista)

    else:
        return jsonify(response)

@news_bp.route('/adi_list', methods=['GET'])
def get_adi_list():
    db = MongoDB('80.7.238.136', 8889, 'testposeidon', 'adi', 'root', 'qwert789')
    data = db.search({"_id": 0}, 'some_field')
    return jsonify(data)

@news_bp.route('/adi_search', methods=['POST'])
def get_adi_search():
    ip = simplejson.dumps(request.get_json())
    ip2 = simplejson.loads(ip.encode("utf-8"))
    ip3 = ip2['ipinfosearch']
    # print(ip3)
    if ip3 == "":
        db = MongoDB('80.7.238.136', 8889, 'testposeidon', 'adi', 'root', 'qwert789')
        data = db.search({"_id": 0}, 'some_field')
        return jsonify(data)
    else:
        db = MongoDB('80.7.238.136', 8889, 'testposeidon', 'adi', 'root', 'qwert789')
        search = db.search(({"IP Address":ip3}), 'one_field')
    # print(search)
        return jsonify(search)

@news_bp.route('/one_list', methods=['GET'])
def get_onelist():
    db = MongoDB('80.7.238.136', 8889, 'test', 'one', 'root', 'qwert789')
    data = db.search({"_id": 0}, 'some_field')
    return jsonify(data)

@news_bp.route('/get_Search_Info_One', methods=['POST'])
def get_one_search():
    ip = simplejson.dumps(request.get_json())
    ip2 = simplejson.loads(ip.encode("utf-8"))
    ip3 = ip2['ipinfosearch']
    print(ip3)
    if ip3 == "":
        db = MongoDB('80.7.238.136', 8889, 'test', 'one', 'root', 'qwert789')
        data = db.search({"_id": 0}, 'some_field')
        return jsonify(data)
    else:
        db = MongoDB('80.7.238.136', 8889, 'test', 'one', 'root', 'qwert789')
        search = db.search(({"ip":ip3}), 'one_field')
    # print(search)
        return jsonify(search)

@news_bp.route('/homedata', methods=['GET'])
def get_home_data():
    data = {}
    try:
        d = homedata(86400)
        pie = d.piedata()
        total = d.alarm_total()
        data['pie'] = pie
        data['totalalarm'] = total
        return jsonify(data)
    except:
        data['pie'] = 0
        data['totalalarm'] = 0
        return jsonify(data)

@news_bp.route('/mobile_alarm', methods=['POST','GET'])
def get_mobile_alarm():
    data = [
        {
            'title': '80.7.83.119',
            'extra': '30',
            'key': '1',
            'alarm': 'Poseidon minion 20分钟未收到返回值',
            'starttime': '2019-02-19 02:50:02',
            'currenttime': '2019-02-19 12:00:01',
        },
        {
            'title': '80.7.83.118',
            'extra': '300',
            'key': '2',
            'alarm': 'Poseidon minion 30分钟未收到返回值',
            'starttime': '2019-02-19 22:50:02',
            'currenttime': '2019-02-19 23:00:01',
        },
    ]
    print("test_mobile")
    return jsonify(data)
