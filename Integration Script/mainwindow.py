from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QGridLayout
from PyQt5.QtGui import QPixmap
#from PyQt5.QtCore import QRectF


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

        self.layout = QGridLayout(self)

        self.lineEdit = QLineEdit(self)
        self.lineEdit.setGeometry(10, 10, 200, 30)
        self.lineEdit.returnPressed.connect(self.player_name_entered)

        self.addtextabove = QLabel("Players Remaining:", self)
        self.addtextabove.setGeometry(50, 40, 200, 200)
        self.layout.addWidget(self.addtextabove)


        # Labels for Player Text
        player1name = QLabel(" ", self)
        player1name.setGeometry(50, 60, 200, 200)
        self.layout.addWidget(player1name)

        player2name = QLabel(" ", self)
        player2name.setGeometry(250, 60, 200, 200)
        self.layout.addWidget(player2name)

        player3name = QLabel(" ", self)
        player3name.setGeometry(450, 60, 200, 200)
        self.layout.addWidget(player3name)

        player4name = QLabel(" ", self)
        player4name.setGeometry(650, 60, 200, 200)
        self.layout.addWidget(player4name)

        self.player_name_labels = [player1name, player2name, player3name, player4name]

        #Labels for Player Images
        player1 = QLabel(self) # label for image
        player1.setGeometry(50, 120, 200, 220)

        player2 = QLabel(self) # label for image
        player2.setGeometry(250, 120, 200, 220)

        player3 = QLabel(self) # label for image
        player3.setGeometry(450, 120, 200, 220)

        player4 = QLabel(self) # label for image
        player4.setGeometry(650, 120, 200, 220)

        self.player_image_labels = [player1, player2, player3, player4]


        # Button
        self.button = QPushButton("Start Next Game", self)
        self.button.setGeometry(100, 400, 200, 30)
        self.button.clicked.connect(self.show_new_window)

    def player_name_entered(self):
        if(len(self.player_list)<4):
            player_name_current = self.lineEdit.text()
            self.player_list.append(player_name_current)
            self.player_name_labels[len(self.player_list)-1].setText(player_name_current)
        self.lineEdit.clear()

        self.w = webcam.WebcamApp(player_name_current)
        self.w.submitted.connect(self.update_images)
        self.w.showMaximized()

        #User Images/self.player_name_current.png
        #print("Hello")

    def update_players(self, player_eliminated):
        if(player_eliminated in self.player_list):
            print(self.player_list)
            print(player_eliminated)
            self.player_list.remove(player_eliminated)
            self.label.setText("players remaining:\n\r"+"               ".join(self.player_list))

    def update_images(self):
        #print("hello")
        # current_user_image = QImage(os.path.join(os.path.dirname(__file__), "User Images", self.player_list[-1]+".png"))

        # painter = QPainter(self)
        # painter.setRenderHint(QPainter.Antialiasing)
        # painter.drawImage(QRectF(0, 0, 1500, 800), current_user_image)

        pixmap = QPixmap(os.path.join(os.path.dirname(__file__), "User Images", self.player_list[-1]+".png"))
        scaled_pixmap = pixmap.scaled(150, 100)



        self.player_image_labels[len(self.player_list)-1].setPixmap(scaled_pixmap)
        #self.label.setPixmap(scaled_pixmap)
        self.layout.addWidget(self.player_image_labels[len(self.player_list)-1])

        #self.label.move(0, 190)



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

