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

        listWidget = QListWidget()
        listWidget.setSpacing(0)
        # listWidget.setGeometry(0, 80, 1000, 450)
        listWidget.show()
        
        delegate = CustomDelegate(listWidget)
        listWidget.setItemDelegate(delegate)
            
        for (game, playtime) in loadPlaytimes():
            item = QListWidgetItem()
            itemWidget = StyledListItemWidget(game, playtime)
            listWidget.addItem(item)
            listWidget.setItemWidget(item, itemWidget)

        listWidget.setStyleSheet("""
            QListWidget {
                padding: 0px;
            }
            QListWidget::item {
                margin: 7px;
                background-color: rgb(220,220,220);
            }
        """)

        layout.addWidget(listWidget)

    def footer(self, layout):
        footerLayout = QGridLayout()
        footerLayout.setRowMinimumHeight(0, 50)

        quitButton = QPushButton("Quit", self)
        quitButton.setFixedSize(130, 40)
        quitButton.clicked.connect(self.closeApp)
        footerLayout.addWidget(quitButton, 0, 0)

        reloadButton = QPushButton("Reload times", self)
        reloadButton.setFixedSize(130, 40)
        reloadButton.clicked.connect(self.reloadData)
        footerLayout.addWidget(reloadButton, 0, 6)

        buttonStyle = """
            QPushButton {
                background-color: rgb(176, 220, 247);
                font-weight: bold;
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
        self.restart()
    

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