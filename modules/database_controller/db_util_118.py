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
        user = config.get("mysql118", "user")
        passwd = config.get("mysql118", "passwd")
        host = config.get("mysql118", "host")
        port = config.getint("mysql118", "port")
        db = config.get("mysql118", "db")
        # print(user, passwd, host, port)
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


class MSSoup118(object):
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
        cursor.close()

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
        sql = "select distinct APPNAME,APP_MAINT,DEPLOYMENT,ENNAME_SIMPLE from poseidon_app_info;"
        res = self.read_db_data_to_dict(sql)
        return res

    def get_machine_detail(self):
        sql = "select * from poseidon_server_info a,poseidon_app_info b where a.APPNODECI = b.APPNODECI and IP_ADDR limit 200;"
        detail = self.read_db_data_to_dict(sql)
        return detail

    def get_machine_detail2(self):
        sql = "select * from poseidon_server_info a,poseidon_app_info b where a.APPNODECI = b.APPNODECI and IP_ADDR limit 40;"
        detail2 = self.read_db_data_to_dict(sql)
        return detail2

    def get_machine_detail3(self, ip):
        sql = "select * from poseidon_server_info a,poseidon_app_info b where a.APPNODECI = b.APPNODECI and IP_ADDR = '%s'" % (
            ip)
        detail3 = self.read_db_data_to_dict(sql)
        return detail3

    def get_machine_detail3_cardlistsearch(self, ip):
        sql = "select IP_ADDR,HOSTNAME from poseidon_server_info a,poseidon_app_info b where a.APPNODECI = b.APPNODECI and CONCAT(`IP_ADDR`,`HOSTNAME`,`APPNAME`) like '%{0}%';" .format(
            ip)
        detail3 = self.read_db_data_to_dict(sql)
        return detail3

    def get_machine_enameandip(self):
        sql = "SELECT DISTINCT b.APPNAME, a.IP_ADDR FROM poseidon_server_info a,poseidon_app_info b WHERE a.APPNODECI = b.APPNODECI ORDER BY b.APPNAME limit 500;"
        enameandip = self.read_db_data_to_dict(sql)
        return enameandip

    def get_app_ip(self, appname):
        sql = "select IP_ADDR,HOSTNAME from poseidon_server_info where APPNODECI in (select APPNODECI from poseidon_app_info where APPNAME = '%s')" % (
            appname)
        appip = self.read_db_data_to_dict(sql)
        return appip

    def get_app_ip_hostname(self, appname):
        sql = "select HOSTNAME from poseidon_server_info where IP_ADDR =  '%s'" % (
            appname)
        appip = self.read_db_data_to_dict(sql)
        return appip



if __name__ == '__main__':
    app = MSSoup118()
    # res = ms.get_name()
    # detail = ms.get_detail()
    # print(detail)
    # print(res)
    # print("111")
