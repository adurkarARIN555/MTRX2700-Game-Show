import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor, QImage, QTransform
from PyQt5.QtCore import QTimer, QObject, pyqtSignal, pyqtSlot, QRect, QRectF, QPointF
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


def process_steering_data(serial_port):
    try:
        line = serial_port.readline().decode("utf-8").strip()
        steering_angle = 0
        if line:
            data = line.split(",")
            #print(data)
            steering_angle = float(data[0])  # Angle
            acceleration_toggle = (data[1])
        return [str(-steering_angle / steering_sensitivity), acceleration_toggle]
    except:
        return(["0","0"])

    

def scaling_factor(theta):
    #factor = np.abs(np.sin(theta))+np.abs(np.cos(theta))
    factor = np.sin(4*(theta-(np.pi/8))) + 2
    return(factor)

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

image_path = os.path.join(os.path.dirname(__file__), "GAME3 Images", "mario-kart-5639670_640.png")
kart_image = QImage(image_path)

class DotWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 400, 200)
        self.setStyleSheet("background-color: white;")
        self.delta_angle = 0
        self.accelerator = 0
        self.pos_x = 400
        self.pos_y = 500
        self.angle = 0
        self.steering_output = 0
        self.serial_port = serial.Serial('/dev/cu.usbmodem142303', 115200)  # Adjust baudrate as per your requirement
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
        painter.setBrush(QColor(0, 70, 70))
        painter.drawEllipse(outer_track_x, outer_track_y, outer_track_width, outer_track_height)
        painter.setBrush(QColor(255, 255, 255))
        painter.drawEllipse(inner_track_x, inner_track_y, inner_track_width, inner_track_height)
        painter.setBrush(QColor(255, 0, 0))

        transformed_kart_image = kart_image.transformed(QTransform().rotate(self.steering_output*(180/np.pi) + 90))

        qrect_obj = QRectF(int(self.pos_x) - (kart_size/2), int(self.pos_y) - (kart_size/2), kart_size, kart_size)


        center = qrect_obj.center()
        transform_for_rect = QTransform().translate(center.x(), center.y()).rotate(self.steering_output*(180/np.pi) + 90).translate(-center.x(), -center.y())

        rotated_rect = transform_for_rect.mapRect(qrect_obj)

        painter.drawImage(rotated_rect, transformed_kart_image)
        # painter.drawLine(int(self.pos_x) + int(30 * np.cos(self.steering_output)),
        #                  int(self.pos_y) + int(30 * np.sin(self.steering_output)), 
        #                  int(self.pos_x), int(self.pos_y))
        

    @pyqtSlot(str)
    def update_steering(self, controller_input):
        try:
            # Map the value to the position on the screen
            self.delta_angle = float(controller_input.split(",")[0])
            self.accelerator = int(controller_input.split(",")[1])
            if (self.accelerator == 1):
                self.angle = self.delta_angle + self.angle
                self.steering_output = self.steering_output + self.angle / 10
        except ValueError:
            print("Invalid data received from serial port:", controller_input)

    def update_position(self):

        if (self.accelerator == 1):
            self.pos_x = self.pos_x + 3 * np.cos(self.steering_output)
            self.pos_y = self.pos_y + 3 * np.sin(self.steering_output)

        if(check_collided_outer(self.pos_x, self.pos_y) or check_collided_inner(self.pos_x, self.pos_y)):
            self.pos_x = 400
            self.pos_y = 500

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DotWidget()
    window.showMaximized()
    sys.exit(app.exec_())