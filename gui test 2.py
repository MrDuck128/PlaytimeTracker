from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import sys
from quickPlaytimeCounter import loadPlaytimes, reloadSessionPlaytimes
from random import choice

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

        # Helper function to add items with styled strings
        def add_styled_item(text1, text2):
            item = QWidget()
            item_layout = QHBoxLayout(item)
            item_layout.setContentsMargins(0, 0, 0, 0)

            label1 = QLabel(text1)
            label1.setStyleSheet("font-weight: bold;")
            item_layout.addWidget(label1)

            label2 = QLabel(text2)
            label2.setStyleSheet("color: red;")
            item_layout.addWidget(label2)

            list_widget.addItem("")
            list_widget.setItemWidget(list_widget.item(list_widget.count() - 1), item)

        # Add items with two strings
        add_styled_item("String1", "String2")
        add_styled_item("Hello", "World")
        add_styled_item("OpenAI", "GPT-3")

        layout.addWidget(list_widget)

        main_widget.setLayout(layout)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()