# -*- coding: utf-8 -*-

import socket as sk
from ui import Mywindow
import threading
import os

'''
初始设置
'''
name = 'router'
port1 = 33330
host1_port = 33331
port2 = 33332
host2_port = 33333
port3 = 33334
host3_port = 33335
port4 = 33336
host4_port = 33337

'''
路由表,只包括Destination,Gateway,Genmask
'''

ip_table = [["1.0.0.0", "0.0.0.0", "255.0.0.0"], ["128.1.0.0", "0.0.0.0", "255.255.0.0"], ["192.168.0.3", "0.0.0.0", "255.255.255.255"], ["192.168.0.4", "0.0.0.0", "255.255.255.255"]]

def ip_to_int(ip):
    a = 0
    a += int(ip.split(".")[0]) * 0x1000000
    a += int(ip.split(".")[1]) * 0x10000
    a += int(ip.split(".")[2]) * 0x100
    a += int(ip.split(".")[3]) * 0x1
    return a

'''
路由器类
'''

class Router(object):
    def __init__(self, name):
        self.mutex = threading.Lock()
        self.name = name
        self.socket1 = sk.socket()
        self.socket2 = sk.socket()
        self.socket3 = sk.socket()
        self.socket4 = sk.socket()
        self.memory = []
        self.ui = Mywindow(self.name)
        self.init_router()
        t_q = threading.Thread(target = self.myquit)
        t_q.start()
        self.ui.init_ui()

    def handle_host(self, c, idx):
        message = bytes.decode(c.recv(100))
        self.mutex.acquire()
        self.memory.append(message)
        self.ui.show("memory store\n" + str(self.memory) + "\n")
        self.mutex.release()
        c.close()

    def server(self, socket, port, idx):
        socket.bind((sk.gethostname(), port))
        socket.listen(10)
        while True:
            c, addr = socket.accept()
            #print(addr)
            #t = threading.Thread(target = self.handle_host, args = (c,))
            #t.start()
            self.handle_host(c, idx)

    def forward(self, num):
        while True:
            self.mutex.acquire()
            if len(self.memory):
                message = self.memory[0]
                del(self.memory[0])
                header = message.split("\n")[0]
                data = message.split("\n")[1]
                ip = header.split(":")[1]
                self.ui.show2("Thread" + str(num) + "forward: " + ip + "\n")
                data = data[5:]
                s = sk.socket()
                host = sk.gethostname()
                r_ip = ip_to_int(ip)
                if (r_ip & ip_to_int(ip_table[0][2]) == ip_to_int(ip_table[0][0])):
                    idx = 0
                    self.ui.show2("Thread" + str(num) + "net_id: " + ip_table[0][0] + "\n")
                elif (r_ip & ip_to_int(ip_table[1][2]) == ip_to_int(ip_table[1][0])):
                    idx = 1
                    self.ui.show2("Thread" + str(num) + "net_id: " + ip_table[1][0] + "\n")
                elif (r_ip & ip_to_int(ip_table[2][2]) == ip_to_int(ip_table[2][0])):
                    idx = 2
                    self.ui.show2("Thread" + str(num) + "net_id: " + ip_table[2][0] + "\n")
                elif (r_ip & ip_to_int(ip_table[3][2]) == ip_to_int(ip_table[3][0])):
                    idx = 3
                    self.ui.show2("Thread" + str(num) + "net_id: " + ip_table[3][0] + "\n")
                try:
                    if (idx == 0):
                        s.connect((host, host1_port))
                        s.send(str.encode(data))
                        s.close()
                    elif (idx == 1):
                        s.connect((host, host2_port))
                        s.send(str.encode(data))
                        s.close()
                    elif (idx == 2):
                        s.connect((host, host3_port))
                        s.send(str.encode(data))
                        s.close()
                    elif (idx == 3):
                        s.connect((host, host4_port))
                        s.send(str.encode(data))
                        s.close()
                except ConnectionRefusedError as e:
                    e = e
                    self.mutex.release()
                    continue
            self.mutex.release()

    def init_router(self):
        t1 = threading.Thread(target = self.server, args = (self.socket1, port1, 0))
        t1.start()
        t2 = threading.Thread(target = self.server, args = (self.socket2, port2, 1))
        t2.start()
        t3 = threading.Thread(target = self.server, args = (self.socket3, port3, 2))
        t3.start()
        t4 = threading.Thread(target = self.server, args = (self.socket4, port4, 3))
        t4.start()
        t_forward_1 = threading.Thread(target = self.forward, args = (1,))
        t_forward_1.start()
        t_forward_2 = threading.Thread(target = self.forward, args = (2,))
        t_forward_2.start()
        t_forward_3 = threading.Thread(target = self.forward, args = (3,))
        t_forward_3.start()

    def myquit(self):
        input("enter to quit\n")
        os._exit(0)

router = Router(name)
