from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import sys, os
from quickPlaytimeCounter import loadPlaytimes, reloadSessionPlaytimes

class MainWindow(QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(900, 400, 800, 600)
        self.setMinimumSize(500, 350)
        self.setWindowTitle("Playtime Tracker")
        self.setWindowIcon(QIcon('logo.ico'))

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

    def main(self, layout):

        self.listWidget = QListWidget()
        self.listWidget.setSpacing(0)
        # listWidget.setGeometry(0, 80, 1000, 450)
        self.listWidget.show()
        
        delegate = CustomDelegate(self.listWidget)
        self.listWidget.setItemDelegate(delegate)

        self.reloadData()
        
        # for (game, playtime) in loadPlaytimes():    # KAKA
        #     item = QListWidgetItem()
        #     itemWidget = StyledListItemWidget(game, playtime)
        #     self.listWidget.addItem(item)
        #     self.listWidget.setItemWidget(item, itemWidget)

        self.listWidget.setStyleSheet("""
            QListWidget {
                padding: 0px;
            }
            QListWidget::item {
                margin: 7px;
                background-color: rgb(220,220,220);
            }
        """)

        layout.addWidget(self.listWidget)


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

    def restart(self):
        QCoreApplication.quit()
        status = QProcess.startDetached(sys.executable, sys.argv)

    def reloadData(self):
        reloadSessionPlaytimes()
        
        self.listWidget.clear()
        self.search.clear()
        for (game, playtime) in loadPlaytimes():
            item = QListWidgetItem()
            itemWidget = StyledListItemWidget(game, playtime)
            self.listWidget.addItem(item)
            self.listWidget.setItemWidget(item, itemWidget)
    

class CustomDelegate(QStyledItemDelegate):
    def sizeHint(self, option, index):
        size = super().sizeHint(option, index)
        size.setHeight(128)  # Set the desired row height
        return size
    
class StyledListItemWidget(QWidget):
    def __init__(self, game, playtime, parent=None):
        super().__init__(parent)

        row = QHBoxLayout(self)
        row.setContentsMargins(0, 0, 0, 0)

        if os.path.isfile('GameIcons/' + game + '.png'):
            picName = game
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
        row.addWidget(label1, 2)

        label2 = QLabel(playtime)
        label2.setStyleSheet("""
                                padding: 7px;
                                color: red;
                                font-weight: bold;
                                font-size: 14pt;
                            """)
        row.addWidget(label2, 1)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()