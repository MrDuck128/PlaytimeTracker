from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import sys
from quickPlaytimeCounter import loadPlaytimes, reloadSessionPlaytimes
from random import choice

class CustomDelegate(QStyledItemDelegate):
    def sizeHint(self, option, index):
        size = super().sizeHint(option, index)
        size.setHeight(40)  # Set the desired row height
        return size

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Customized List Widget")
        self.setup_ui()

    def setup_ui(self):
        main_widget = QListWidget(self)

        # Set a custom delegate to control the item size
        delegate = CustomDelegate(main_widget)
        main_widget.setItemDelegate(delegate)

        # Add items to the list widget
        main_widget.addItem("Item 1")
        main_widget.addItem("Item 2")
        main_widget.addItem("Item 3")

        self.setCentralWidget(main_widget)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()