      #!/usr/bin/env python3
# ======================================
# POSEIDON PROGRAM FILE
# APPLICATION:
# Author:Alvin Ye .ICBC
# Version(Internal):1.0
# All rights reserved
# ======================================

from modules.app import create_app
from modules.net_detection import *

app = create_app(app_name="poseidon_mobile_appserver")

if __name__ == '__main__':
    app.run(host=get_address())

# from flask_script import Manager, Server
# manager = Manager(create_app)
# manager.add_command('runserver', Server(host='192.168.31.193', port=3345))
#

# if __name__ == '__main__':
#     manager.run()
#


# from flask import Flask
# app = Flask(__name__)
#
#
# @app.route('/')
# def hello_world():
#     return 'Hello World!'
#
#


# if __name__ == '__main__':
#     app.run()
