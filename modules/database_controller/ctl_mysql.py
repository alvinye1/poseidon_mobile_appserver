#!/usr/bin/env python
# ======================================
# POSEIDON PROGRAM FILE
# APPLICATION:
# Author:Alvin Ye .ICBC
# Version(Internal):1.0
# All rights reserved
# Modified by KnightQin
# date: 2018-11-15
# ======================================

import pymysql
from modules.utility import *
from DBUtils.PooledDB import *
import logging


class Label:
    """A label means a alarm"""
    pass


class Database:
    """mysql database connection."""

    def __init__(self):
        # read from config file
        self.host = config.get('DATABASE', 'MYSQL_HOST')
        self.port = int(config.get('DATABASE', 'MYSQL_PORT'))
        self.user = config.get('DATABASE', 'MYSQL_USER')
        self.passwd = config.get('DATABASE', 'MYSQL_PASSWD')
        self.db = config.get('DATABASE', 'MYSQL_DB')
        # mysql database initialize
        '''
        self._db = pymysql.connect(host=self.host,
                                   port=self.port,
                                   user=self.user,
                                   passwd=self.passwd,
                                   db=self.db,
                                   charset="utf8",
                                   autocommit=True)
        '''
        # init self.pool
        self.pool = PooledDB(pymysql, db=self.db, host=self.host, user=self.user, passwd=self.passwd, port=self.port,
                             charset="utf8", use_unicode=True, autocommit=True)
        self.conn = self.pool.connection(shareable=True)

    def __del__(self):
        self.conn.close()

    def cursor(self):
        # return self._db.cursor()
        cursor = self.conn.cursor()
        return cursor

    def update(self, sql):
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(sql)
        except Exception:
            logging.error("Update Exception Occurred", Exception)
            logging.error("ERROR:", sql)
            self.conn.rollback()
        finally:
            self.cursor.close()

    def insert(self, sql):
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(sql)
        except Exception:
            logging.error("Insert Exception Occurred", Exception)
            logging.error("ERROR:", sql)
            self.conn.rollback()
        finally:
            self.cursor.close()

    def selectone(self, sql):
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(sql)
        except Exception:
            logging.error("Select Exception Occurred", Exception)
        finally:
            result = self.cursor.fetchone()
            self.cursor.close()
        return result

    def selectall(self, sql):
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(sql)
        except Exception:
            logging.error("Select Exception Occurred", Exception)
        finally:
            results = self.cursor.fetchall()
            self.cursor.close()
        return results

    def delete(self, sql):
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(sql)
        except Exception:
            logging.error("Delete Exception Occurred", Exception)
            self.conn.rollback()
        finally:
            self.cursor.close()


if __name__ == "__main__":
    db = Database()
    sql = "select * from poseidon_alarm_dcap "
    logging.info(db.selectall(sql))
