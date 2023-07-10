import os
import sys
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
    if not os.listdir(path) or len(os.listdir(path)) == 1 and os.path.isfile(os.path.join(path, '0.txt')):
        newSessionIndex = str(1)
    else:
        lastSessionIndex = int(natsorted(os.listdir(path))[-1].replace('.json', ''))
        newSessionIndex = str(lastSessionIndex + 1)

    eT = datetime.now().replace(microsecond=0)
    endDate = eT.strftime("%d-%m-%Y")
    endTime = eT.strftime("%H:%M:%S")
    differenceSeconds = (eT - sT).total_seconds()

    # FORMAT DIFFERENCE
    hours = int(differenceSeconds / 3600)
    minutes = int(differenceSeconds % 3600 / 60)
    seconds = int((differenceSeconds % 3600) % 60)
    difference = f'{hours:02d}:{minutes:02d}:{seconds:02d}'

    data = {
        "startDate": startDate,
        "startTime": startTime,
        "endDate": endDate,
        "endTime": endTime,
        "difference": str(difference)
    }
    print(f'Saving to: "{path}" as "{newSessionIndex+".json"}"')
    with open(os.path.join(path, newSessionIndex+".json"), 'w') as file:
        file.write(json.dumps(data, indent=4))

    return difference


# MAKE DEFAULT CONFIG IF ONE DOESN'T EXIST
if not os.path.isfile('config.ini'):
    with open('config.ini', 'w') as configFile:
        configFile.write('[DEFAULT]')
        configFile.write('\nGamesPath = Default')
        configFile.write('\nOpeningScanInterval = 2')
        configFile.write('\nClosingScanInterval = 20')
        configFile.write('\nGameExeNames = gamesExeNames.json')

# READ CONFIG FILE
config = configparser.ConfigParser()
config.optionxform = str
config.read('config.ini')

# C:\Programski-kod\Playtime Tracker\Games
gamesPath = config['DEFAULT']['GamesPath']
if gamesPath == 'Default' or not os.path.isdir(gamesPath):
    gamesPath = os.path.join(os.path.dirname(sys.argv[0]), 'Games') # TODO
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