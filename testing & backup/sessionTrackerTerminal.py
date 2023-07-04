import atexit
import os
from datetime import datetime
from time import sleep
import json
import psutil
import configparser

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

def isGameStillOpen(gameProcessName):
    for proc in psutil.process_iter():
        if proc.name() == gameProcessName:
            return True
    return False

config = configparser.ConfigParser()
config.optionxform = str
config.read('config.ini')

gamesPath = config['DEFAULT']['GamesPath']
openingScanInterval = int(config['DEFAULT']['OpeningScanInterval'])
closingScanInterval = int(config['DEFAULT']['ClosingScanInterval'])

# SCAN FOR GAME LOOP, break if game found
with open('gamesExeNames.json', 'r') as file:
    gamesDict = json.load(file)

gamesProcessList = list(gamesDict.keys())

print('Waiting for game...')
while True:
    gameProcessName = scanForGame(gamesProcessList)

    if gameProcessName:
        gameFullName = gamesDict[gameProcessName]
        print(f'GAME FOUND! -> {gameFullName}')
        print('Tracking...')
        break

    sleep(openingScanInterval)


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


while True:
    gameStillOpen = isGameStillOpen(gameProcessName)

    if not gameStillOpen:
        print('Game closed, logging session.')
        break

    sleep(closingScanInterval)


atexit.register(saveSession)