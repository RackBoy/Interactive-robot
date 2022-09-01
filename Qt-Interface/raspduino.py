import serial 
import Snowboy.snowboydecoder as snowboydecoder
import speech_recognition as sr 
from pocketsphinx import LiveSpeech

arduino=serial.Serial('/dev/ttyACM0',9600)
r=sr.Recognizer()
print("now the beginning...")



while 1:
	#detectorBack.start(protected) #snowboy
	archivo=open("file.txt","r")
	for line in archivo.readlines():
		if line=="hellooo":
			print("received word from Qt")
			with sr.Microphone() as source:
				print("Listening...")
				audio=r.listen(source)

			try:
				print("Sphinx thinks u said: "+r.recognize_sphinx(audio))
				#if(r.recognize_sphinx(audio)=='go forward'):
				if(r.recognize_sphinx(audio)=='lights on'):
					comando='f'
					arduino.write(comando.encode())
				#elif(r.recognize_sphinx(audio)=='go back'):
			elif(r.recognize_sphinx(audio)=='one'):
					comando='b'
					arduino.write(comando.encode())
			except sr.UnknownValueError:
				print("Error...")

