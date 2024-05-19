from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QGridLayout
from PyQt5.QtGui import QPixmap, QImage
#from PyQt5.QtCore import QRectF


import game3, game2, game1, webcam
import sys
import os
import shutil

image_width = 350
image_height = 320

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
        self.addtextabove.setGeometry(50, 40, 200, 30)
        self.layout.addWidget(self.addtextabove)


        # Labels for Player Text
        player1name = QLabel(" ", self)
        player1name.setGeometry(int(50+image_width/2), 300, image_width, image_height)
        self.layout.addWidget(player1name)

        player2name = QLabel(" ", self)
        player2name.setGeometry(int(50 + (1.25*image_width)+image_width/2), 300, image_width, image_height)
        self.layout.addWidget(player2name)

        player3name = QLabel(" ", self)
        player3name.setGeometry(int(50 + (1.25*image_width)*2+image_width/2), 300, image_width, image_height)
        self.layout.addWidget(player3name)

        player4name = QLabel(" ", self)
        player4name.setGeometry(int(50 + (1.25*image_width)*3+image_width/2), 300, image_width, image_height)
        self.layout.addWidget(player4name)

        self.player_name_labels = [player1name, player2name, player3name, player4name]

        #Labels for Player Images
        player1 = QLabel(self) # label for image
        player1.setGeometry(int(50), 120, image_width, image_height)

        player2 = QLabel(self) # label for image
        player2.setGeometry(int(50 + 1.25*image_width), 120, image_width, image_height)

        player3 = QLabel(self) # label for image
        player3.setGeometry(int(50 + (1.25*image_width)*2), 120, image_width, image_height)

        player4 = QLabel(self) # label for image
        player4.setGeometry(int(50 + (1.25*image_width)*3), 120, image_width, image_height)

        self.player_image_labels = [player1, player2, player3, player4]

        #Labels for Player Crosses
        player1cross = QLabel(self) # label for image
        player1cross.setGeometry(int(50), 120, image_width, image_height)

        player2cross = QLabel(self) # label for image
        player2cross.setGeometry(int(50 + 1.25*image_width), 120, image_width, image_height)

        player3cross = QLabel(self) # label for image
        player3cross.setGeometry(int(50 + (1.25*image_width)*2), 120, image_width, image_height)

        player4cross = QLabel(self) # label for image
        player4cross.setGeometry(int(50 + (1.25*image_width)*3), 120, image_width, image_height)

        self.player_cross_labels = [player1cross, player2cross, player3cross, player4cross]


        # Button
        self.button = QPushButton("Start Next Game", self)
        self.button.setGeometry(100, 220+image_height, 200, 30)
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

    def update_players(self, player_eliminated):
        if((player_eliminated in self.player_list) and (len(self.player_list) != 1)):
            
            player_index = 0
            for player in self.player_list:
                if(player == player_eliminated):
                    break
                player_index+=1

            cross = self.player_cross_labels.pop(player_index) 
            playerim = self.player_image_labels.pop(player_index)
            self.player_name_labels.pop(player_index)     

            pixmap = QPixmap(os.path.join(os.path.dirname(__file__), "User Images", self.player_list[player_index]+".png"))
            scaled_pixmap = pixmap.scaled(image_width, image_height)
            Q_image = QPixmap.toImage(scaled_pixmap)
            grayscale = Q_image.convertToFormat(QImage.Format_Grayscale8)
            grey_pixmap = QPixmap.fromImage(grayscale)
            playerim.setPixmap(grey_pixmap)


            self.player_list.remove(player_eliminated)

            pixmap = QPixmap(os.path.join(os.path.dirname(__file__), "Integrated Images", "cross.png"))
            scaled_pixmap = pixmap.scaled(image_width, image_height)

            cross.setPixmap(scaled_pixmap)
            self.layout.addWidget(cross)
            

    def update_images(self):

        pixmap = QPixmap(os.path.join(os.path.dirname(__file__), "User Images", self.player_list[-1]+".png"))
        scaled_pixmap = pixmap.scaled(image_width, image_height)

        self.player_image_labels[len(self.player_list)-1].setPixmap(scaled_pixmap)
        self.layout.addWidget(self.player_image_labels[len(self.player_list)-1])



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

