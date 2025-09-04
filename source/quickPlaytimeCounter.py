import os
import json
from datetime import timedelta, datetime
from natsort import natsorted
import glob

GAME_DATA_FILE = 'gameData.json'

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

        playtime = playtime.total_seconds()
        newGameData[game]['playtime'] = f'{int(playtime//3600):02d}:{int(playtime%3600//60)}:{int(playtime%60)}'
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