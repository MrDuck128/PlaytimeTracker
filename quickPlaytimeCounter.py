import os
import json
from datetime import timedelta


def loadPlaytimes():
    playtimes = []
    for dir in os.listdir('Games'):
        path = os.path.join('Games', dir, '0.txt')

        if os.path.isfile(path):
            with open(path, 'r') as f:
                playtime = f.read()
            playtimes.append((dir, playtime))
        else:
            playtimes.append((dir, 0))
    return playtimes


def reloadSessionPlaytimes():
    for dir in os.listdir('Games'):
        localPath = os.path.join('Games', dir)
        totalPath = os.path.join(localPath, '0.txt')
        totalPlaytime = timedelta()
        start = 1 if os.path.isfile(totalPath) else 0

        for session in os.listdir(localPath)[start:]:
            with open(os.path.join(localPath, session)) as sessionFile:
                info = json.load(sessionFile)
                (h, m, s) = (int(x) for x in info['difference'].split(':'))
                totalPlaytime += timedelta(hours=h, minutes=m, seconds=s)

        if not start:
            with open(totalPath, 'w') as file:
                file.write(str(totalPlaytime))

        with open(totalPath, 'r') as f:
            oldPlaytime = f.read()
        if oldPlaytime != str(totalPlaytime):
            if input('Outputs not the same, do you want to override old time? (y/n)') == 'y':
                with open(totalPath, 'w') as f:
                    f.write(str(totalPlaytime))

if __name__ == '__main__':
    loadPlaytimes()