import sys
import mainwindow
from PySide2.QtWidgets import*

if __name__=="__main__":
    App=QApplication(sys.argv)
    Bot=mainwindow.SpeakerBot()
    App.exec_()


