import os, sys
import ftplib
import FaceRecognizer
import Socket

def rec():
    _host = 'localhost'
    obj = FaceRecognizer.FaceRecognizer()
    cond, name = obj.recognize()
    if cond:
        Socket.Socket(_host,name)
    else:
        print "Access denied"
        sys.exit

def train():
    FaceRecognizer.FaceRecognizer().train()

def main():
    option = raw_input("Do you want to train or search? ")
    if option=='train':
        train()
    else:
        rec()

if __name__ == '__main__':
    main()