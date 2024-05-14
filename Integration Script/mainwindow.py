from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit


import game3, game2, game1
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.w = None  # No external window yet.

        self.setWindowTitle("Main Window Example")

        self.player_list = []

        self.lineEdit = QLineEdit(self)
        self.lineEdit.setGeometry(10, 10, 200, 30)
        self.lineEdit.returnPressed.connect(self.player_name_entered)

        # Label
        self.label = QLabel("players remaining:\n\r"+"               ".join(self.player_list), self)
        self.label.setGeometry(50, 50, 2000, 30)

        # Button
        self.button = QPushButton("Start Next Game", self)
        self.button.setGeometry(100, 100, 100, 30)
        self.button.clicked.connect(self.show_new_window)

    def player_name_entered(self):
        if(len(self.player_list)<4):
            self.player_list.append(self.lineEdit.text())
            self.label.setText("players remaining:\n\r"+"               ".join(self.player_list))
        self.lineEdit.clear()

    def update_players(self, player_eliminated):
        if(len(self.player_list)>1):
            self.player_list.remove(player_eliminated)
            self.label.setText("players remaining:\n\r"+"               ".join(self.player_list))

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

