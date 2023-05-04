import atexit
import os
import sys
from datetime import datetime
from time import sleep
import json
import psutil
import configparser
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

class MainWindow(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Playtime Tracker")
        self.setWindowIcon(QIcon('logo.png'))
        self.setGeometry(400, 400, 400, 300)

        label = QLabel("Waiting for game...")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(label)

        

    def gameFound(self):
        label = QLabel("Tracking...")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(label)


def scanForGame(gamesList):
    for proc in psutil.process_iter():
        if proc.name() in gamesList:
            return proc.name()
    return False

def saveSession():
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






config = configparser.ConfigParser()
config.optionxform = str
config.read('config.ini')

gamesPath = config['DEFAULT']['GamesPath']


# SCAN FOR GAME LOOP, break if game found
with open('gamesExeNames.json', 'r') as file:
    gamesDict = json.load(file)

gamesProcessList = list(gamesDict.keys())

while True:
    gameProcessName = scanForGame(gamesProcessList)

    if gameProcessName:
        print('GAME FOUND!')
        gameFullName = gamesDict[gameProcessName]
        break

    sleep(10)


sT = datetime.now().replace(microsecond=0)
startDate = sT.strftime("%d-%m-%Y")
startTime = sT.strftime("%H:%M:%S")


path = os.path.join(gamesPath, gameFullName)

# CREATE FOLEDR IF NOT EXISTS
if not os.path.isdir(path):
    os.makedirs(path)

# ADD NEW FILE AFTER LAST INDEX OR START AT 1 IF NONE EXIST
if not os.listdir(path):
    newSessionIndex = str(1)
else:
    lastSessionIndex = int(os.listdir(path)[-1].replace('.json', ''))
    newSessionIndex = str(lastSessionIndex + 1)

atexit.register(saveSession)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()