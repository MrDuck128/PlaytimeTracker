import os
import sys
from datetime import datetime, timedelta
from time import sleep
import json
import psutil
import configparser
from natsort import natsorted
from quickPlaytimeCounter import loadGameData, reloadSessionPlaytimes, formatSeconds, formatTime

GAME_DATA_FILE = 'gameData.json'

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


def saveSession(gameName, sT, start):
    eT = datetime.now().replace(microsecond=0)
    end = eT.strftime("%d-%m-%Y %H:%M:%S")
    differenceSeconds = (eT - sT).total_seconds()

    gameData = loadGameData()

    if not gameData:
        gameData = {}

    if gameName not in gameData:
        gameData[gameName] = {
            'playtime': "00:00:00",
            'completed': False,
            'lastPlayed': '01-01-2001 01:01:01',
            'sessions': []
        }

    # FORMAT DIFFERENCE
    difference = formatSeconds(differenceSeconds)
    
    # TOTAL PLAYTIME + CURRENT SESSION PLAYTIME
    playtimeSeconds = formatTime(gameData[gameName]['playtime'])
    gameData[gameName]['playtime'] = formatSeconds(playtimeSeconds + differenceSeconds)
    gameData[gameName]['lastPlayed'] = end
    gameData[gameName]['sessions'].append({
        'start': start,
        'end': end,
        'difference': difference
    })



    with open(GAME_DATA_FILE, 'w', encoding='utf-8') as f:
        f.write(json.dumps(gameData, indent=4))

    return difference


# MAKE DEFAULT CONFIG IF ONE DOESN'T EXIST
if not os.path.isfile('config.ini'):
    with open('config.ini', 'w') as configFile:
        configFile.write('[DEFAULT]')
        configFile.write('\nGamesPath = Default')
        configFile.write('\nOpeningScanInterval = 2')
        configFile.write('\nClosingScanInterval = 20')
        configFile.write('\nCurrentPlaytimeUpdateInterval = 600')
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
currentPlaytimeUpdateInterval = int(config['DEFAULT']['CurrentPlaytimeUpdateInterval'])
gameExeNames = config['DEFAULT']['GameExeNames']


# SCAN FOR GAME LOOP, break if game found
with open(gameExeNames, 'r') as file:
    gamesDict = json.load(file)

gamesProcessList = list(gamesDict.keys())

print('Waiting for game...')
while True:
    gameProcessName = scanForGame(gamesProcessList)

    if gameProcessName:
        gameName = gamesDict[gameProcessName]
        print(f'GAME FOUND! -> {gameName} ({gameProcessName})')
        break

    sleep(openingScanInterval)

sT = datetime.now().replace(microsecond=0)
start = sT.strftime("%d-%m-%Y %H:%M:%S")


# # CREATE DATA FILE IF IT DOESN'T EXIST
# if not os.path.isfile('gameData.json'):
#     with open(GAME_DATA_FILE, 'w', encoding='utf-8') as f:
#         f.write({})
#     print('Created game data file.')

# CHECK IF GAME IS OPEN, IF NOT SAVE SESSION
currentPlaytime = 0
while True:
    gameStillOpen = isGameStillOpen(gameProcessName)

    if not gameStillOpen:
        print('Game closed, logging session.')
        playtime = saveSession(gameName, sT, start)
        break

    if currentPlaytime % currentPlaytimeUpdateInterval == 0:
        playtime = formatSeconds(currentPlaytime)
        print(f'Tracking...       {playtime}', end='\r', flush=True)

    currentPlaytime += closingScanInterval
    sleep(closingScanInterval)

print(f'Played for {playtime}')
input('Press enter to exit...')