import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import QTimer
import serial
import numpy as np

steering_sensitivity = 162

def process_steering_data(serial_port):
    line = serial_port.readline().decode("utf-8").strip()
    steering_angle = 0
    if(line):
        data = (line.split(","))
        steering_angle_unprocessed = float(data[2]) # Angle

        if(100*np.abs(steering_angle_unprocessed) < 50):
            steering_angle = 0
        else:
            steering_angle = steering_angle_unprocessed

    return(-steering_angle/steering_sensitivity)
        

class DotWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 400, 200)
        self.delta_angle = 0
        self.pos_x = 50
        self.pos_y = 500
        self.angle = -np.pi/2
        self.serial_port = serial.Serial('/dev/cu.usbmodem142303', 115200)  # Adjust baudrate as per your requirement
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_position)
        self.timer.start(10)  # Update every 100 milliseconds
    

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(255, 0, 0))
        painter.drawEllipse(int(self.pos_x) - 10, int(self.pos_y) - 10, 20, 20)
        painter.drawLine(int(self.pos_x) + int(30*np.cos(self.angle)), int(self.pos_y) + int(30*np.sin(self.angle)), int(self.pos_x), int(self.pos_y))

    def update_position(self):
        while self.serial_port.in_waiting:
            steering_angle = process_steering_data(self.serial_port)
            try:
                value = steering_angle
                # Map the value to the position on the screen
                self.delta_angle = value
                self.angle = self.delta_angle + self.angle
                self.pos_x = self.pos_x + np.cos(self.angle)
                self.pos_y = self.pos_y + np.sin(self.angle)
                self.update()  # Trigger repaint
            except ValueError:
                print("Invalid data received from serial port:", steering_angle)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DotWidget()
    window.show()
    sys.exit(app.exec_())