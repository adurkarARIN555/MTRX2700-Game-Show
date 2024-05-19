from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit


import game3, game2, game1, webcam
import sys
import os
import shutil

def clear_folder(folder_path):
    if not os.path.exists(folder_path):
        print(f"The folder {folder_path} does not exist.")
        return
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        try:
            # If it's a file, remove it
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
                print(f"File {file_path} has been removed.")
            # If it's a directory, remove it and all its contents
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
                print(f"Directory {file_path} and all its contents have been removed.")
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        desktop = QApplication.desktop()
        screen_geom = desktop.screenGeometry()
        self.widthscreen = screen_geom.width()
        self.heightscreen = screen_geom.height()

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
            player_name_current = self.lineEdit.text()
            self.player_list.append(player_name_current)
            self.label.setText("players remaining:\n\r"+"               ".join(self.player_list))
        self.lineEdit.clear()

        self.w = webcam.WebcamApp(player_name_current)
        self.w.showMaximized()

    def update_players(self, player_eliminated):
        if(player_eliminated in self.player_list):
            print(self.player_list)
            print(player_eliminated)
            self.player_list.remove(player_eliminated)
            self.label.setText("players remaining:\n\r"+"               ".join(self.player_list))

    def show_new_window(self, checked):
        if(len(self.player_list) == 4):
            self.w = game1.GameWindow("               ".join(self.player_list), self.widthscreen, self.heightscreen)
            self.w.submitted.connect(self.update_players)
        elif(len(self.player_list) == 3):
            self.w = game2.AnotherWindow("               ".join(self.player_list), self.widthscreen, self.heightscreen)
            self.w.submitted.connect(self.update_players)
        else:
            self.w = game3.GameWindow("               ".join(self.player_list), self.widthscreen, self.heightscreen)
            self.w.submitted.connect(self.update_players)
        self.w.showMaximized()

    def closeEvent(self, event):
        clear_folder("User Images")
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.showFullScreen()  # Open fullscreen
    sys.exit(app.exec_())

