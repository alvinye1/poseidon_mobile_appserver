# ======================================
# POSEIDON PROGRAM FILE
# APPLICATION:
# Author:Alvin Ye .ICBC
# Version(Internal):1.0
# All rights reserved
# ======================================

import logging
import json
import socket
import sys

'''
Usage:
First connect the server:
s = Singal(host,port)

Then exec command:
result = s.run(type,data)

Then close:
del s
'''


class Signal:
    """to connect to the minion and control or get messages etc."""

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.host, self.port))
        self.s.settimeout(5)

    def reconnect(self):
        self.s.close()
        self.s.connect((self.host, self.port))
        self.s.settimeout(5)

    def run(self, type, data):
        """execute command identified by type arg"""
        try:
            # eval("self.%s" % type)(data)
            c = {'type': type, 'data': data}
            self.s.send(json.dumps(c).encode(encoding='utf8'))
        except:
            logging.error("[SIGNAL]no function found or excute failed.")

        # decode messages
        total_data = ''
        while True:
            data = self.s.recv(10240000).decode('utf-8')
            if not data:
                break
            total_data += data

        # get json data
        json_total = json.loads(total_data)
        # return messages
        return json_total

    def __del__(self):
        self.s.close()

    def nmon(self):
        pass

    def instant_nmon(self):
        pass

    def instant_script(self):
        pass

    def script(self):
        pass

    def instant_heartbeat(self):
        pass

    def deploy_update(self):
        pass

# if __name__ == '__main__':
#     s = Signal("80.2.238.218",8885)
#     result = s.run("instant_script", "asdfsdf")
#     print  (result)