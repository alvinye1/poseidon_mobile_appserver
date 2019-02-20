# -*-coding: utf-8 -*-
import time

class Sourcedata():
    '''
    the source from poseidon_alarm_*
    '''
    def set_format(self, data, name):
        '''
        根据输入，生成前端需要的数据格式
        :param data: 来自数据库的原始数据
        :param name: 原始数据中，每段对应的数据名称
        :return: 键值对数据
        '''
        lendata = len(data)
        lenstr = len(name)
        try:
            sourcedata = {}
            i = 0
            for i in range(lenstr):
                if name[i] in ("START_TIME","Occurence"):
                    sourcedata[name[i]] =time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(data[i])))
                else:
                    sourcedata[name[i]] = data[i]
            return sourcedata
        except:
            print("Error data lenth =", lendata, "str lenth=", lenstr)


class Alarmdata():
    '''
    alarm data to table json
    '''

    def __init__(self, name, father_field, children_field, aargs):
        '''
        :param name: 数据表头
        :param father_field: 父ID列
        :param children_field: 子ID列
        :param args: 存入数据
        '''
        self.name = name
        self.data = aargs
        self.father_field = father_field
        self.children_field = children_field
        self.father_list = []
        self.children_list = []
        self.fatherid_pro = []
        self.fatherid = []
        self.fatherid_sed =[]
        self.format_list = []
        self.merchildrenlist = {}
        self.key = 0
        self.format()
        self.select_fatherid()
        self.select_fatherid_second()
        self.classify_father_chlidren()
        self.merge_children()

    def format(self):
        '''
        对输入数据进行格式化
        :return: 格式化后数据，键值对
        '''
        for i in self.data:
            single_alarm = Sourcedata().set_format(i, self.name)
            self.format_list.append(single_alarm)
            # print(self.format_list)

    def select_fatherid(self):
        '''
        根据制定key值，找出所有的父类
        :return:fatherid
        '''
        for i in self.format_list:
            if i[self.father_field] == i[self.children_field]:
                self.fatherid_pro.append(i[self.father_field])

    def select_fatherid_second(self):
        '''
        根据制定key值，找出所有的父类
        :return:fatherid
        '''
        for i in self.format_list:
            if (i[self.father_field] != i[self.children_field]) and (i[self.father_field] not in self.fatherid_pro):
                self.fatherid_sed.append(i[self.father_field])
        self.fatherid = self.fatherid_pro + self.fatherid_sed

    def classify_father_chlidren(self):
        '''
        将father和children分类
        :return: 一个list，list[0]是father，list[1]是children
        '''
        for i in self.format_list:
            if i[self.father_field] == i[self.children_field]:
                self.father_list.append(i)
            elif i[self.father_field] in self.fatherid_sed:
                self.father_list.append(i)
            else:
                self.children_list.append(i)

    def merge_children(self):
        for i in self.fatherid:
            chlidren = []
            for x in self.children_list:
                if i == x[self.father_field]:
                    chlidren.append(x)
                self.merchildrenlist[i] = chlidren

    def get_value(self, number, keyvalue, *args):
        self.value_number = number
        self.value_key = keyvalue
        self.value_data = args[0]
        for i in self.value_data:
            if i[self.value_key] == self.value_number:
                res = i
                return res

    def make_json(self):
        json = {"list": []}
        for i in self.fatherid:
            self.key += 1
            # alarm_cluster = {}
            father = self.get_value(i, self.father_field, self.father_list)  # 真正的父报警，需要补充方法
            father["key"] = self.key
            # father["chlidren"] = []     # 字典增加元素方法alarm_cluster = alarm_cluster.update(father)
            children = []
            # for x in self.merchildrenlist[i]:  # 找到父id为i的报警
            key_children = (self.key +1) * 1000
            if self.merchildrenlist == {}:         #新增当子报警为空时判断
                json["list"].append(father)
            else:
                x = self.merchildrenlist[i]
                if x != []:
                    for y in x:
                        key_children += 1
                        y['key'] = key_children
                        children.append(y)
                        father['children'] = children
                    # print(alarm_cluster)
                    json["list"].append(father)
                else:
                    json["list"].append(father)
                #     json["list"].append(father)
        return json

if __name__ == '__main__':
    start = time.time()
    print("==========test===========")
    a = Alarmdata(("name", "age", "key2"), "key2", "age", (("a", "1", "1"), ("b", "2", "2"), ("e", "5", "1"), ("f", "6", "3"),("g", "7", "4"),("h", "8", "1")))
    # a = Alarmdata(("NodeIP", "NodeAlias", "Component", "SummaryCN", "EventType", "START_TIME", "Occurence", "FREQUENCY", "EventNameCN", "CustomerSeverity", "SyslogID", "FatherEvent","FLAGBIT"), "FatherEvent",
    #                      "SyslogID",((u'80.16.161.92', u'pdccbccisdbsb53', u'SuSE', u'NTP OFFSET is too large', u'0', u'1543804201', u'1543900201', 161, u'NTP OFFSET TOO LARGE', u'7', 17024, 3, 2), (u'80.20.97.36', u'PDCCBNCTSAPPZH2', u'LINUX', u'\u4ea4\u6362\u7a7a\u95f4\u5229\u7528\u7387:swap_used_pct=25', 1, u'1543800149', u'1543900325', 835, u'\u4ea4\u6362\u7a7a\u95f4\u5229\u7528\u7387', u'7', 3, 3, 1), (u'80.32.225.73', u'PDCCBCCISNDM001', u'Windows', u'\u7cfb\u7edf\u5185\u5b58\u4f7f\u7528\u7387:memoryusage=100', 1, u'1543800159', u'1543899839', 167, u'\u7cfb\u7edf\u5185\u5b58\u4f7f\u7528\u7387', u'7', 5, 3, 1)))
    # print(a.format_list)
    b = a.make_json()
    print("asdsasaddsdsa",b)

    # #a = Alarmdata(,,,"",((u'80.16.145.127', u'pdccbebpfdbsro3', u'Linux', u'persondb delete arhcivelog before 1 day successfull...', u'0', u'1542618020', u'1542618020', 1, u'DELETE ARCHIVE LOG', u'7', 14894, 14894), (u'10.255.65.33', u'pdccjmimsdbsk33', u'None', u'name=/,disk_used_pct=82,disk_avail=1808,fs_total=10079', 1, u'1542352208', u'1542384037', 107, u'None', 5, 3644, 3644)))
    # end = time.time()
    # print(str(end - start))
    # a = Sourcedata()
    # b = a.set_format(("111"),("age"))
    # print b
