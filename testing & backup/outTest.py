from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

class SearchableListWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.listWidget = QListWidget()
        self.searchLineEdit = QLineEdit()
        self.searchLineEdit.textChanged.connect(self.filterListItems)

        layout = QVBoxLayout()
        layout.addWidget(self.searchLineEdit)
        layout.addWidget(self.listWidget)
        self.setLayout(layout)

        self.populateList()

    def populateList(self):
        items = ["Apple", "Banana", "Orange", "Grapes", "Mango"]
        self.listWidget.addItems(items)

    def filterListItems(self, search_text):
        items = self.listWidget.findItems(search_text, Qt.MatchFlag.MatchContains)
        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            if item in items:
                item.setHidden(False)
            else:
                item.setHidden(True)

if __name__ == "__main__":
    app = QApplication([])
    window = SearchableListWidget()
    window.show()
    app.exec()