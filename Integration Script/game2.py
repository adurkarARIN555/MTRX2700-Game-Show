# Importing relevant modules
from PyQt5 import QtCore as qtc
from PyQt5.QtWidgets import QPushButton, QWidget, QLabel

# Defining constants to remove magic numbers
text_label_x_offset = 50
text_label_y_offset = 50
text_label_width = 20000
text_label_height = 30
button_x_offset = 150
button_width = 100
button_height = 30

# Window for game two
class AnotherWindow(QWidget):
    # This "window" is a QWidget. If it has no parent, it will appear as a free-floating window as we want
    # Ensures that the synchronicity with other windows of the integration
    submitted = qtc.pyqtSignal(str)

    def __init__(self, argument, width, height):
        super().__init__()

        # Splits up the players
        players = argument.split("               ")

        # Creates a label for start and elimination text
        self.label = QLabel("Start catapult game \n\r Player eliminated:", self)
        self.label.setGeometry(text_label_x_offset, text_label_y_offset, text_label_width, text_label_height)

        buttons = []
        button_index = 0
        ypos = 10

        # Assigns each player a button 
        for player in players:
            buttons.append(QPushButton(player, self))
            
            buttons[button_index].setGeometry(button_x_offset, ypos, button_width, button_height)
            buttons[button_index].clicked.connect(lambda state, x = player: self.button_pressed(x))
            
            button_index += 1
            ypos += 30
            
    # Eliminates the player if their button is pressed
    def button_pressed(self,player):
        self.submitted.emit(player)
        self.close()
