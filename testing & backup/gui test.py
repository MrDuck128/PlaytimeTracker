from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import sys
from quickPlaytimeCounter import loadPlaytimes, reloadSessionPlaytimes
from random import choice

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GUI with Sections")
        self.setup_sections()

    def setup_sections(self):
        # Create the main widget and set it as the central widget
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        # Create a vertical layout to organize the sections
        layout = QVBoxLayout(main_widget)

        # Add sections to the layout
        self.add_section(layout, "Section 1", ["Widget 1", "Widget 2"])
        self.add_section(layout, "Section 2", ["Widget 3", "Widget 4"])

        # Set the layout for the main widget
        main_widget.setLayout(layout)

    def add_section(self, layout, title, widgets):
        # Create a section label
        section_label = QLabel(title)
        layout.addWidget(section_label)

        # Create the section widget and layout
        section_widget = QWidget()
        section_layout = QVBoxLayout(section_widget)

        # Add widgets to the section layout
        for widget in widgets:
            section_layout.addWidget(QLabel(widget))

        # Add the section widget to the main layout
        layout.addWidget(section_widget)




app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()