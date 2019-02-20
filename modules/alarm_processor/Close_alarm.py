# -*-coding: utf-8 -*-
from modules.database_controller.ctl_mysql import *
import calendar
import time
import datetime
import logging

class Close_alarm:


    def __init__(self):
        """使用共享的数据库链接"""
        self.db = Database()

    def __del__(self):
        """当实例销毁时关闭数据库链接"""
        self.db.__del__()

    def alarm_close(self,id,flagbit):

        now_stamp = time.time()
        utc_time = datetime.datetime.utcfromtimestamp(now_stamp)
        #time_datetime = datetime.datetime.now()
        time_utc = calendar.timegm(datetime.datetime.timetuple(utc_time))

        if flagbit == 2:
            logging.info("Ready to delete syslog alarm ..")

            sql1 = "UPDATE poseidon_alarm_sys SET END_TIME = '%s'" % time_utc + " WHERE SyslogID = '%s'" % id
            self.db.update(sql1)

            sql2 = "INSERT INTO poseidon_alarm_sys_hist(SyslogID,FatherEvent,Class,START_TIME,END_TIME,Occurence," \
                   "FREQUENCY,Customer,NodeAlias,NodeIP,BusinessName,AppName,AppShortName,ComponentType,Component," \
                   "SubComponent,InstanceId,InstanceValue,EventName,EventNameCN,Type,EventType,CustomerSeverity," \
                   "FirstOccurrence,LastOccurrence,SourceServerSerial,ACK_Time,Close_Time,OwnerGroup,Summary,SummaryCN," \
                   "Tally,Site,OrgID,DevOrgID,ProcessMode,EnrichStatus,MaintainStatus,SMSFlag,Acknowledged,EventStatus," \
                   "ENNAME,FLAGBIT)" \
                   "SELECT SyslogID,FatherEvent,Class,START_TIME,END_TIME,Occurence,FREQUENCY,Customer,NodeAlias,NodeIP," \
                   "BusinessName,AppName,AppShortName,ComponentType,Component,SubComponent,InstanceId,InstanceValue," \
                   "EventName,EventNameCN,Type,EventType,CustomerSeverity,FirstOccurrence,LastOccurrence," \
                   "SourceServerSerial,ACK_Time,Close_Time,OwnerGroup,Summary,SummaryCN,Tally,Site,OrgID,DevOrgID," \
                   "ProcessMode,EnrichStatus,MaintainStatus,SMSFlag,Acknowledged,EventStatus,ENNAME,FLAGBIT " \
                   "FROM poseidon_alarm_sys WHERE SyslogID = '%d'" % id
            self.db.insert(sql2)

            sql3 = "DELETE FROM poseidon_alarm_sys WHERE  SyslogID = '%s'" % id
            self.db.delete(sql3)

        elif flagbit == 1:
            logging.info("Ready to delete dcap alarm ..")
            # cursor = db.cursor()
            sql4 = "UPDATE poseidon_alarm_dcap SET END_TIME = '%s'" % time_utc + " WHERE DCAPID = '%s'" % id
            self.db.update(sql4)

            sql5 = "INSERT INTO poseidon_alarm_dcap_hist(DCAPID,FatherEvent,Class,START_TIME,END_TIME,FREQUENCY," \
                   "EventSource,NodeIP,IndicatorName,IndicatorName2,unknown,MoniStatus,Recovery,Occurence,Instance," \
                   "InstanceName,IndicatorValue,Strategy,NodeAlias,Component,EventNameCN,EventType,CustomerSeverity," \
                   "SummaryCN,ENNAME,FLAGBIT)" \
                   "SELECT DCAPID,FatherEvent,Class,START_TIME,END_TIME,FREQUENCY,EventSource,NodeIP,IndicatorName," \
                   "IndicatorName2,unknown,MoniStatus,Recovery,Occurence,Instance,InstanceName,IndicatorValue,Strategy," \
                   "NodeAlias,Component,EventNameCN,EventType,CustomerSeverity,SummaryCN,ENNAME,FLAGBIT " \
                   "FROM poseidon_alarm_dcap WHERE DCAPID = '%d'" % id
            self.db.insert(sql5)

            sql6 = "DELETE FROM poseidon_alarm_dcap WHERE  DCAPID = '%s'" % id
            self.db.delete(sql6)

        else:
            logging.error("There is an error when closing alarm")
