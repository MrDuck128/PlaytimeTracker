import typing
from PyQt6 import QtCore
from PyQt6.QtGui import QIcon, QFont, QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QListWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, QListWidgetItem, QPushButton, QStyledItemDelegate, QCheckBox
from PyQt6.QtCore import Qt, QCoreApplication
import sys, os
from quickPlaytimeCounter import loadPlaytimes, reloadSessionPlaytimes, loadSessions
import ctypes

myappid = 'playtimeTracker'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

class MainWindow(QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(900, 400, 800, 600)
        self.setMinimumSize(500, 350)
        self.setWindowTitle("Playtime Tracker")
        self.setWindowIcon(QIcon('palm.ico'))

        mainWidget = QWidget(self)
        self.setCentralWidget(mainWidget)

        layout = QVBoxLayout(mainWidget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.header(layout)
        self.main(layout)
        self.footer(layout)

    def header(self, layout):
        header = QWidget(self)
        header.setStyleSheet('background-color: rgb(117,193,240);')

        headerLayout = QVBoxLayout(header)

        # title in header
        titleFont = QFont()
        titleFont.setFamily("Unispace")
        titleFont.setPointSize(36)

        title = QLabel("Playtime Tracker")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(titleFont)
        title.setFixedHeight(80)
        title.setStyleSheet("""
                                color: rgb(255, 0, 0);
                            """)

        headerLayout.addWidget(title)

        # search layout below title (label and search box)
        searchLayout = QHBoxLayout()

        searchLabel = QLabel('Search:')
        searchLabel.setStyleSheet("""
                                font-weight: bold;
                                font-size: 15px;
                             """)
        searchLayout.addWidget(searchLabel, 0)

        self.search = QLineEdit()
        self.search.setStyleSheet("""
                                font-size: 15px; 
                                height: 25px;
                                padding: 5px;
                                background-color: white;
                            """)
        self.search.textChanged.connect(self.filterItems)
        searchLayout.addWidget(self.search)

        searchLabel = QLabel('Sort:')
        searchLabel.setStyleSheet("""
                                margin-left: 10px;
                                font-weight: bold;
                                font-size: 15px;
                             """)
        searchLayout.addWidget(searchLabel, 0)

        self.sortButton = QPushButton("Playtime", self)
        self.sortButton.setFixedSize(130, 37)
        self.sortButton.setCheckable(True)
        self.sortButton.clicked.connect(self.changeSort)
        searchLayout.addWidget(self.sortButton, 0)

        buttonStyle = """
            QPushButton {
                height: 25px;
                background-color: white;
                font-weight: bold;
                font-size: 15px;
                border: 1px solid;
            }"""
        self.sortButton.setStyleSheet(buttonStyle)

        headerLayout.addLayout(searchLayout)

        layout.addWidget(header)

    def filterItems(self, searchText):
        searchText = searchText.lower()
        for i in range(self.listWidget.count()):
            listWidgetItem = self.listWidget.item(i)
            item = self.listWidget.itemWidget(listWidgetItem)
            # each item has 3 labels, (pic, game, playtime)
            gameName = item.findChildren(QLabel)[1].text().lower()
            if searchText in gameName:
                listWidgetItem.setHidden(False)
            else:
                listWidgetItem.setHidden(True)

    def changeSort(self):

        def iterAllItems():
            for i in range(self.listWidget.count()):
                yield self.listWidget.item(i)

        tempItemList = []

        for listWidgetItem in iterAllItems():
            item = self.listWidget.itemWidget(listWidgetItem)
            h, m, s = item.playtime.split(':')
            playtimeSeconds = h*3600 + m*60 + s
            tempItemList.append((item.gameName, item.playtime, playtimeSeconds, item.completed, item.isHidden()))


        if self.sortButton.isChecked():
            self.sortButton.setText('Name')

            self.listWidget.clear()
            for (game, playtime, _, completed, hidden) in sorted(tempItemList, key=lambda x: x[2], reverse=True):
                item = QListWidgetItem()
                itemWidget = StyledListItemWidget(game, playtime, completed)
                self.listWidget.addItem(item)
                self.listWidget.setItemWidget(item, itemWidget)
                item.setHidden(hidden)

        else:
            self.sortButton.setText('Playtime')

            self.listWidget.clear()
            for (game, playtime, _, completed, hidden) in sorted(tempItemList, key=lambda x: x[0]):
                item = QListWidgetItem()
                itemWidget = StyledListItemWidget(game, playtime, completed)
                self.listWidget.addItem(item)
                self.listWidget.setItemWidget(item, itemWidget)
                item.setHidden(hidden)

    def main(self, layout):
        self.listWidget = QListWidget()
        self.listWidget.setSpacing(0)
        # listWidget.setGeometry(0, 80, 1000, 450)
        # self.listWidget.setSortingEnabled(True)
        self.listWidget.show()
        
        delegate = CustomDelegate(self.listWidget)
        self.listWidget.setItemDelegate(delegate)
        self.listWidget.itemDoubleClicked.connect(self.launchSessionPreview)

        self.reloadData()

        self.listWidget.setStyleSheet("""
            QListWidget {
                padding: 0px;
            }
            QListWidget::item {
                margin: 7px;
                background-color: rgb(220,220,220);
            }
        """)

        self.listWidget.sortItems(QtCore.Qt.SortOrder.DescendingOrder)

        layout.addWidget(self.listWidget)

    def launchSessionPreview(self, item):
        item = self.listWidget.itemWidget(item).findChildren(QLabel)[1].text()
        sessionPreview = SessionPreview(item, self)
        sessionPreview.show()

    def footer(self, layout):
        footerLayout = QGridLayout()
        footerLayout.setRowMinimumHeight(0, 50)

        quitButton = QPushButton("Quit", self)
        quitButton.setFixedSize(130, 40)
        quitButton.clicked.connect(self.closeApp)
        footerLayout.addWidget(quitButton, 0, 0)

        # spacer = QSpacerItem(1, 1)
        # footerLayout.addItem(spacer, 0, 1, 1, 2)

        reloadButton = QPushButton("Reload times", self)
        reloadButton.setFixedSize(130, 40)
        reloadButton.clicked.connect(self.reloadData)
        footerLayout.addWidget(reloadButton, 0, 2)

        buttonStyle = """
            QPushButton {
                background-color: white;
                font-weight: bold;
                border: 1px solid;
            }"""
        quitButton.setStyleSheet(buttonStyle)
        reloadButton.setStyleSheet(buttonStyle)

        layout.addLayout(footerLayout)

    def closeApp(self):
        QCoreApplication.instance().quit()

    # depricated
    # def restart(self):
    #     QCoreApplication.quit()
    #     status = QProcess.startDetached(sys.executable, sys.argv)

    def reloadData(self):
        # reload and check if no games
        if not reloadSessionPlaytimes():
            return

        self.listWidget.clear()
        self.search.clear()
        for (game, playtime, completed) in loadPlaytimes():
            item = QListWidgetItem()
            itemWidget = StyledListItemWidget(game, playtime, completed)
            self.listWidget.addItem(item)
            self.listWidget.setItemWidget(item, itemWidget)

        self.sortButton.setText('Playtime')
        self.sortButton.setChecked(False)
    

# Styled list item height for main window list display
class CustomDelegate(QStyledItemDelegate):
    def sizeHint(self, option, index):
        size = super().sizeHint(option, index)
        size.setHeight(128)  # Set the desired row height
        return size

# Styled list item height for session preview window list display
class CustomDelegate2(QStyledItemDelegate):
    def sizeHint(self, option, index):
        size = super().sizeHint(option, index)
        size.setHeight(64)  # Set the desired row height
        return size
    
# StyledListItemWidget for main window list display
class StyledListItemWidget(QWidget):
    def __init__(self, game, playtime, completed, parent=None):
        super().__init__(parent)

        self.gameName = game
        self.playtime = playtime
        self.completed = completed

        row = QHBoxLayout(self)
        row.setContentsMargins(0, 0, 0, 0)

        if os.path.isfile('GameIcons/' + game + '.png'):
            picName = game + '.png'
        else:
            picName = 'default.png'

        pic = QLabel(self)
        pic.setPixmap(QPixmap('./GameIcons/' + picName).scaled(128, 128, Qt.AspectRatioMode.KeepAspectRatio))
        pic.show()

        row.addWidget(pic)

        label1 = QLabel(game)
        label1.setStyleSheet("""
                                padding: 7px;
                                font-weight: bold;
                                font-size: 14pt;
                             """)
        row.addWidget(label1, 3)

        self.label2 = QLabel(playtime)
        self.changeLabelColor(completed)
        row.addWidget(self.label2, 1)

        checkbox = QCheckBox(self)
        checkbox.setChecked(completed)
        checkbox.stateChanged.connect(lambda completed: self.changeCompleted(game, playtime, checkbox.isChecked())) # TODO lambda?
        row.addWidget(checkbox, 1)

    def changeCompleted(self, game, playtime, completed):
        with open(os.path.join('Games', game, '0.txt'), 'w') as f:
            f.write(playtime)
            f.write('\n' + str(int(completed)))
        self.changeLabelColor(completed)
        
    def changeLabelColor(self, completed):
        if completed:
            self.label2.setStyleSheet("""
                                    padding: 7px;
                                    color: green;
                                    font-weight: bold;
                                    font-size: 14pt;
                                """)
        else:
            self.label2.setStyleSheet("""
                                    padding: 7px;
                                    color: red;
                                    font-weight: bold;
                                    font-size: 14pt;
                                """)

# StyledListItemWidget for session preview window list display
class StyledListItemWidget2(QWidget):
    def __init__(self, i, startDate, startTime, endDate, endTime, playtime, parent=None):
        super().__init__(parent)

        row = QHBoxLayout(self)
        row.setContentsMargins(0, 0, 0, 0)

        self.label1 = QLabel(i)
        self.label1.setStyleSheet("""
                                padding: 7px;
                                font-weight: bold;
                                font-size: 14pt;
                             """)
        row.addWidget(self.label1, 1)

        self.labelStart = QLabel("Start:")
        row.addWidget(self.labelStart, 1)

        self.label2 = QLabel(startDate)
        self.label2.setStyleSheet("""
                                font-size: 12pt;
                                font-weight: bold;
                             """)
        row.addWidget(self.label2, 2)

        self.label3 = QLabel(startTime)
        self.label3.setStyleSheet("""
                                font-size: 12pt;
                                font-weight: bold;
                             """)
        row.addWidget(self.label3, 2)

        self.labelEnd = QLabel("End:")
        row.addWidget(self.labelEnd, 1)

        self.label4 = QLabel(endDate)
        self.label4.setStyleSheet("""
                                font-size: 12pt;
                                font-weight: bold;
                             """)
        row.addWidget(self.label4, 2)

        self.label5 = QLabel(endTime)
        self.label5.setStyleSheet("""
                                font-size: 12pt;
                                font-weight: bold;
                             """)
        row.addWidget(self.label5, 2)

        self.label6 = QLabel(playtime)
        self.label6.setStyleSheet("""
                                padding: 7px;
                                font-weight: bold;
                                font-size: 14pt;
                                color: red;
                             """)
        row.addWidget(self.label6, 2)


class SessionPreview(QMainWindow):
    def __init__(self, gameName, parent):
        super().__init__(parent)
        self.resize(800, 600)
        self.setWindowTitle(f"Session Preview - {gameName}")
        self.setWindowIcon(QIcon('palm.ico'))

        mainWidget = QWidget(self)
        self.setCentralWidget(mainWidget)

        layout = QVBoxLayout(mainWidget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.header(layout, gameName)
        self.main(layout, gameName)
        # self.footer(layout)

    def header(self, layout, gameName):
        header = QWidget(self)
        header.setStyleSheet('background-color: rgb(117,193,240);')

        headerLayout = QVBoxLayout(header)

        # title in header
        titleFont = QFont()
        titleFont.setFamily("Unispace")
        titleFont.setPointSize(36)

        title = QLabel(gameName)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(titleFont)
        title.setFixedHeight(80)
        title.setStyleSheet("""
                                color: rgb(255, 0, 0);
                            """)

        headerLayout.addWidget(title)

        layout.addWidget(header)

    def main(self, layout, gameName):
        self.listWidget = QListWidget()
        self.listWidget.setSpacing(0)
        # listWidget.setGeometry(0, 80, 1000, 450)
        self.listWidget.show()
        
        delegate = CustomDelegate2(self.listWidget)
        self.listWidget.setItemDelegate(delegate)

        self.displaySessions(gameName)

        self.listWidget.setStyleSheet("""
            QListWidget {
                padding: 0px;
            }
            QListWidget::item {
                margin: 3px;
                background-color: rgb(220,220,220);
            }
        """)

        layout.addWidget(self.listWidget)

    def displaySessions(self, gameName):
        sessions = loadSessions(gameName)

        self.listWidget.clear()
        for i, session in enumerate(sessions):
            i = str(i+1)
            startDate = str(session["startDate"])
            startTime = str(session["startTime"])
            endDate = str(session["endDate"])
            endTime = str(session["endTime"])
            playtime = str(session["difference"])

            self.item = QListWidgetItem()
            self.itemWidget = StyledListItemWidget2(i, startDate, startTime, endDate, endTime, playtime)
            self.listWidget.addItem(self.item)
            self.listWidget.setItemWidget(self.item, self.itemWidget)



app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()