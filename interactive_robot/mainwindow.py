from PySide2.QtWidgets import*
from PySide2.QtCore import*
from PySide2.QtUiTools import*
from PySide2.QtGui import*
#from cuttinFaces import*  #modulo
import sys
import numpy as np 
import cv2
import time


face_cascade=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade=cv2.CascadeClassifier('haarcascade_eye.xml')
#smile_cascade=cv2.CascadeClassifier('haarcascade_smile.xml')

font=cv2.FONT_HERSHEY_SIMPLEX

class SpeakerBot(QMainWindow):
    def __init__(self):
        super(SpeakerBot,self).__init__()

        uifile=QFile("mainwindow.ui")

        uifile.open(QFile.ReadOnly)
        loader=QUiLoader()
        self.ui=loader.load(uifile)
        uifile.close()

        self.timerClean=QTimer()

        #------------ obtetos camara
        self.timerCam=QTimer()
        self.cam=cv2.VideoCapture(0)
        self.pixmap=QPixmap()
        #-------------------

        self.timerLabel=QTimer() #timer cambio mensajes label


        self.ui.setWindowTitle("Interactive Robot")

        self.ui.show()
        #self.ui.showMaximized() #full tamaño interface
        #self.timerCam.start(30) #activar camara
        #self.timerCam.stop()#detener camara

        #self.timerCam.timeout.connect(self.updateCam)



        self.ui.radioButton.toggled.connect(self.chec_camera) #radio buton 

        self.ui.button_connect.clicked.connect(self.Bconnect) #boton de conexion provisional

        self.ui.button_play.clicked.connect(self.Bplay)


        self.ui.pushQuit.clicked.connect(self.Quit_app)

        self.ui.button_talk.clicked.connect(self.Btalk) #boton talk

        self.ui.button_left.clicked.connect(self.Bleft) #boton left

        self.ui.button_right.clicked.connect(self.Bright) #boton right
        

    def Bplay(self):
        #print("boton play")
        #self.ui.label_feedback.setText("play")

        self.timerLabel.timeout.connect(self.clean_label)
        self.timerLabel.start(1000)
        #self.timerLabel.stop()
        self.ui.label_feedback.setText("second")


    def clean_label(self):
         
        #lis_mesages=["play","next step","really?"]
        self.ui.label_feedback.setText("play ")
        


    def chec_camera(self): #activa camara con radio buton
        if self.ui.radioButton.isChecked():
            self.timerCam.start(30) #activar camara
            self.timerCam.timeout.connect(self.fac3_detect)
        else:
            self.timerCam.stop()#detener camara
            #self.pixmap.fill(Qt.transparent)
            #self.widgetUi.camLabel.setPixmap(self.pixmap)


    def fac3_detect(self):
        if self.cam.isOpened():
            ret,frame=self.cam.read()
            frame=cv2.flip(frame,1) #camara sin mirror
            gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            #faces=face_cascade.detectMultiScale(gray,1.5,5)
            faces=face_cascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(200, 200),flags=cv2.CASCADE_SCALE_IMAGE)
            if not ret:
                return 
            for (x,y,w,h) in faces: #----------------------face
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),3) #rectangle face
                roi_gray=gray[y:y+h, x:x+w]
                roi_color=frame[y:y+h, x:x+w]

                eyes=eye_cascade.detectMultiScale(roi_gray)
                for (ex,ey,ew,eh) in eyes: #------------------ojos
                    cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),3) #eyes rectangle
                    cv2.putText(frame,'Faces:' + str(len(faces)),(10, 86), font, 1,(0,0,0),2) #message 

            image=QImage(frame,frame.shape[1],frame.shape[0],frame.shape[1]*frame.shape[2],QImage.Format_RGB888) #image made
            self.pixmap.convertFromImage(image.rgbSwapped())
            self.ui.camLabel.setPixmap(self.pixmap) #nombre label hecho en .ui

    def Quit_app(self):
        QCoreApplication.quit()

    def Btalk(self):
        print("boton talk")

    def Bright(self):
        print("boton right")

    def Bleft(self):
        print("boton left")

    def Bconnect(self):
        #print("boton conexion")
        self.ui.label_conection.setText("Connected")

