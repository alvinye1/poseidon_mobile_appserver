# -*-coding: utf-8 -*-
from modules.database_controller.db_util_118_alarm import MSSoup118alarm
import datetime
import time

class homedata(object):
    def __init__(self, pietime):
        ms = MSSoup118alarm()
        self.pietime = pietime
        self.time = int(time.mktime(datetime.date.today().timetuple()))
        self.sys = ms.search_alarm_sys_today_hist(self.time, self.pietime)
        self.dcap = ms.search_alarm_dcap_today_hist(self.time, self.pietime)
        self.dcaphist = ms.search_alarm_dcap_today(self.time, self.pietime)
        self.syshist = ms.search_alarm_sys_today(self.time, self.pietime)
        self.alldcap = self.dcaphist + self.dcap
        self.allsys = self.sys + self.syshist
        self.allalarm = self.alldcap + self.allsys

    def piedata(self):
        sum = {}
        res = []
        for x in self.allalarm:
            for y in x:
                if y in sum:
                    sum[y] += 1
                else:
                    sum[y] = 1
        sum['Middleware'] = sum['Middleware'] + sum['WebServer']
        del sum['WebServer']
        for x, y in sum.items():
            v = {}
            if x in ['Middleware']:
                v['x'] = '中间件'
                v['y'] = y
                res.append(v)
            elif x in ['OperatingSystem']:
                v['x'] = '操作系统'
                v['y'] = y
                res.append(v)
            elif x in ['Database']:
                v['x'] = '数据库'
                v['y'] = y
                res.append(v)
            else:
                v['x'] = '其他'
                v['y'] = y
                res.append(v)
        return res

    def alarm_total(self):
        return (len(self.allalarm))

    def today(self):
        unit = 3600
        nowtime = int(time.time())
        times = nowtime - (nowtime % unit)


if __name__ == '__main__':
    d = homedata()
    d.today()
