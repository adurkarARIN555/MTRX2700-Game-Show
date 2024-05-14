from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget

import game3

import sys

from random import randint


class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self, argument):
        super().__init__()
        players = argument.split("               ")
        
        self.button = QPushButton(players[0], self)
        self.button.setGeometry(100, 100, 100, 30)

        self.button2 = QPushButton(players[1], self)
        self.button2.setGeometry(100, 60, 100, 30)



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

    def show_new_window(self, checked):
        if self.w is None:
            #self.w = game3.GameWindow()
            self.w = AnotherWindow("               ".join(self.player_list))
        self.w.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.showFullScreen()  # Open fullscreen
    sys.exit(app.exec_())

