from PySide2.QtWidgets import*
from PySide2.QtCore import*
from PySide2.QtUiTools import*
from PySide2.QtGui import*
#from cuttinFaces import*  #modulo
import sys
import numpy as np 
import cv2
import time
import serial
import speech_recognition as sr 
from pocketsphinx import LiveSpeech

arduino=serial.Serial('/dev/ttyACM0',9600) #conexion arduino via serial

face_cascade=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade=cv2.CascadeClassifier('haarcascade_eye.xml')
#smile_cascade=cv2.CascadeClassifier('haarcascade_smile.xml')

#detectorBack=snowboydecoder.HotwordDetector("chapie.pmdl",sensitivity=0.5,audio_gain=1) #key word

r=sr.Recognizer()

font=cv2.FONT_HERSHEY_SIMPLEX

class SpeakerBot(QMainWindow):
    def __init__(self):
        super(SpeakerBot,self).__init__()

        uifile=QFile("mainwindow.ui")

########-------------------------------
        f=QFile("file.txt")  
        f.open(QIODevice.WriteOnly)
        out=QTextStream(f)
        out<<"" #elimina palabra previamente cargada en txt

###################-----------------
        uifile.open(QFile.ReadOnly)
        loader=QUiLoader()
        self.ui=loader.load(uifile)
        uifile.close()
        self.timer=QTimer() #timer file
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

        #self.ui.button_connect.clicked.connect(self.Bconnect) #boton de conexion provisional

        #self.ui.button_play.clicked.connect(self.Bplay)


        self.ui.pushQuit.clicked.connect(self.Quit_app)

        self.ui.button_talk.clicked.connect(self.sendata) #boton talk

        self.ui.keybutton.clicked.connect(self.send_key_word) #boton keyword

        self.ui.button_forward.clicked.connect(self.Bforward) #boton forward

        self.ui.button_back.clicked.connect(self.Bback) #boton move back
        

    '''def Bplay(self):
        #print("boton play")
        #self.ui.label_feedback.setText("play")

        self.timerLabel.timeout.connect(self.clean_label)
        self.timerLabel.start(1000)
        #self.timerLabel.stop()
        self.ui.label_feedback.setText("second")'''
        
        
    def sendata(self):
        self.timer.start(500)
        self.timer.timeout.connect(self.Btalk)

    def send_key_word(self):
        self.timer.start(500)
        self.timer.timeout.connect(self.key_word)
        
    def clean_label(self):
        self.ui.label_feedback.setText("")
        

    def chec_camera(self): #activa camara con radio buton
        if self.ui.radioButton.isChecked():
            self.timerCam.start(30) #activar camara
            self.timerCam.timeout.connect(self.fac3_detect)
        else:
            self.ui.camLabel.setPixmap('black.jpg') #fondo negro
            self.timerCam.stop()#detener camara
            #self.pixmap.fill(Qt.transparent)
            #self.ui.camLabel.setPixmap(self.pixmap) #nombre label hecho en .ui


    def fac3_detect(self):
        if self.cam.isOpened():
            ret,frame=self.cam.read()
            frame=cv2.flip(frame,1) #camara sin mirror
            gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            #faces=face_cascade.detectMultiScale(gray,1.5,5)
            faces=face_cascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(200, 200),flags=cv2.CASCADE_SCALE_IMAGE)
            x=len(faces) #aloja cantidad de rostros 
            cv2.putText(frame,'Faces:' + str(x),(10, 86), font, 1,(0,0,0),2) #message on screen num faces
            if x==0:
                self.ui.label_people.setText(str(x)+" come closer...") #show people like feedback on interfaz
            else:
                self.ui.label_people.setText(str(x)) #show people like feedback on interfaz
            if not ret:
                return 
            for (x,y,w,h) in faces: #----------------------face
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),3) #rectangle face
                roi_gray=gray[y:y+h, x:x+w]
                roi_color=frame[y:y+h, x:x+w]
                eyes=eye_cascade.detectMultiScale(roi_gray)
                for (ex,ey,ew,eh) in eyes: #------------------ojos
                    cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),3) #eyes rectangle
                    #cv2.putText(frame,'Faces:' + str(len(faces)),(10, 86), font, 1,(0,0,0),2) #message 
                    #self.ui.label_people.setText(str(len(faces))) #show people like feedback on interfaz

            image=QImage(frame,frame.shape[1],frame.shape[0],frame.shape[1]*frame.shape[2],QImage.Format_RGB888) #image made
            self.pixmap.convertFromImage(image.rgbSwapped())
            self.ui.camLabel.setPixmap(self.pixmap) #nombre label hecho en .ui

            #self.ui.label_people.setText("") #show people like feedback on interfaz

    def Quit_app(self):
        QCoreApplication.quit()

    def key_word(self):#metodo iniciar palabra clave en voice_control.py
        print("keyword")
     
        #f=QFile("file.txt")
        #f.open(QIODevice.WriteOnly)
        #out=QTextStream(f)
        #out<<"" #elimina contenido basura anterior en txt 
        #out<<"key"

    def Btalk(self):#metodo para iniciar comandos de voz en raspduino.py

        f=QFile("file.txt")
        f.open(QIODevice.WriteOnly)
        out=QTextStream(f)
        out<<"" #elimina contenido basura anterior en txt 
        out<<"hellooo"
        #self.timerLabel.timeout.connect(self.clean_label)
        #self.timerLabel.start(1000)
        #self.ui.label_feedback.setText("im fine")
        '''with sr.Microphone() as source:
            print("Listening...")
            self.ui.label_text.setText("Listening...")
            audio=r.listen(source)
    
        try:
            print("Sphinx thinks you said: "+r.recognize_sphinx(audio))
            self.ui.label_text.setText("You said: "+r.recognize_sphinx(audio))
            if (r.recognize_sphinx(audio)=='lights on'): #led on 
                comando='h'
                arduino.write(comando.encode())
            elif (r.recognize_sphinx(audio)=='one'): #led off
                comando='l'
                arduino.write(comando.encode())
            elif (r.recognize_sphinx(audio)=='come back'): #movimiento atras robot
                comando='b'
                arduino.write(comando.encode())
            elif (r.recognize_sphinx(audio)=='come to me'): #movimiento adelante robot
                comando='f' 
                arduino.write(comando.encode()) #envia caracter to arduino

        except sr.UnknownValueError:
            self.ui.label_feedback.setText("")
        except sr.RequestError as e:
            self.ui.label_feedback.setText("")'''

    def Bback(self):
        self.ui.label_feedback.setText("Moving Back...")
        print("boton back") #movimiento adelante robot
        comando='b'
        arduino.write(comando.encode())
        self.timerLabel.timeout.connect(self.clean_label) #borra 
        self.timerLabel.start(3000)

    def Bforward(self):
        self.ui.label_feedback.setText("Moving Forward...")
        print("boton forward") #movimiento atras robot
        comando='f'
        arduino.write(comando.encode())
        self.timerLabel.timeout.connect(self.clean_label)
        self.timerLabel.start(3000)
