import Snowboy.snowboydecoder as snowboydecoder
#import snowboydecoder
import serial
arduino=serial.Serial('/dev/ttyACM0',9600)

def protected():
	print("word detected, you said chapie")
	comand='l'
	arduino.write(comand.encode())

#detectorBack=snowboydecoder.HotwordDetector("chapie.pmdl",sensitivity=0.5,audio_gain=1)
#detectorBack.start(protected)

while 1:
	archivo=open("file.txt","r")
	for line in archivo.readlines():
		if line=="key":
			print("received keyword from Qt")
			detectorBack=snowboydecoder.HotwordDetector("chapie.pmdl",sensitivity=0.5,audio_gain=1)
			detectorBack.start(protected)



