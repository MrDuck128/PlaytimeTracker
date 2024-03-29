import os
import json
from datetime import timedelta
from natsort import natsorted

def loadPlaytimes():
    playtimes = []
    for dir in os.listdir('Games'):
        path = os.path.join('Games', dir, '0.txt')

        if os.path.isfile(path):
            with open(path, 'r') as f:
                playtime, completed = f.read().splitlines()
            playtimes.append((dir, playtime, int(completed)))
        else:
            playtimes.append((dir, 0, False))
    return playtimes

def reloadSessionPlaytimes():
    if not os.path.isdir('Games'):
        return 0
    for dir in os.listdir('Games'):
        localPath = os.path.join('Games', dir)
        totalPath = os.path.join(localPath, '0.txt')
        totalPlaytime = timedelta()
        start = 1 if os.path.isfile(totalPath) else 0

        for session in os.listdir(localPath)[start:]:
            try:
                with open(os.path.join(localPath, session)) as sessionFile:
                    info = json.load(sessionFile)
                    (h, m, s) = (int(x) for x in info['difference'].split(':'))
                    totalPlaytime += timedelta(hours=h, minutes=m, seconds=s)
            except:
                raise ValueError(f'Something went wrong with processing "{dir}/{session}" data.')

        # FORMAT TOTAL PLAYTIME
        totalPlaytime = totalPlaytime.total_seconds()
        hours = int(totalPlaytime / 3600)
        minutes = int(totalPlaytime % 3600 / 60)
        seconds = int((totalPlaytime % 3600) % 60)
        totalPlaytime = f'{hours:02d}:{minutes:02d}:{seconds:02d}'

        # IF "0.txt" FILE DOENS'T EXIST
        if not start:
            with open(totalPath, 'w') as file:
                file.write(totalPlaytime)
                file.write("\n0")
            return

        with open(totalPath, 'r') as f:
            oldPlaytime, completed = f.read().splitlines()
        if oldPlaytime != totalPlaytime:
            # if input('Outputs not the same, do you want to override old time? (y/n)') == 'y':
                with open(totalPath, 'w') as f:
                    f.write(totalPlaytime)
                    f.write('\n' + completed)
    return 1

def loadSessions(game):
    sessions = []
    for sessionFile in natsorted(os.listdir(os.path.join('Games', game))):
        if sessionFile[-4:] == 'json':
            path = os.path.join('Games', game, sessionFile)
            with open(path) as f:
                session = json.load(f)
                sessions.append(session)
    return sessions

if __name__ == '__main__':
    # print(loadPlaytimes())
    # reloadSessionPlaytimes()
    print(loadSessions('Outer Wilds'))