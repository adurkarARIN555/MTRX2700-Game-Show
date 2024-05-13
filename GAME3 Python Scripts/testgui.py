import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor, QImage, QTransform
from PyQt5.QtCore import QTimer, QObject, pyqtSignal, pyqtSlot, QRectF
import serial
import numpy as np
import threading
import os

steering_sensitivity = 250

outer_track_width = 1000
outer_track_height = 625
outer_track_x = 200
outer_track_y = 75

inner_track_width = 700
inner_track_height = 325
inner_track_x = 350
inner_track_y = 220

kart_size = 60

port = "COM10"
baud = 115200

class Player:
    def __init__(self, start_x_pos, start_y_pos):
        self.start_x_pos = start_x_pos
        self.start_y_pos = start_y_pos
        self.x_pos = start_x_pos
        self.y_pos = start_y_pos

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
            if self.serial_port.in_waiting:
                controller_input = process_steering_data(self.serial_port)
                self.data_received.emit(",".join(controller_input))

    def stop(self):
        self.running = False

image_path = os.path.join(os.path.dirname(__file__), "GAME3 Images", "luigi.png")
kart_image = QImage(image_path)

f_image_path = os.path.join(os.path.dirname(__file__), "GAME3 Images", "finishline.png")
finishline_image = QImage(f_image_path)

class GameWindow(QWidget):
    def __init__(self):
        self.player1 = Player(start_x_pos=670, start_y_pos=150)
        super().__init__()
        self.setGeometry(100, 100, 400, 200)
        self.setStyleSheet("background-color: white;")
        self.delta_angle = 0
        self.velocity = 0
        self.angle = 0
        self.steering_output = 0
        self.passed = 0
        self.lap_count = 0
        self.serial_port = serial.Serial(port, baud)  # Adjust baudrate as per your requirement
        self.serial_reader = SerialReader(self.serial_port)
        self.serial_thread = threading.Thread(target=self.serial_reader.run)
        self.serial_reader.data_received.connect(self.update_steering)
        self.serial_thread.start()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_position)
        self.timer.start(10)  # Update every 10 milliseconds

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(30, 30, 0))
        painter.drawEllipse(outer_track_x, outer_track_y, outer_track_width, outer_track_height)
        painter.setBrush(QColor(255, 255, 255))
        painter.drawEllipse(inner_track_x, inner_track_y, inner_track_width, inner_track_height)

        transformed_kart_image = kart_image.transformed(QTransform().rotate(self.steering_output*(180/np.pi) + 90))

        qrect_obj = QRectF(int(self.player1.x_pos) - (kart_size/2), int(self.player1.y_pos) - (kart_size/2), kart_size, kart_size)


        center = qrect_obj.center()
        transform_for_rect = QTransform().translate(center.x(), center.y()).rotate(self.steering_output*(180/np.pi) + 90).translate(-center.x(), -center.y())

        rotated_rect = transform_for_rect.mapRect(qrect_obj)

        painter.drawImage(QRectF(695, 75, 10, 145), finishline_image)
        painter.drawImage(rotated_rect, transformed_kart_image)
        

    @pyqtSlot(str)
    def update_steering(self, controller_input):
        try:
            # Map the value to the position on the screen
            self.delta_angle = float(controller_input.split(",")[0])
            self.velocity = float(controller_input.split(",")[1])
            if (self.velocity > 0):
                self.angle = self.delta_angle + self.angle
                self.steering_output = self.steering_output + self.angle / 10
        except ValueError:
            print("Invalid data received from serial port:", controller_input)

    def update_position(self):

        self.player1.x_pos = self.player1.x_pos + self.velocity * np.cos(self.steering_output)
        self.player1.y_pos = self.player1.y_pos + self.velocity * np.sin(self.steering_output)

        if(check_collided_outer(self.player1.x_pos, self.player1.y_pos) or check_collided_inner(self.player1.x_pos, self.player1.y_pos)):
            self.player1.x_pos = self.player1.start_x_pos
            self.player1.y_pos = self.player1.start_y_pos
            self.passed = 0
            self.serial_port.write(b'1')
        
        checkpoint_check = checkpoint(self.player1.x_pos, self.player1.y_pos, self.passed)
        if (checkpoint_check == 2):
            self.passed = 1
        if (checkpoint_check == 1):
            self.passed = 0
            self.lap_count += 1
            print(self.lap_count)


        self.update()  # Trigger repaint

    def closeEvent(self, event):
        self.serial_reader.stop()
        self.serial_thread.join()

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
        if ((x >= 670) and (x <= 690) and (y >= 545) and (y <= 700)): 
            return 2
    else:
        if ((x >= 670) and (x <= 690) and (y >= 75) and (y <= 220)):
            return 1
    
    return 0

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GameWindow()
    window.showMaximized()
    sys.exit(app.exec_())