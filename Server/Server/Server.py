import socket
import thread
import threading
import os
import sys
import numpy as np
import subprocess
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

class Trinity(object):
    def __init__(self):
        self._host = "localhost"
        self.ftp_port = 21
        self.sos_port = 8080
        self.notify_port = 10000

        ftpThread = threading.Thread(target=self.ftpserver)
        interfaceThread = threading.Thread(target=self.interface)
        sosThread = threading.Thread(target=self.sosserver)
        ftpThread.start()
        interfaceThread.start()
        sosThread.start()
        #subprocess.Popen("cmd.exe /c start python ftpserver.py")

    def ftpserver(self):
        authorizer = DummyAuthorizer()
        authorizer.add_user("bhavya","123","./assets",perm="raw")
        
        handler = FTPHandler
        handler.authorizer = authorizer

        server = FTPServer((self._host, self.ftp_port), handler)
        server.serve_forever()

    def sosserver(self):
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.bind((self._host, self.sos_port))

        threads = []
        while True:
            tcp.listen(5)
            print "\nListening for incoming connections..."
            client, (ip,port) = tcp.accept()

            t = SosClient(ip,port,client)
            t.start()
            threads.append(t)

        for i in threads:
            i.join()

    def interface(self):
        print "Welcome to Trinity"
        f = raw_input("> ")
        print f

class SosClient(threading.Thread):

    def __init__(self, host, port, socket):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.socket = socket

    def run(self):
        self.socket.send("\nTRINITY\n\n")
        data = "dummy"

        try:
            while len(data):
                data,e,n = self.socket.recv(2048)
                msg = RSADecrypt(data,e,n)

                info = msg.split(';')
                print "SOS from " + str(self.host) + ":" + str(self.port)
                print info[0]
                print "message - " + info[1]
                print "Longitude - " + str(info[2])
                print "Latitude - " + str(info[3])
        except Exception as e:
            pass

    def RSADecrypt(self, data, e, n):
        p = 37
        q = n/p

        for d in xrange(1,n):
            if (d*e)%((p-1)*(q-1)) == 1:
                break

        msg = data.split(" ")
        decr_msg = ""
        for i in msg:
            if i != '':
                decr_msg += chr(pow(int(i),d)%n)

        return decr_msg


        
Trinity()