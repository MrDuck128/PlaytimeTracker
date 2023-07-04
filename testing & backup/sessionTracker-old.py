import atexit
import os
import sys
from datetime import datetime
from time import sleep
import json
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

game = sys.argv[1:][0]
path = os.path.join("C:\Programski-kod\Playtime Tracker\Games", game)

if not os.listdir(path):
    newSessionIndex = str(1)
else:
    lastSessionIndex = int(os.listdir(path)[-1].replace('.json', ''))
    newSessionIndex = str(lastSessionIndex + 1)

sT = datetime.now().replace(microsecond=0)
startDate = sT.strftime("%d-%m-%Y")
startTime = sT.strftime("%H:%M:%S")



def saveSession():
    sleep(2)
    eT = datetime.now().replace(microsecond=0)
    endDate = eT.strftime("%d-%m-%Y")
    endTime = eT.strftime("%H:%M:%S")
    difference = eT - sT

    data = {
        "startDate": startDate,
        "startTime": startTime,
        "endDate": endDate,
        "endTime": endTime,
        "difference": str(difference)
    }
    with open(os.path.join(path, newSessionIndex+".json"), 'w') as file:
        file.write(json.dumps(data, indent=4))

atexit.register(saveSession)



class MainWindow(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Playtime Tracker")

        label = QLabel("Super!")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(label)

        quitButton = QPushButton("Exit")
        quitButton.clicked.connect(self.buttonClicked)

    def buttonClicked(self):
        QCoreApplication.instance().quit()



app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()