# -*- coding: utf-8 -*-

import socket as sk
import os
import time
from ui import Mywindow
import random
import threading

'''
初始设置
'''
name = 'host2'
ip = "128.1.1.2"
port = 33333
router_port = 33332
remotes = ["1.1.1.1", "192.168.0.3", "192.168.0.4"]

'''
主机类
'''
 
class Host(object):
    def __init__(self, name, port):
        self.name = name
        self.port = port
        self.socket = sk.socket()
        self.ui = Mywindow(self.name)
        self.init_host()
        self.ui.init_ui()

    def handle_host(self, c):
        message = bytes.decode(c.recv(100))
        myfile = open(self.name + ".txt", "a")
        myfile.write(message + "\n")
        myfile.close()
        self.ui.show2("recv:" + message + "\n")
        c.close()

    def server(self, socket, port):
        socket.bind((sk.gethostname(), port))
        socket.listen(10)
        while True:
            c, addr = socket.accept()
            #print(addr)
            #t = threading.Thread(target = self.handle_host, args = (c,))
            #t.start()
            self.handle_host(c)

    def init_host(self):
        t1 = threading.Thread(target = self.server, args = (self.socket, self.port))
        t1.start()
        t2 = threading.Thread(target = self.send_message)
        t2.start()
        t_q = threading.Thread(target = self.myquit)
        t_q.start()

    def send_message(self):
        i = 0
        while True:
            message = ""
            message += "header:" + remotes[random.randint(0, 2)] + "\n"
            message += "data:" + str(os.getpid()) + ":" + str(port) + ":" + str(i) + ":" + "161730213" + "\n"
            b_message = str.encode(message)
            s = sk.socket()
            host = sk.gethostname()
            s.connect((host, router_port))
            s.send(b_message)
            self.ui.show("send:\n" + message)
            s.close()
            i = i + 1
            time.sleep(1)

    def myquit(self):
        input("enter to quit\n")
        os._exit(0)

host = Host(name, port)