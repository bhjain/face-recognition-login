import urllib2
import os
import main
import sys

class Loader(object):
    def __init__(self):
        _FLAG = 1
        if self.isConnected():
            print "Connection successful"
        else:
            _FLAG = 0
            print "Connection failed"
        if self.isExists():
            print "All files intact"
        else:
            _FLAG = 0
            print "Files missing"

        if _FLAG:
            main.main()
        else:
            sys.exit

    def isConnected(self):
        print "Check network connection..."
        try:
            response = urllib2.urlopen('http://74.125.68.106', timeout=1)
            return True
        except urllib2.URLError as err:
            pass
        return False

    def isExists(self):
        FILE_EXIST = 1
        print "Checking file system..."
        if os.path.exists("db"):
            print "db/ = True"
            if os.path.exists("db/client_name.csv"):
                print "client_name.csv = True"
            else:
                print "client_name = False"
                FILE_EXIST = 0
            if os.path.exists("db/train_db.csv"):
                print "train_db.csv = True"
            else:
                print "train_db.csv = False"
                FILE_EXIST = 0
        else:
            print "db/ = False"
            FILE_EXIST = 0

        if os.path.exists("assets"):
            print "assets/ = True"
            if os.path.exists("assets/client_match/"):
                print "client_match = True"
                if os.path.exists("assets/client_match/client_face.jpg"):
                    print "client_face.jpg = True"
                else:
                    print "client_face.jpg = False"
                    FILE_EXIST = 0
            else:
                print "client_match = False"
                FILE_EXIST = 0
            if os.path.exists("assets/haarcascades/"):
                print "haarcascades = True"
                if os.path.exists("assets/haarcascades/haarcascade_frontalface_alt.xml"):
                    print "haarcascade_frontalface_alt.xml = True"
                else:
                    FILE_EXIST = 0
            else:
                FILE_EXIST = 0
            if os.path.exists("assets/trainingset"):
                print "trainingset = True"
            else:
                print "trainingset = False"
                FILE_EXIST = 0
        if os.path.exists("FaceRecognizer.py"):
            print "FaceRecognizer.py = True"
        else:
            print "FaceRecognizer.py = False"
            FILE_EXIST = 0
        if os.path.exists("Socket.py"):
            print "Socket.py = True"
        else:
            print "Socket.py = False"
            FILE_EXIST = 0

        if FILE_EXIST:
            return True
        else:
            return False
        
if __name__ == '__main__':
    Loader()

