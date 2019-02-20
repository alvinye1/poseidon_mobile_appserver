# -*-coding: utf-8 -*-
'''
Created by jojo at 2018/7/5
'''
import os
import configparser
import tarfile

def get_config():
    """
    读取project.conf
    """
    pwd = os.path.dirname(os.path.realpath(__file__))
    conf_file = os.path.join(pwd, "../", "conf/project.conf")
    config = configparser.ConfigParser()
    config.read(conf_file)
    return config


if __name__ == '__main__':
    print ("test")
