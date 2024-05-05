import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor, QImage, QTransform
from PyQt5.QtCore import QTimer, QObject, pyqtSignal, pyqtSlot, QRect
import serial
import numpy as np
import threading
import os

steering_sensitivity = 200

def process_steering_data(serial_port):
    line = serial_port.readline().decode("utf-8").strip()
    steering_angle = 0
    if line:
        data = line.split(",")
        steering_angle = float(data[2])  # Angle

    return -steering_angle / steering_sensitivity

def scaling_factor(theta):
    #factor = np.abs(np.sin(theta))+np.abs(np.cos(theta))
    factor = np.sin(4*(theta-(np.pi/8))) + 2
    return(factor)

class SerialReader(QObject):
    data_received = pyqtSignal(float)

    def __init__(self, serial_port):
        super().__init__()
        self.serial_port = serial_port
        self.running = True

    def run(self):
        while self.running:
            if self.serial_port.in_waiting:
                steering_angle = process_steering_data(self.serial_port)
                self.data_received.emit(steering_angle)

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
        self.pos_x = 200
        self.pos_y = 500
        self.angle = 0
        self.steering_output = 0
        self.serial_port = serial.Serial('/dev/cu.usbmodem1421303', 115200)  # Adjust baudrate as per your requirement
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
        painter.drawEllipse(200, 75, 1000, 625)
        painter.setBrush(QColor(255, 255, 255))
        painter.drawEllipse(350, 220, 700, 325)
        painter.setBrush(QColor(255, 0, 0))
        transformed_kart_image = kart_image.transformed(QTransform().rotate(self.steering_output*(180/np.pi) + 90))
        #scale_factor = scaling_factor(self.steering_output)
        #transformed_scaled_kart_image = transformed_kart_image.transformed(QTransform().scale(scale_factor, scale_factor))
        #painter.drawImage(QRect(int(self.pos_x) - 50, int(self.pos_y) - 50, int(60 + 15*scale_factor), int(60 + 15*scale_factor)), transformed_kart_image)
        painter.drawImage(QRect(int(self.pos_x) - 50, int(self.pos_y) - 50, 100, 100), transformed_kart_image)
        painter.drawLine(int(self.pos_x) + int(30 * np.cos(self.steering_output)),
                         int(self.pos_y) + int(30 * np.sin(self.steering_output)), 
                         int(self.pos_x), int(self.pos_y))
        

    @pyqtSlot(float)
    def update_steering(self, steering_angle):
        try:
            value = steering_angle
            # Map the value to the position on the screen
            self.delta_angle = value
            self.angle = self.delta_angle + self.angle
            self.steering_output = self.steering_output + self.angle / 10
        except ValueError:
            print("Invalid data received from serial port:", steering_angle)

    def update_position(self):
        self.pos_x = self.pos_x + 2.5 * np.cos(self.steering_output)
        self.pos_y = self.pos_y + 2.5 * np.sin(self.steering_output)
        self.update()  # Trigger repaint

    def closeEvent(self, event):
        self.serial_reader.stop()
        self.serial_thread.join()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DotWidget()
    window.showMaximized()
    sys.exit(app.exec_())