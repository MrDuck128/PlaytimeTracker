from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import sys
from quickPlaytimeCounter import loadPlaytimes, reloadSessionPlaytimes
from random import choice

class MainWindow(QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(900, 400, 1000, 600)
        self.setWindowTitle("Playtime Tracker")
        self.setWindowIcon(QIcon('logo.ico'))

        mainWidget = QWidget(self)
        self.setCentralWidget(mainWidget)

        layout = QVBoxLayout(mainWidget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.header(layout)
        self.main(layout)

    def header(self, layout):
        titleFont = QFont()
        titleFont.setFamily("Calibri")
        titleFont.setPointSize(36)

        title = QLabel("Playtime Tracker")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(titleFont)
        title.setFixedHeight(80)
        title.setStyleSheet("""
            QLabel {
                color: rgb(255, 0, 0);
                background-color: rgb(117,193,240);
            }
        """)

        layout.addWidget(title)

    def main(self, layout):

        mainContainer = QWidget()
        mainContainer.setStyleSheet("""
            QWidget {
                background-color: rgb(220,220,220);
            }
        """)

        layout.addWidget(mainContainer)

        quitButton = QPushButton("Quit", self)
        quitButton.move(70, 550)
        quitButton.clicked.connect(self.closeApp)

        loadButton = QPushButton("Reload times", self)
        loadButton.move(830, 550)
        loadButton.clicked.connect(self.reloadData)

        self.createListWidget()

    def closeApp(self):
        QCoreApplication.instance().quit()

    def reloadData(self):
        reloadSessionPlaytimes()
        self.createListWidget()

    def createListWidget(self):
        listWidget = QListWidget(self)
        listWidget.setGeometry(0, 80, 1000, 450)
        listWidget.show()

        gamesAndPlaytimes = loadPlaytimes()

        def addGameItem(game, playtime, ):
            item = QWidget()
            item_layout = QHBoxLayout(item)
            item_layout.setContentsMargins(0, 0, 0, 0)

            label1 = QLabel(game)
            label1.setStyleSheet("font-weight: bold;")
            item_layout.addWidget(label1)

            label2 = QLabel(playtime)
            label2.setStyleSheet("color: red;")
            item_layout.addWidget(label2)

            listWidget.addItem("")
            listWidget.setItemWidget(listWidget.item(listWidget.count() - 1), item)

        for (game, playtime) in gamesAndPlaytimes:
            addGameItem(game, playtime)

        listWidget.setStyleSheet("""
            QListWidget {
                padding: 5px;
            }
            QListWidget::item {
                margin: 7px;
                background-color: rgb(220,220,220);
            }
        """)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()