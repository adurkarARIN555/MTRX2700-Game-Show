import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor, QImage, QTransform
from PyQt5.QtCore import QTimer, QObject, pyqtSignal, pyqtSlot, QRectF
import serial
import numpy as np
import threading
import os

steering_sensitivity = 250

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

port1 = "COM7"
port2 = "COM10"

class Player:
    def __init__(self, start_x_pos, start_y_pos, port, image, player_id):
        self.player_id = player_id
        self.start_x_pos = start_x_pos
        self.start_y_pos = start_y_pos
        self.x_pos = start_x_pos
        self.y_pos = start_y_pos

        self.delta_angle = 0
        self.velocity = 0
        self.angle = 0
        self.steering_output = 0
        self.passed = 0
        self.lap_count = 0

        self.image_obj = QImage(os.path.join(os.path.dirname(__file__), "GAME3 Images", image))

        self.serial_port = serial.Serial(port, baud)
        self.serial_reader = SerialReader(self.serial_port)
        self.serial_thread = threading.Thread(target=self.serial_reader.run)
        

def process_steering_data(serial_port):
    try:
        line = serial_port.readline().decode("utf-8").strip()
        steering_angle = 0
        if line:
            data = line.split(",")
            #print(data)
            steering_angle = float(data[0])  # Angle
            velocity = (data[1])
        return [str(-steering_angle / steering_sensitivity), velocity]
    except:
        return(["0","0"])


class SerialReader(QObject):
    data_received = pyqtSignal(str)

    def __init__(self, serial_port):
        super().__init__()
        self.serial_port = serial_port
        self.running = True

    def run(self):
        while self.running:
            try:
                if self.serial_port.in_waiting:
                    controller_input = process_steering_data(self.serial_port)
                    self.data_received.emit(",".join(controller_input))
            except:
                print("Read failed")
                self.data_received.emit(",".join([0,0]))

    def stop(self):
        self.running = False

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

    def __init__(self, argument):
        players = argument.split("               ")

        self.player1 = Player(start_x_pos=670, start_y_pos=95, port=port1, image="mario.png", player_id=players[0])
        try:
            self.player1.serial_port.write(b'2')
        except:
            print("write 2 failed")
        self.player2 = Player(start_x_pos=630, start_y_pos=155, port=port2, image="luigi.png", player_id=players[1])
        try:
            self.player2.serial_port.write(b'3')
        except:
            print("write 3 failed")

        super().__init__()
        self.setGeometry(100, 100, 400, 200)
        self.setStyleSheet("background-color: white;")

        self.player1.serial_reader.data_received.connect(self.player1_update_steering)
        self.player2.serial_reader.data_received.connect(self.player2_update_steering)
        self.player1.serial_thread.start()
        self.player2.serial_thread.start()
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_position)
        self.timer.start(40) 

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawImage(QRectF(0, 0, 1500, 800), background_image)
        painter.setBrush(QColor(30, 30, 0))
        painter.drawEllipse(outer_track_x, outer_track_y, outer_track_width, outer_track_height)
        painter.setBrush(QColor(255, 255, 255))
        #painter.drawEllipse(inner_track_x, inner_track_y, inner_track_width, inner_track_height)

        painter.drawImage(QRectF(695, 25, 10, 195), finishline_image)
        painter.drawImage(QRectF(inner_track_x-328, inner_track_y-198, inner_track_width+680, inner_track_height+400), inner_background_image)

        for player in [self.player1, self.player2]:

            transformed_kart_image = player.image_obj.transformed(QTransform().rotate(player.steering_output*(180/np.pi) + 90))

            qrect_obj = QRectF(int(player.x_pos) - (kart_size/2), int(player.y_pos) - (kart_size/2), kart_size, kart_size)

            center = qrect_obj.center()
            transform_for_rect = QTransform().translate(center.x(), center.y()).rotate(player.steering_output*(180/np.pi) + 90).translate(-center.x(), -center.y())

            rotated_rect = transform_for_rect.mapRect(qrect_obj)

            painter.drawImage(rotated_rect, transformed_kart_image)
            
        painter.drawImage(QRectF(inner_track_x-335, inner_track_y-198, inner_track_width+660, inner_track_height+400), td_inner_background_image)
        

    @pyqtSlot(str)
    def player1_update_steering(self, controller_input):
        try:
            self.player1.delta_angle = float(controller_input.split(",")[0])
            self.player1.velocity = float(controller_input.split(",")[1])
            # if (self.player1.velocity > 0):
            self.player1.angle = self.player1.delta_angle + self.player1.angle
            self.player1.steering_output += self.player1.angle / 10
        except ValueError:
            print("Invalid data received from serial port:", controller_input)

    @pyqtSlot(str)
    def player2_update_steering(self, controller_input):
        try:
            self.player2.delta_angle = float(controller_input.split(",")[0])
            self.player2.velocity = float(controller_input.split(",")[1])
            # if (self.player2.velocity > 0):
            self.player2.angle = self.player2.delta_angle + self.player2.angle
            self.player2.steering_output += self.player2.angle / 10
        except ValueError:
            print("Invalid data received from serial port:", controller_input)

    def update_position(self):

        for player in [self.player1, self.player2]:

            player.x_pos += player.velocity * np.cos(player.steering_output)
            player.y_pos += player.velocity * np.sin(player.steering_output)

            if(check_collided_outer(player.x_pos, player.y_pos) or check_collided_inner(player.x_pos, player.y_pos)):
                player.x_pos = player.start_x_pos
                player.y_pos = player.start_y_pos
                player.passed = 0
                try:
                    player.serial_port.write(b'1')
                except:
                    print("write 1 failed")
            
            checkpoint_check = checkpoint(player.x_pos, player.y_pos, player.passed)
            if (checkpoint_check == 2):
                player.passed = 1
            if (checkpoint_check == 1):
                player.passed = 0
                player.lap_count += 1
                #print(player.lap_count)
            if (player.lap_count == 3):
                self.game_won(player.player_id)



        self.update()  # Trigger repaint

    def game_won(self,winner):
        for player in [self.player2, self.player1]:
            player.serial_reader.stop()
            player.serial_thread.join()

        for player in [self.player2, self.player1]:
            if(player.player_id == winner):
                continue
            else:
                self.submitted.emit(player.player_id)
                self.close()
            
        

def check_collided_outer(x, y):
    x_block = ((2*x - 2*outer_track_x - outer_track_width)/outer_track_width)**2
    y_block = ((2*y - 2*outer_track_y - outer_track_height)/outer_track_height)**2
    LHS = x_block + y_block
    return(LHS > 1)

def check_collided_inner(x, y):
    x_block = ((2*x - 2*inner_track_x - inner_track_width)/inner_track_width)**2
    y_block = ((2*y - 2*inner_track_y - inner_track_height)/inner_track_height)**2
    LHS = x_block + y_block
    return(LHS < 1)

def checkpoint(x, y, passed):
    if (passed == 0):
        if ((x >= 670) and (x <= 690) and (y >= 545) and (y <= 750)): 
            return 2
    else:
        if ((x >= 670) and (x <= 690) and (y >= 25) and (y <= 220)):
            return 1
    
    return 0

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GameWindow("               ".join(["Tom", "James"]))
    window.showMaximized()
    sys.exit(app.exec_())