from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import sys
from quickPlaytimeCounter import loadPlaytimes, reloadSessionPlaytimes

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
        layout.setSpacing(10)


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

 

        listWidget = QListWidget()
        
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



        footer = QGridLayout()

        quitButton = QPushButton("Quit", self)
        # quitButton.move(50, 100)
        quitButton.clicked.connect(self.closeApp)
        footer.addWidget(quitButton, 1, 0, 1, 1)

        loadButton = QPushButton("Reload times", self)
        # loadButton.move(100, 100)
        loadButton.clicked.connect(self.reloadData)
        footer.addWidget(loadButton, 1, 2, 1, 1)

        layout.addLayout(footer)


    def closeApp(self):
        QCoreApplication.instance().quit()

    def reloadData(self):
        reloadSessionPlaytimes()
        self.createListWidget()
    

class CustomDelegate(QStyledItemDelegate):
    def sizeHint(self, option, index):
        size = super().sizeHint(option, index)
        size.setHeight(60)  # Set the desired row height
        return size
    
class StyledListItemWidget(QWidget):
    def __init__(self, text1, text2, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        label1 = QLabel(text1)
        label1.setStyleSheet("""
                                padding: 7px;
                                font-weight: bold;
                             """)
        layout.addWidget(label1)

        label2 = QLabel(text2)
        label2.setStyleSheet("""
                                padding: 7px;
                                color: red;
                                font-weight: bold;
                            """)
        layout.addWidget(label2)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()