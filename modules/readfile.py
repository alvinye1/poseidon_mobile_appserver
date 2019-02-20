# -*- coding:utf-8 -*-
__author__ = 'sysop'

import os
import socket
import sys
import simplejson as json
#from modules.file_sender import *



class NMONfile(object):


    def __init__(self,hostname):
        self.host = hostname # hostname
        # self.path = str   # directory
        # self.files = os.listdir(self.path)  # filenames

    def get_names(self):
        return self.files

    # def get_first_line(self):
    #     return self.files



    # get messages from socket
    def get_messages(self,ip,port,date):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        c = {'type': 'instant_nmon', 'data': date}
        # c = {'type': 'instant_nmon', 'data': '181130'}
        s.send(json.dumps(c).encode(encoding='utf8'))

        total_data = ''
        while True:
            data = s.recv(10240000).decode('utf-8')
            if not data:
                break
            total_data += data

        # print("total_datatotal_datatotal_datatotal_data",total_data)
        json_total = json.loads(total_data)
        self.files = list(json_total.keys()) # all file names
        self.files.sort()
        #print(len(self.files))
        #print(self.files)
        self.files.remove("VM.json")
        # self.files.remove("test.sh")
        self.infos = []
        self.files_content = {}
        i = 0
        #for file in self.files:
        while i < len(self.files):

            file = self.files[i]

            if(len(json_total[file]) == 0):

                self.files.remove(file)
                #i -= 1
                continue
            #else:#print(file)

            i += 1


            content = json_total[file].replace(",\n", ",")
            content_str = "[" + content[0:len(content) - 1] + "]"
            content_list = json.loads(content_str, encoding="utf-8")

            line_first = content_list[0]


            content_list[0] = line_first

            self.infos.append(line_first)
            self.files_content[file] = content_list


        self.get_cols_fields()
        print(self.type)

        return [self.files,self.cols,self.fields,self.files_content,self.type]



        # result
        # cpu_6 = cpu.replace(",\n",",")
        # print(cpu_6)
        # cpu_ff = "["+cpu_6[0:len(cpu_6)-1]+"]"
        # cpu_4 = json.loads(cpu_ff,encoding="utf-8")
        # print(cpu_4)
        # print(type(cpu_4))




    # handle massages from socket
    def handle_massages(self):
        return self.json_total



    # all files first line
    def get_file_infos(self,):
        self.infos = []
        for file in self.files:
            domain = os.path.abspath(self.path)
            file = os.path.join(domain, file)
            file = open(file, 'r')
            file_json = json.load(file)
            #print(file_json[0])
            file.close()
            line = file_json[0]
            for key in line.keys():
                if (key.find(self.host) != -1):
                    #print("1 "+line[key])
                    continue
                if (len(key) == 0 or line[key] == '-nan'):
                    #print("2 "+line[key])
                    continue
                line[key] = float(line[key])
            self.infos.append(line)




    # get all cols and fields
    def get_cols_fields(self):
        self.fields = {}
        self.cols = []
        self.type = []
        for info in self.infos:

            key_list = []
            keys = list(info.keys())
            i = 0
            type = []
            while i < len(keys):
                if(keys[i].find(self.host) != -1):
                    col = keys[i]
                    self.cols.append(keys[i])
                    keys.remove(keys[i])
                    i -=1
                elif(len(keys[i]) == 0 or info[keys[i]] == "" or info[keys[i]] == '-nan'):
                    keys.remove(keys[i])
                    i -= 1

                if(keys[i].find("%") != -1):
                    type_tmp = "%"
                    if keys[i] not in type:
                        type.append(type_tmp)
                elif(keys[i].find("KB/s") != -1):
                    type_tmp = "KB/s"
                    if keys[i] not in type:
                        type.append(type_tmp)
                elif(keys[i].find("/s") != -1):
                    type_tmp = "/s"
                    if keys[i] not in type:
                        type.append(type_tmp)
                else:
                    type_temp = " "
                #else:print(list[i])

                i += 1
            self.fields[col] = keys

            if (len(type) > 1):
                self.type.append(type[1])
            elif (len(type) == 1):
                self.type.append(type[0])
            else:
                self.type.append(" ")

        return [self.cols, self.fields,self.type]
