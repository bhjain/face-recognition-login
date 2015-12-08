import socket
import ftplib
import getpass
import os, sys

class Socket(object):
    def __init__(self, _host, name):
        os.system('cls')
        self._user = name
        self._host = _host
        self.sos_port = 8080
        self.ftp_port = 21
        self.notify_port = 10000
        self._client = ftplib.FTP()

        self.menu()

    def ftpconnect(self):      
        try:
            _pass = getpass.getpass("Pass: ")
            self._client.connect(self._host, self.ftp_port)
            self._client.login(_user, _pass)
        except ftplib.error_perm as e:
            print str(e)
            sys.exit
        except IOError as e:
            print str(e)
            sys.exit
        finally:
            self._client.close()

    def menu(self):
        print """
================================================================================
            
            ##            ##  ##########  ##      ##  ##      ##
            ####        ####  ##          ####    ##  ##      ##
            ## ##      ## ##  ##          ## ##   ##  ##      ##
            ##  ##    ##  ##  ##########  ##  ##  ##  ##      ##
            ##   ##  ##   ##  ##          ##   ## ##  ##      ##
            ##    ####    ##  ##          ##    # ##  ##      ##
            ##     ##     ##  ##########  ##      ##  ##########

================================================================================"""
        choice = raw_input("Please type sos to connect: ")
        if choice == 'sos':
            self.sos()
        elif choice == 'search':
            pass
        elif choice == 'notifications':
            pass
        elif choice == 'exit':
            sys.exit
        else:
            print "incorrent choice"
            self.menu()

    def sos(self):
        os.system('cls')
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self._host, self.sos_port))

        try:
            message = raw_input("msg > ")
            long = raw_input("long > ")
            lat = raw_input("lat > ")
            msg = self._user + ";"+ message + ";" + long + ";" + lat;

            client.sendall(RSAEncrypt(msg))
            print "SOS sent"
        finally:
            client.close()

    def gcd(self, a, b):
        if b == 0:
            return a
        else:
            return gcd(b, a%b)

    def RSAEncrypt(self, msg):
        p = 37
        q = 43
        n = p*q

        e = 2
        for e in xrange(n):
            if gcd(e, (p-1)*(q-1)) == 1:
                break

        encr_msg = ""
        for i in msg:
            encr_msg += str(pow(ord(i),e)%n) + " "

        return encr_msg, e, n
