from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import sys
from quickPlaytimeCounter import loadPlaytimes
from random import choice

class MainWindow(QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(900, 400, 600, 400)
        self.setWindowTitle("Playtime Tracker")
        self.main()

    def main(self):
        self.label = QLabel("Super!")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(self.label)

        quitButton = QPushButton("Quit", self)
        quitButton.move(50, 50)
        quitButton.clicked.connect(self.closeApp)

        loadButton = QPushButton("Load", self)
        loadButton.move(300, 300)
        loadButton.clicked.connect(self.loadData)

        labelButton = QPushButton("Change label", self)
        labelButton.move(400, 50)
        labelButton.clicked.connect(self.changeLabel)

        listButton = QPushButton("Show list", self)
        listButton.move(400, 100)
        listButton.clicked.connect(self.listTest)

    def closeApp(self):
        QCoreApplication.instance().quit()

    def changeLabel(self):
        labels = ['jedan', 'dva', 'tri', 'kiticaa', 'Promjenaaa..!']
        novi = choice(labels)
        self.label.setText(novi)

    def loadData(self):
        playtimes = loadPlaytimes()
        self.label.setText(str(playtimes))

    def listTest(self):
        listWidget = QListWidget(self)
        listWidget.setGeometry(100, 100, 100, 100)
        listWidget.show()

        ls = ['test', 'test2', 'test3']

        listWidget.addItem('test')
        listWidget.addItem('test2')
        listWidget.addItem('test3')

        listWidget.addItems(ls)
        




app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()