# import psutil

# for proc in psutil.process_iter():
#     if proc.name() != 'CalculatorApp.exe':
#         continue
#     print('da')
#     break
    

# import configparser

# config = configparser.ConfigParser()
# config.optionxform = str
# config.read('config.ini')

# for key in config['DEFAULT']:
#     print(key, config['DEFAULT'][key])

# import json

# def scanForGame(gamesProcessList):
#     for i in ['sekiro.exe']:
#         if i in gamesProcessList:
#             return i


# with open('gamesExeNames.json', 'r') as file:
#     games = json.load(file)

# gamesProcessList = list(games.keys())

# while True:
#     game = scanForGame(gamesProcessList)

#     if game:
#         gameName = games[game]
#         break

# print(gameName)

# import os 

# gp =  os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Games')

# print(gp)

from PyQt6 import QtGui, QtCore, QtWidgets
from PyQt6.QtWidgets import *

import sys



if __name__ == '__main__':

    app = QApplication(sys.argv)


    listWidget = QListWidget()
    listWidget.show()

    ls = ['test', 'test2', 'test3']

    listWidget.addItem('test')
    listWidget.addItem('test2')
    listWidget.addItem('test3')

    listWidget.addItems(ls)

    app.exec()