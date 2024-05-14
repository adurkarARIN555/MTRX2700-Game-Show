from PyQt5 import QtCore as qtc
from PyQt5.QtWidgets import QPushButton, QWidget, QLabel

class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """

    submitted = qtc.pyqtSignal(str)

    def __init__(self, argument):
        super().__init__()
        players = argument.split("               ")

        self.label = QLabel("Start catapult game \n\r Player eliminated:", self)
        self.label.setGeometry(50, 50, 2000, 30)

        buttons = []
        button_index = 0
        ypos = 10

        for player in players:

            buttons.append(QPushButton(player, self))
            buttons[button_index].setGeometry(150, ypos, 100, 30)
            buttons[button_index].clicked.connect(lambda state, x = player: self.button_pressed(x))
            button_index += 1
            ypos += 30
            

    def button_pressed(self,player):
        self.submitted.emit(player)
        self.close()