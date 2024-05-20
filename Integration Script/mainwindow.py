# Importing relevant modules and libraries
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QGridLayout
from PyQt5.QtGui import QPixmap, QImage
import game3, game2, game1, webcam
import sys
import os
import shutil

# Defining constants to remove magic numbers
image_width = 350
image_height = 320
player_name_offset = 300
player_photo_offset = 120
image_scaling_factor = 1.25
player_name_and_photo_x_offset = 50
next_game_x_offset = 100
next_game_y_offset = 220
next_game_width = 200
next_game_height = 30
maximum_player_length = 4
player_name_x_offset = 10
player_name_y_offset = 10
player_name_width = 200
player_name_height = 30
players_remaining_x_offset = 50
players_remaining_y_offset = 40
players_remaining_width = 200
players_remaining_height = 30

# Removes the user images from the webcam once the program is finished
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

        # Gets the dimensions of the computers screen
        desktop = QApplication.desktop()
        screen_geom = desktop.screenGeometry()
        self.widthscreen = screen_geom.width()
        self.heightscreen = screen_geom.height()

        self.w = None  # No external window yet

        self.setWindowTitle("Main Window Example")

        self.player_list = []

        self.layout = QGridLayout(self)

        # Creates a spot to write the player names
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setGeometry(player_name_x_offset, player_name_y_offset, player_name_width, player_name_height)
        self.lineEdit.returnPressed.connect(self.player_name_entered)

        # Creates a spot to show which players are still remaining
        self.addtextabove = QLabel("Players Remaining:", self)
        self.addtextabove.setGeometry(players_remaining_x_offset, players_remaining_y_offset, players_remaining_width, players_remaining_height)
        self.layout.addWidget(self.addtextabove)

        # Labels for player names
        player1name = QLabel(" ", self)
        player1name.setGeometry(int(player_name_and_photo_x_offset+image_width/2), player_name_offset, image_width, image_height)
        self.layout.addWidget(player1name)

        player2name = QLabel(" ", self)
        player2name.setGeometry(int(player_name_and_photo_x_offset + (image_scaling_factor*image_width)+image_width/2), player_name_offset, image_width, image_height)
        self.layout.addWidget(player2name)

        player3name = QLabel(" ", self)
        player3name.setGeometry(int(player_name_and_photo_x_offset + (image_scaling_factor*image_width)*2+image_width/2), player_name_offset, image_width, image_height)
        self.layout.addWidget(player3name)

        player4name = QLabel(" ", self)
        player4name.setGeometry(int(player_name_and_photo_x_offset + (image_scaling_factor*image_width)*3+image_width/2), player_name_offset, image_width, image_height)
        self.layout.addWidget(player4name)

        self.player_name_labels = [player1name, player2name, player3name, player4name]

        # Labels for player images
        player1 = QLabel(self)
        player1.setGeometry(int(player_name_and_photo_x_offset), player_photo_offset, image_width, image_height)

        player2 = QLabel(self)
        player2.setGeometry(int(player_name_and_photo_x_offset + image_scaling_factor*image_width), player_photo_offset, image_width, image_height)

        player3 = QLabel(self)
        player3.setGeometry(int(player_name_and_photo_x_offset + (image_scaling_factor*image_width)*2), player_photo_offset, image_width, image_height)

        player4 = QLabel(self)
        player4.setGeometry(int(player_name_and_photo_x_offset + (image_scaling_factor*image_width)*3), player_photo_offset, image_width, image_height)

        self.player_image_labels = [player1, player2, player3, player4]

        # Labels for player crosses
        player1cross = QLabel(self)
        player1cross.setGeometry(int(player_name_and_photo_x_offset), player_photo_offset, image_width, image_height)

        player2cross = QLabel(self)
        player2cross.setGeometry(int(player_name_and_photo_x_offset + image_scaling_factor*image_width), player_photo_offset, image_width, image_height)

        player3cross = QLabel(self)
        player3cross.setGeometry(int(player_name_and_photo_x_offset + (image_scaling_factor*image_width)*2), player_photo_offset, image_width, image_height)

        player4cross = QLabel(self)
        player4cross.setGeometry(int(player_name_and_photo_x_offset + (image_scaling_factor*image_width)*3), player_photo_offset, image_width, image_height)

        self.player_cross_labels = [player1cross, player2cross, player3cross, player4cross]


        # Button to start the next game
        self.button = QPushButton("Start Next Game", self)
        self.button.setGeometry(next_game_x_offset, next_game_y_offset+image_height, next_game_width, next_game_height)
        self.button.clicked.connect(self.show_new_window)

    # Instantiates player name and image
    def player_name_entered(self):
        if(len(self.player_list)<maximum_player_length):
            player_name_current = self.lineEdit.text()
            self.player_list.append(player_name_current)
            self.player_name_labels[len(self.player_list)-1].setText(player_name_current)
        self.lineEdit.clear()

        self.w = webcam.WebcamApp(player_name_current)
        self.w.submitted.connect(self.update_images)
        self.w.showMaximized()

    # Keeps track of which players are still alive
    def update_players(self, player_eliminated):
        if((player_eliminated in self.player_list) and (len(self.player_list) != 1)):
            player_index = 0

            # Finds the player that is to be eliminated
            for player in self.player_list: 
                if(player == player_eliminated):
                    break
                player_index+=1

            # Removes player from alive player lists
            cross = self.player_cross_labels.pop(player_index) 
            playerim = self.player_image_labels.pop(player_index)
            self.player_name_labels.pop(player_index)     

            # Converts the image of eliminated players to grayscale
            pixmap = QPixmap(os.path.join(os.path.dirname(__file__), "User Images", self.player_list[player_index]+".png"))
            scaled_pixmap = pixmap.scaled(image_width, image_height)
            Q_image = QPixmap.toImage(scaled_pixmap)
            grayscale = Q_image.convertToFormat(QImage.Format_Grayscale8)
            grey_pixmap = QPixmap.fromImage(grayscale)
            playerim.setPixmap(grey_pixmap)

            self.player_list.remove(player_eliminated)

            # Adds a cross over the image of eliminated players
            pixmap = QPixmap(os.path.join(os.path.dirname(__file__), "Integrated Images", "cross.png"))
            scaled_pixmap = pixmap.scaled(image_width, image_height)
            cross.setPixmap(scaled_pixmap)
            self.layout.addWidget(cross)
            
    # Displays the user image on the GUI
    def update_images(self):
        # Creates a pixmap of the image
        pixmap = QPixmap(os.path.join(os.path.dirname(__file__), "User Images", self.player_list[-1]+".png"))
        scaled_pixmap = pixmap.scaled(image_width, image_height)

        # Places the image onto the desired label in the GUI
        self.player_image_labels[len(self.player_list)-1].setPixmap(scaled_pixmap)
        self.layout.addWidget(self.player_image_labels[len(self.player_list)-1])

    # Determines which game mode is to be played based on the number of remaining players
    def show_new_window(self, checked):
        if(len(self.player_list) == (maximum_player_length)):
            self.w = game1.GameWindow("               ".join(self.player_list), self.widthscreen, self.heightscreen)
            self.w.submitted.connect(self.update_players)
        elif(len(self.player_list) == (maximum_player_length-1)):
            self.w = game2.AnotherWindow("               ".join(self.player_list), self.widthscreen, self.heightscreen)
            self.w.submitted.connect(self.update_players)
        else:
            self.w = game3.GameWindow("               ".join(self.player_list), self.widthscreen, self.heightscreen)
            self.w.submitted.connect(self.update_players)
        self.w.showMaximized()

    # Closes the application window
    def closeEvent(self, event):
        clear_folder("User Images")
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.showFullScreen()  # Open fullscreen
    sys.exit(app.exec_())
