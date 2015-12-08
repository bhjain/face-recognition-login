import numpy as np
import os, sys, cv2, time
from PIL import Image
import main

class FaceRecognizer(object):
    def __init__(self):
        self.CascadePath = "assets/haarcascades/haarcascade_frontalface_alt.xml"
        self.ClientPath = "db/PredictionDatabase.csv"
        self.GenderPath = "db/GenderDatabase.csv"
        self.TrainingDBPath = "db/TrainingDatabase.csv"
        self.XML = "assets/face_trained.xml"
        self.genderXML = "assets/gender_trained.xml"
        self.ClientImage = ""
        self.FaceCascade = cv2.CascadeClassifier(self.CascadePath)
        self.Recognizer = cv2.createLBPHFaceRecognizer()
        self.GenderRecognizer = cv2.createLBPHFaceRecognizer()
        self.UserName = "Tom Cruise"
        self.FLAG = 0   # Utility flag

    def train(self):
        # if not os.path.exists(self.XML) or not os.path.exists(self.genderXML):
        ImagesLabels = [ x.split(';') for x in [ x.rsplit('\n')[0] for x in open(self.TrainingDBPath)]]
        images = []
        labels = []
        genders = []

        for (path, label, gen) in ImagesLabels:
            try:
                image = cv2.imread(path, 0)
            except Exception, e:
                continue
            faces = self.FaceCascade.detectMultiScale(image)
            for (x,y,w,h) in faces:
                images.append(image[y:y+h, x:x+w])
                labels.append(int(label))
                genders.append(int(gen))

        self.Recognizer.train(images, np.array(labels))
        self.GenderRecognizer.train(images, np.array(genders))
            
        # Save to XMLs
        self.Recognizer.save(self.XML)
        self.GenderRecognizer.save(self.genderXML)
        #else:
        #    self.Recognizer.load(self.XML)
        #    self.GenderRecognizer.load(self.genderXML)

        # self.recognize()
        print "Training complete"
        main.main()

    def recognize(self):
        if os.path.exists(self.XML) and os.path.exists(self.genderXML):
            filepath = raw_input("Enter file path > ")
            if not os.path.exists(filepath):
                return self.FLAG, self.UserName
            
            self.ClientImage = filepath
            self.Recognizer.load(self.XML)
            self.GenderRecognizer.load(self.genderXML)

            # Getting data from the prediction database csv file
            List1 = [ x.split(';') for x in [ x.rsplit('\n')[0] for x in open(self.ClientPath)]]
            List2 = [x.split(';') for x in [ x.rsplit('\n')[0] for x in open(self.GenderPath)]]
        
            NAMES = ["" for x in xrange(len(List1))]
            GENDERS = ["" for x in xrange(len(List2))]
        

            # Appending names to labels
            for (l,n) in List1:
                NAMES[int(l)] = str(n)

            for (l,g) in List2:
                GENDERS[int(l)] = str(g)

            # Creating a window
            cv2.cv.NamedWindow("Input", cv2.CV_WINDOW_AUTOSIZE)

            # Read image 
            dst = cv2.imread(self.ClientImage)

            # Resizing image
            #rows, cols, t = dst.shape
            #dst = cv2.resize(dst, (int(0.8*cols), int(0.8*rows)))

            # Coverting to RGB image to Grayscale
            gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)

            # Face detection
            faces = self.FaceCascade.detectMultiScale(gray)
            

            # Face recognition
            for (x,y,w,h) in faces:
                prediction, faceconf = self.Recognizer.predict(gray[y:y+h, x:x+w])
                genderPredict, genderconf = self.GenderRecognizer.predict(gray[y:y+h, x:x+w])

                # Create rectangle around face
                if NAMES[prediction] == self.UserName:
                    cv2.rectangle(dst, (x, y-25), (x+w,y-5), (57,220,205),-1)
                    cv2.rectangle(dst, (x, y), (x+w, y+h), (3, 255, 118), 2)
                    cv2.putText(dst, NAMES[prediction], (x+10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0))
                    self.FLAG = 1
                else:
                    cv2.rectangle(dst, (x, y), (x+w, y+h), (0, 0, 213), 2)
                if not self.FLAG == 1:
                    print "Prediction = "+ str(NAMES[prediction+1])
                print "Confidence = "+ str(faceconf)
                cv2.rectangle(dst, (x, y+h+25), (x+w, y+h+50), (224, 208, 191), -1)
                cv2.putText(dst, GENDERS[genderPredict], (x+20,y+h+40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0))
        
            cv2.imshow("Input", dst)
            if cv2.waitKey(0) & 0xFF==ord('q'):
                cv2.destroyAllWindows()
            return self.FLAG, self.UserName
        else:
            print "Files missing"
            return self.FLAG, self.UserName



