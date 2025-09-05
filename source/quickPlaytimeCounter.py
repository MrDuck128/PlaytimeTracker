import os
import json
from datetime import timedelta, datetime
from natsort import natsorted
import glob

GAME_DATA_FILE = 'gameData.json'

def formatSeconds(seconds: int) -> str:
    hours = int(seconds // 3600)
    minutes = int(seconds % 3600 // 60)
    seconds = int(seconds % 60)
    
    return f'{hours:02d}:{minutes:02d}:{seconds:02d}'

def formatTime(playtime: str) -> int:
    hours, minutes, seconds = map(int, playtime.split(':'))

    return hours*3600 + minutes*60 + seconds

def loadGameData() -> dict:
    '''
    Loads all game data from the game data file and returns it. 
    Structure:
    {
        Game name:
            playtime,
            completed,
            lastPlayed,
            sessions
    }
    '''

    # no data file
    if not os.path.isfile(GAME_DATA_FILE):
        return 0
    
    try:
        with open(GAME_DATA_FILE) as f:
            gameData = json.load(f)
        return gameData
    except Exception as e:
        print(e)

def reloadSessionPlaytimes(gameData=0):
    newGameData = loadGameData()

    for game, data in newGameData.items():
        # if 'completed' in data:
        #     del newGameData[game]['completed']

        playtime = timedelta()
        for session in data['sessions']:
            t = datetime.strptime(session['difference'], '%H:%M:%S')
            playtime += timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
        
        lastPlayed = data['sessions'][-1]['end']

        newGameData[game]['playtime'] = formatSeconds(playtime.total_seconds())
        newGameData[game]['lastPlayed'] = lastPlayed

    # return newGameData if no current data is loaded/available
    if not gameData:
        return newGameData
    
    # update all except "completed" status from app
    for game, changes in gameData.items():
        if game in newGameData:
            newGameData[game]['completed'] = changes['completed']
    return newGameData

def saveData(gameData):
    try:
        with open(GAME_DATA_FILE, 'w', encoding='utf-8') as f:
            f.write(json.dumps(gameData, indent=4))
    except Exception as e:
        print(e)
    
if __name__ == '__main__':
    # print(loadPlaytimes())
    # reloadSessionPlaytimes()
    print(loadGameData())