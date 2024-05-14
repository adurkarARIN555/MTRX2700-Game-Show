from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QWidget
from PyQt5 import QtCore as qtc

import game3

import sys

from random import randint


class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """

    submitted = qtc.pyqtSignal(str)

    def __init__(self, argument):
        super().__init__()
        players = argument.split("               ")


        button1 = QPushButton(players[0], self)
        button1.setGeometry(100, 100, 100, 30)

        button2 = QPushButton(players[1], self)
        button2.setGeometry(100, 70, 100, 30)

        button3 = QPushButton(players[2], self)
        button3.setGeometry(100, 40, 100, 30)

        button4 = QPushButton(players[3], self)
        button4.setGeometry(100, 10, 100, 30)

        button1.clicked.connect(self.button1_pressed)
        button2.clicked.connect(self.button2_pressed)
        button3.clicked.connect(self.button3_pressed)
        button4.clicked.connect(self.button4_pressed)

    def button1_pressed(self):
        self.submitted.emit("Player 1")
        self.close()

    def button2_pressed(self):
        self.submitted.emit("Player 2")
        self.close()

    def button3_pressed(self):
        self.submitted.emit("Player 3")
        self.close()

    def button4_pressed(self):
        self.submitted.emit("Player 4")
        self.close()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.w = None  # No external window yet.

        self.setWindowTitle("Main Window Example")

        self.player_list = ["Player 1", "Player 2", "Player 3", "Player 4"]

        # Label
        self.label = QLabel("               ".join(self.player_list), self)
        self.label.setGeometry(50, 50, 2000, 30)

        # Button
        self.button = QPushButton("Start Next Game", self)
        self.button.setGeometry(100, 100, 100, 30)
        self.button.clicked.connect(self.show_new_window)

    def update_players(self, player_eliminated):
        self.player_list.remove(player_eliminated)
        self.label.setText("               ".join(self.player_list))

    def show_new_window(self, checked):
        if self.w is None:
            #self.w = game3.GameWindow()
            self.w = AnotherWindow("               ".join(self.player_list))
            self.w.submitted.connect(self.update_players)
        self.w.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.showFullScreen()  # Open fullscreen
    sys.exit(app.exec_())

