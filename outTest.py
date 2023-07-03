from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton

app = QApplication([])
window = QWidget()

layout = QVBoxLayout(window)

# Add your other widgets to the QVBoxLayout here

# Create a QGridLayout to hold the buttons
button_layout = QGridLayout()

# Create the left button
left_button = QPushButton("Left Button")
left_button.setFixedSize(100, 30)  # Set a fixed size for the button
button_layout.addWidget(left_button, 0, 0)  # Add the button to row 0, column 0

# Create the right button
right_button = QPushButton("Right Button")
right_button.setFixedSize(100, 30)  # Set a fixed size for the button
button_layout.addWidget(right_button, 0, 2)  # Add the button to row 0, column 2

# Add the button layout to the QVBoxLayout
layout.addLayout(button_layout)

window.show()
app.exec()