from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import sys
from quickPlaytimeCounter import loadPlaytimes, reloadSessionPlaytimes
from random import choice

class StyledListItemWidget(QWidget):
    def __init__(self, text1, text2, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        label1 = QLabel(text1)
        label1.setStyleSheet("font-weight: bold;")
        layout.addWidget(label1)

        label2 = QLabel(text2)
        label2.setStyleSheet("color: red;")
        layout.addWidget(label2)

class CustomDelegate(QStyledItemDelegate):
    def sizeHint(self, option, index):
        size = super().sizeHint(option, index)
        size.setHeight(60)  # Set the desired row height
        return size

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Styled List Widget")
        self.setup_ui()

    def setup_ui(self):
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout(main_widget)

        list_widget = QListWidget()

        delegate = CustomDelegate(list_widget)
        list_widget.setItemDelegate(delegate)

        # Add items with two strings
        item1 = QListWidgetItem()
        item_widget1 = StyledListItemWidget("String1", "String2")
        list_widget.addItem(item1)
        list_widget.setItemWidget(item1, item_widget1)

        item2 = QListWidgetItem()
        item_widget2 = StyledListItemWidget("Hello", "World")
        list_widget.addItem(item2)
        list_widget.setItemWidget(item2, item_widget2)

        item3 = QListWidgetItem()
        item_widget3 = StyledListItemWidget("OpenAI", "GPT-3")
        list_widget.addItem(item3)
        list_widget.setItemWidget(item3, item_widget3)

        layout.addWidget(list_widget)

        main_widget.setLayout(layout)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()