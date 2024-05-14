from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel


import game3, game2
import sys


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
        if(len(self.player_list)>1):
            self.player_list.remove(player_eliminated)
            self.label.setText("               ".join(self.player_list))

    def show_new_window(self, checked):
        if(len(self.player_list) == 4):
            self.w = game2.AnotherWindow("               ".join(self.player_list))
            self.w.submitted.connect(self.update_players)
        elif(len(self.player_list) == 3):
            self.w = game2.AnotherWindow("               ".join(self.player_list))
            self.w.submitted.connect(self.update_players)
        else:
            self.w = game3.GameWindow("               ".join(self.player_list))
            self.w.submitted.connect(self.update_players)
        self.w.showMaximized()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.showFullScreen()  # Open fullscreen
    sys.exit(app.exec_())

