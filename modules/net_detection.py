#!/usr/bin/env python
# ======================================
# POSEIDON PROGRAM FILE
# APPLICATION:
# Author:Alvin Ye .ICBC
# Version(Internal):1.0
# All rights reserved
# ======================================

import socket
import ifcfg

PRODUCTION_AREA = '80.7.83.'


def get_address():
    address = ifcfg.default_interface()['inet']
    return address


def area_detect():
    """to define whether it's in the production envirorment or the test one"""
    address = get_address()
    if address.find(PRODUCTION_AREA) == -1:
        # this is a test area
        return 'test'
    else:
        # this is a production area
        return 'production'


