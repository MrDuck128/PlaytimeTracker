import os
from datetime import datetime
from time import sleep
import json
import psutil
import configparser
from natsort import natsorted

def scanForGame(gamesList):
    for proc in psutil.process_iter():
        if proc.name() in gamesList:
            return proc.name()
    return False

def isGameStillOpen(gameProcessName):
    for proc in psutil.process_iter():
        if proc.name() == gameProcessName:
            return True
    return False

def saveSession():
    # ADD NEW FILE AFTER LAST INDEX OR START AT 1 IF NONE EXIST
    if not os.listdir(path):
        newSessionIndex = str(1)
    else:
        lastSessionIndex = int(natsorted(os.listdir(path))[-1].replace('.json', ''))
        newSessionIndex = str(lastSessionIndex + 1)

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

    return difference


if not os.path.isfile('config.ini'):
    with open('config.ini', 'w') as configFile:
        configFile.write('[DEFAULT]')
        configFile.write('\nGamesPath = Default')
        configFile.write('\nOpeningScanInterval = 5')
        configFile.write('\nClosingScanInterval = 20')
        configFile.write('\nGameExeNames = gamesExeNames.json')

config = configparser.ConfigParser()
config.optionxform = str
config.read('config.ini')

# C:\Programski-kod\Playtime Tracker\Games
gamesPath = config['DEFAULT']['GamesPath']
if gamesPath == 'Default':
    gamesPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Games')
openingScanInterval = int(config['DEFAULT']['OpeningScanInterval'])
closingScanInterval = int(config['DEFAULT']['ClosingScanInterval'])
gameExeNames = config['DEFAULT']['GameExeNames']

# SCAN FOR GAME LOOP, break if game found
with open(gameExeNames, 'r') as file:
    gamesDict = json.load(file)

gamesProcessList = list(gamesDict.keys())

print('Waiting for game...')
while True:
    gameProcessName = scanForGame(gamesProcessList)

    if gameProcessName:
        gameFullName = gamesDict[gameProcessName]
        print(f'GAME FOUND! -> {gameFullName} ({gameProcessName})')
        print('Tracking...')
        break

    sleep(openingScanInterval)

sT = datetime.now().replace(microsecond=0)
startDate = sT.strftime("%d-%m-%Y")
startTime = sT.strftime("%H:%M:%S")


# CREATE FOLEDR IF NOT EXISTS
path = os.path.join(gamesPath, gameFullName)

if not os.path.isdir(path):
    os.makedirs(path)

# CHECK IF GAME IS OPEN, IF NOT SAVE SESSION
while True:
    gameStillOpen = isGameStillOpen(gameProcessName)

    if not gameStillOpen:
        print('Game closed, logging session.')
        playtime = saveSession()
        break

    sleep(closingScanInterval)

print(f'Played for {playtime}')
input('Press enter to exit...')