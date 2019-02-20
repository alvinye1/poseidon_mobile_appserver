# ======================================
# POSEIDON PROGRAM FILE
# APPLICATION:
# Author:Alvin Ye .ICBC
# Version(Internal):1.0
# All rights reserved
# ======================================
import time
import configparser
import logging
import os


def log(string):
    t = time.strftime(r"%Y-%m-%d_%H-%M-%S", time.localtime())
    print("[%s]%s" % (t, string))


def duplicate(one_list):
    # list prove to remove the same alarm in a moment
    temp_list = []
    for one in one_list:
        if one not in temp_list:
            temp_list.append(one)
    return temp_list


class GetConfig:
    def __init__(self):
        pwd = os.path.dirname(os.path.realpath(__file__))
        conf_file = os.path.join(pwd, "../conf", "poseidon_server.conf")
        self.config = configparser.ConfigParser()
        self.config.read(conf_file)

    def get(self, section, option):
        return self.config.get(section=section, option=option)


def log_level():
    cfg = GetConfig()
    loglevel = cfg.get('BASIC', 'LOG_LEVEL')
    logging.basicConfig(level=loglevel, format='%(asctime)s %(name)s %(levelname)s:%(message)s')


# initialize log level status
log_level()
# initialize configuration
config = GetConfig()

