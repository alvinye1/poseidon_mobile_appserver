# -*-coding: utf-8 -*-
'''
Created by jojo at 2018/7/5
'''
import pymysql as MySQLdb
from modules.common_util import get_config

config = get_config()

class MSDB(object):
    """
    封装MySQL的增删改查，具更细致的查询封装在MSSoup中
    """
    def __init__(self):
        self.conn = self.get_connect()

    def __del__(self):
        self.conn.close()

    def get_connect(self):
        """
        从配置中读取数据库配置，建立连接
        """
        user = config.get("mysqlalarm", "user")
        passwd = config.get("mysqlalarm", "passwd")
        host = config.get("mysqlalarm", "host")
        port = config.getint("mysqlalarm", "port")
        db = config.get("mysqlalarm", "db")
        print (user,passwd,host,port)
        return MySQLdb.connect(user=user,
                passwd=passwd,
                host=host,
                port=port,
                db=db,
                charset="utf8")

    def _update(self, sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        self.conn.commit()
        cursor.close()

    def _select(self, sql, use_dict=False):
        cursor = self.conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) \
                if use_dict else self.conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result


class MSSoup118alarm(object):
    """
    封装与mysql的交互
    """

    def __init__(self):
        """使用共享的数据库链接"""
        self.db_conn = MSDB().get_connect()

    def __del__(self):
        """当实例销毁时关闭数据库链接"""
        self.db_conn.close()

    def _update_db(self, sql):
        """更新数据库字段状态"""
        cursor = self.db_conn.cursor()
        cursor.execute(sql)
        self.db_conn.commit()
        # cursor.close()

    def read_db_data_to_dict(self, sql, dict_enabled=True):
        """封装sql命令执行"""
        result = {}
        try:
            cursor = self.db_conn.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
        except MySQLdb.Error as e:
            print("DIFF_DATA DB Error:" + e)
        finally:
            cursor.close()
            return result

    def get_appname(self):
        sql = "select distinct APPNAME from poseidon_app_info limit 200;"
        res = self.read_db_data_to_dict(sql)
        return res


    def get_machine_detail(self):
	    sql = "select * from poseidon_server_info a,poseidon_app_info b where a.APPNODECI = b.APPNODECI and IP_ADDR limit 200;"
	    detail = self.read_db_data_to_dict(sql)
            return detail

    def get_machine_detail2(self):
        sql = "select * from poseidon_server_info a,poseidon_app_info b where a.APPNODECI = b.APPNODECI and IP_ADDR limit 10;"
        detail2 = self.read_db_data_to_dict(sql)
        return detail2

    def get_machine_detail3(self,ip):
        sql = "select * from poseidon_server_info a,poseidon_app_info b where a.APPNODECI = b.APPNODECI and IP_ADDR = '%s'"%(ip)
        detail3 = self.read_db_data_to_dict(sql)
        return detail3

    def get_machine_enameandip(self):
        sql = "SELECT DISTINCT b.APPNAME, a.IP_ADDR FROM poseidon_server_info a,poseidon_app_info b WHERE a.APPNODECI = b.APPNODECI ORDER BY b.APPNAME limit 500;"
        enameandip = self.read_db_data_to_dict(sql)
        return enameandip

    def get_alarmname(self):
        sql = "select NodeIP,NodeAlias,Component,SummaryCN,EventType,START_TIME,Occurence,FREQUENCY,EventNameCN,CustomerSeverity,SyslogID from poseidon_alarm_sys limit 40;"
        res = self.read_db_data_to_dict(sql)
        return res

    def get_del(self,syslogid):
        sql = "delete from poseidon_alarm_sys where SyslogID= '%s'"%(syslogid)
        # sql = "DELETE FROM poseidon_alarm_sys WHERE SyslogID = 14001;"
        # self.read_db_data_to_dict(sql)
        self._update_db(sql)
        print ("==================del====================")
        # return self.read_db_data_to_dict(sql)



    def get_num(self):
        sql = "select count(1) as num,FatherEvent " \
              "from(select NodeIP,NodeAlias,Component,SummaryCN,EventType," \
              "START_TIME,Occurence,FREQUENCY,EventNameCN,SyslogID," \
              "FatherEvent " \
              "from poseidon_alarm_sys " \
              "limit 200) a " \
              "group by FatherEvent" \
              ";"
        res = self.read_db_data_to_dict(sql)
        return res


    def get_context(self, fatherEvent):
        sql = "select NodeIP,NodeAlias,Component,SummaryCN,EventType," \
              "START_TIME,Occurence,FREQUENCY,EventNameCN,SyslogID," \
              "FatherEvent " \
              "from poseidon_alarm_sys " \
              "where FatherEvent='%d'" % fatherEvent
        res = self.read_db_data_to_dict(sql)
        return res


if __name__ == '__main__':
   app = MSSoup118alarm()
    #res = ms.get_name()
   # detail = ms.get_detail()
   # print(detail)
   # print(res)
   # print("111")
