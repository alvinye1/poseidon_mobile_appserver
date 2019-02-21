# -*-coding: utf-8 -*-
'''
Created by jojo at 2018/7/5
'''
import pymysql as MySQLdb
# import MySQLdb
from modules.common_util import get_config

config = get_config()


class MSDB(object):
    def __init__(self, db_label):
        self.db_label = db_label
        self.conn = self.get_connect()

    def __del__(self):
        self.conn.close()

    def get_connect(self):
        user = config.get(self.db_label, "user")
        passwd = config.get(self.db_label, "passwd")
        host = config.get(self.db_label, "host")
        port = config.getint(self.db_label, "port")
        db = config.get(self.db_label, "db")
        print('============================= get_connect ==========================')
        print(user)
        print(passwd)
        print(host)
        print(port)
        print(db)
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
        cursor = self.conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result


class MSSoup(object):
    def __init__(self, db_name):
        #        print('===============================尝试连接==============================')
        self.db_conn = MSDB(db_name).get_connect()
        print('lianjie')

    def __del__(self):
        self.db_conn.close()

    def _update_db(self, sql):
        cursor = self.db_conn.cursor()
        cursor.execute(sql)
        self.db_conn.commit()
        cursor.close()

    def read_db_data_to_dict(self, sql, dict_enabled=True):
        result = {}
        try:
            cursor = self.db_conn.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
        except MySQLdb.Error as e:
            logger.error("error" + e)
        finally:
            cursor.close()
        return result

    def get_appname(self):
        sql = "select APPNAME from cmdb_app_info limit 20"
        result = self.read_db_data_to_dict(sql)
        return result

    def get_totalnum(self):
        sql = "select count(1) from monitor_message"
        result = self.read_db_data_to_dict(sql)
        return result

    def get_alarminfo(self, start, end):
        print(start, end)
        sql = "select * from monitor_message where msg_id BETWEEN " + str(start) \
              + " and " + str(end)
        result = self.read_db_data_to_dict(sql)
        return result


if __name__ == '__main__':
    db_map = {'mysql': 'cmdb_app_info', 'mysql_alart': 'monitor_message'}
    # db_name = 'mysql'
    db_label = 'mysql'
    ms = MSSoup(db_label)
    sql = "select * from " + db_map[db_label] + " limit 20"
    result_cmdb = ms.read_db_data_to_dict(sql)
    print(result_cmdb)
