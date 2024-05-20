# Impoerting relevant libraries and modules
import sys
import serial
import numpy as np
import threading
import os
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor, QImage, QTransform
from PyQt5.QtCore import QTimer, QObject, pyqtSignal, pyqtSlot, QRectF

# Defining constants to remove magic numbers
port1 = "COM7"
port2 = "COM10"
outer_track_width = 1100
outer_track_height = 725
outer_track_x = 150
outer_track_y = 25
inner_track_width = 700
inner_track_height = 325
inner_track_x = 350
inner_track_y = 220
kart_size = 60
baud = 115200
player1_start_x_position = 670
player1_start_y_position = 95
player2_start_x_position = 630
player2_start_y_position = 155
timer_ms = 40
background_x_offset = 0
background_y_offset = 0
background_width = 1500
background_height = 800
finish_line_x_offset = 695
finish_line_y_offset = 25
finish_line_width = 10
finish_line_height = 195
inner_background_x_offset = 328
inner_background_y_offset = 198
inner_background_width = 680
inner_background_height = 400
td_inner_background_x_offset = 335
td_inner_background_width = 660
player1_textbox_x_offset = 0
player1_textbox_y_offset = 0
textbox_width = 250
textbox_height = 150
player2_textbox_x_offset = 1250
player2_textbox_y_offset = 0
player1_text_offset_x = 30
player1_text_offset_y = 70
player2_text_offset_x = 1280
player2_text_offset_y = 70
player1_lap_count_text_offset_x = 30
player1_lap_count_text_offset_y = 30
player2_lap_count_text_offset_x = 1280
player2_lap_count_text_offset_y = 30
maximum_laps = 3
checkpoint_lower_bound_x = 670
checkpoint_upper_bound_x = 690
finish_line_lower_bound_y = 25
finish_line_upper_bound_y = 220
bottom_checkpoint_lower_bound_y = 545
bottom_checkpoint_upper_bound_y = 750


# Class for each player
class Player:
    def __init__(self, start_x_pos, start_y_pos, port, image, player_id):
        # Player name
        self.player_id = player_id

        # Coordinates
        self.start_x_pos = start_x_pos
        self.start_y_pos = start_y_pos
        self.x_pos = start_x_pos
        self.y_pos = start_y_pos

        # Kart parameters
        self.delta_angle = 0
        self.velocity = 0
        self.angle = 0
        self.steering_output = 0
        self.passed = 0
        self.lap_count = 0

        # Kart image
        self.image = image
        self.image_obj = QImage(os.path.join(os.path.dirname(__file__), "GAME3 Images", image))

        # Microcontroller gyroscope communication
        self.serial_port = serial.Serial(port, baud)
        self.serial_reader = SerialReader(self.serial_port)
        self.serial_thread = threading.Thread(target=self.serial_reader.run)
        
# Gets the velocity and position coordinates for the kart calculated in the microcontroller
def process_steering_data(serial_port):
    try:
        line = serial_port.readline().decode("utf-8").strip()
        steering_angle = 0
        
        if line:
            data = line.split(",")

            steering_angle = float(data[0])
            x_pos = (data[1])
            y_pos = (data[2])
        return [str(steering_angle), x_pos, y_pos]
    except:
        return(["0","0","0"])

# Multithreadding for reading serial data
class SerialReader(QObject):
    data_received = pyqtSignal(str) # Signal to ensure synchonicity within the integration

    # Initialise a new thread
    def __init__(self, serial_port):
        super().__init__()
        self.serial_port = serial_port
        self.running = True

    # Checks the serial line for data
    def run(self):
        while self.running:
            try:
                if self.serial_port.in_waiting:
                    controller_input = process_steering_data(self.serial_port)
                    self.data_received.emit(",".join(controller_input))
            except:
                print("Read failed")
                self.data_received.emit(",".join([0,0]))

    # Stops the thread
    def stop(self):
        self.running = False

# Getting the track images from the directory
f_image_path = os.path.join(os.path.dirname(__file__), "GAME3 Images", "finishline.png")
finishline_image = QImage(f_image_path)

background_path = os.path.join(os.path.dirname(__file__), "GAME3 Images", "Background.png")
background_image = QImage(background_path)

inner_background_path = os.path.join(os.path.dirname(__file__), "GAME3 Images", "inner_background.png")
inner_background_image = QImage(inner_background_path)

td_inner_background_path = os.path.join(os.path.dirname(__file__), "GAME3 Images", "3d_inner_background.png")
td_inner_background_image = QImage(td_inner_background_path)

class GameWindow(QWidget):
    submitted = pyqtSignal(str)

    # Initialises the two players
    def __init__(self, argument, width, height):
        players = argument.split("               ")

        self.screenwidth = width
        self.screenheight = height

        # Creates player 1
        self.player1 = Player(start_x_pos=player1_start_x_position, start_y_pos=player1_start_y_position, port=port1, image="mario.png", player_id=players[0])
        try:
            self.player1.serial_port.write(b'2')
        except:
            print("write 2 failed")
        # Creates player 2
        self.player2 = Player(start_x_pos=player2_start_x_position, start_y_pos=player2_start_y_position, port=port2, image="luigi.png", player_id=players[1])
        try:
            self.player2.serial_port.write(b'3')
        except:
            print("write 3 failed")

        super().__init__()

        self.setStyleSheet("background-color: white;")

        # Connects both karts to their respective micrcontroller on individual thread
        self.player1.serial_reader.data_received.connect(self.player1_update_steering)
        self.player2.serial_reader.data_received.connect(self.player2_update_steering)
        self.player1.serial_thread.start()
        self.player2.serial_thread.start()

        # Timer for frequency of kart parameter updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_position)
        self.timer.start(timer_ms) 

    # Displays everything on the GUI
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # Displays the background on the GUI
        painter.drawImage(QRectF(background_x_offset, background_y_offset, background_width, background_height), background_image)
        painter.setBrush(QColor(30, 30, 0))
        # Displays the track on the GUI
        painter.drawEllipse(outer_track_x, outer_track_y, outer_track_width, outer_track_height)
        painter.setBrush(QColor(255, 255, 255))
        # Displays the finish line on the GUI
        painter.drawImage(QRectF(finish_line_x_offset, finish_line_y_offset, finish_line_width, finish_line_height), finishline_image)
        painter.drawImage(QRectF(inner_track_x-inner_background_x_offset, inner_track_y-inner_background_y_offset, inner_track_width+inner_background_width, inner_track_height+inner_background_height), inner_background_image)

        # Scales and maps the kart image to bounding rectangle
        for player in [self.player1, self.player2]:
            # Rotates the image with the rotation of the rectangle bounding the image
            transformed_kart_image = player.image_obj.transformed(QTransform().rotate(player.steering_output*(180/np.pi) + 90))
            qrect_obj = QRectF(int(player.x_pos) - (kart_size/2), int(player.y_pos) - (kart_size/2), kart_size, kart_size)

            center = qrect_obj.center()
            transform_for_rect = QTransform().translate(center.x(), center.y()).rotate(player.steering_output*(180/np.pi) + 90).translate(-center.x(), -center.y())

            rotated_rect = transform_for_rect.mapRect(qrect_obj)

            painter.drawImage(rotated_rect, transformed_kart_image)

        # Displays the three-dimensional effect of the inner background on the GUI
        painter.drawImage(QRectF(inner_track_x-td_inner_background_x_offset, inner_track_y-inner_background_y_offset, inner_track_width+td_inner_background_width, inner_track_height+inner_background_height), td_inner_background_image)

        # Displays the lap count and character for player1 on the GUI
        box_for_text = QRectF(player1_textbox_x_offset,player1_textbox_y_offset,textbox_width,textbox_height)
        painter.setBrush(QColor(255, 255, 255))
        painter.drawRect(box_for_text)
        painter.drawText(player1_lap_count_text_offset_x,player1_lap_count_text_offset_y,str(self.player1.lap_count+1)+"/3")
        painter.drawText(player1_text_offset_x,player1_text_offset_y,self.player1.player_id+" is "+self.player1.image.split(".png")[0])

        # Displays the lap count and character for player2 on the GUI
        box_for_text = QRectF(player2_textbox_x_offset,player2_textbox_y_offset,textbox_width,textbox_height)
        painter.setBrush(QColor(255, 255, 255))
        painter.drawRect(box_for_text)
        painter.drawText(player2_lap_count_text_offset_x,player2_lap_count_text_offset_y,str(self.player2.lap_count+1)+"/3")
        painter.drawText(player2_text_offset_x,player2_text_offset_y,self.player2.player_id+" is "+self.player2.image.split(".png")[0])

    @pyqtSlot(str)
    # Updates the steering angle of player1's kart
    def player1_update_steering(self, controller_input):
        try:
            self.player1.steering_output = float(controller_input.split(",")[0])
            self.player1.x_pos = float(controller_input.split(",")[1])
            self.player1.y_pos = float(controller_input.split(",")[2])
        except ValueError:
            print("Invalid data received from serial port:", controller_input)

    @pyqtSlot(str)
    # Updates the steering angle of player2's kart
    def player2_update_steering(self, controller_input):
        try:
            self.player2.steering_output = float(controller_input.split(",")[0])
            self.player2.x_pos = float(controller_input.split(",")[1])
            self.player2.y_pos = float(controller_input.split(",")[2])
        except ValueError:
            print("Invalid data received from serial port:", controller_input)

    # Updates the position of the kart
    def update_position(self):
        for player in [self.player1, self.player2]:
            if(check_collided_outer(player.x_pos, player.y_pos) or check_collided_inner(player.x_pos, player.y_pos)):
                # Respawns the kart at the finish line
                player.x_pos = player.start_x_pos
                player.y_pos = player.start_y_pos
                # Remove their checkpoint clearing flag
                player.passed = 0
                try:
                    player.serial_port.write(b'1')
                except:
                    print("write 1 failed")
            
            checkpoint_check = checkpoint(player.x_pos, player.y_pos, player.passed)
            
            if (checkpoint_check == 2):
                # Kart has passed the checkpoint
                player.passed = 1
            elif (checkpoint_check == 1):
                # Kart had passed the checkpoint, and has now passed the finish line
                player.passed = 0
                player.lap_count += 1

            # Determines if the game has finished
            if (player.lap_count == maximum_laps):
                self.game_won(player.player_id)

        # Triggers a repaint of the GUI
        self.update()

    # When three laps have been completed the game will be stopped
    def game_won(self,winner):
        # Stops the threadding for serial data receiving 
        for player in [self.player2, self.player1]:
            player.serial_reader.stop()
            player.serial_thread.join()

        # Eliminating the loser
        for player in [self.player2, self.player1]:
            if(player.player_id == winner):
                continue
            else:
                self.submitted.emit(player.player_id)
                self.close()
            
# Checks for kart collision with outer track
def check_collided_outer(x, y):
    x_block = ((2*x - 2*outer_track_x - outer_track_width)/outer_track_width)**2
    y_block = ((2*y - 2*outer_track_y - outer_track_height)/outer_track_height)**2
    LHS = x_block + y_block
    return(LHS > 1)

# Checks for kart collision with inner track
def check_collided_inner(x, y):
    x_block = ((2*x - 2*inner_track_x - inner_track_width)/inner_track_width)**2
    y_block = ((2*y - 2*inner_track_y - inner_track_height)/inner_track_height)**2
    LHS = x_block + y_block
    return(LHS < 1)

# Checks if the checkpoint has been passed
def checkpoint(x, y, passed):
    if (passed == 0):
        # Sees if the kart has now passed the checkpoint
        if ((x >= checkpoint_lower_bound_x) and (x <= checkpoint_upper_bound_x) and (y >= bottom_checkpoint_lower_bound_y) and (y <= bottom_checkpoint_upper_bound_y)): 
            return 2
    else:
        # Kart has passed the checkpoint, now sees if the kart has reached the finish line
        if ((x >= checkpoint_lower_bound_x) and (x <= checkpoint_upper_bound_x) and (y >= finish_line_lower_bound_y) and (y <= finish_line_upper_bound_y)):
            return 1

    # Kart has not passed the checkpoint
    return 0

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Gets the computer screen geometry
    desktop = QApplication.desktop()
    screen_geom = desktop.screenGeometry()
    widthscreen = screen_geom.width()
    heightscreen = screen_geom.height()
    
    window = GameWindow("               ".join(["Tom", "James"]), widthscreen,heightscreen) # Creates the game window
    window.showMaximized() # Opens the window maximised
    sys.exit(app.exec_())
