import json

with open('gamesExeNames.json', 'r') as file:
    data = dict(json.load(file))

data = dict(sorted(data.items()))

with open('gamesExeNames.json', 'w') as file:
    json.dump(data, file, indent=4)