import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import QTimer
import serial
import numpy as np

def process_steering_data(serial_port):
    line = serial_port.readline().decode("utf-8").strip()
    steering_angle = 0
    if(line):
        data = (line.split(","))
        steering_angle_unprocessed = float(data[1])

        if(100*np.abs(steering_angle_unprocessed) < 50):
            steering_angle = 0
        else:
            steering_angle = steering_angle_unprocessed

    return(steering_angle)
        

class DotWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 400, 200)
        self.dot_delta_x = 0
        self.dot_x = 500
        self.serial_port = serial.Serial('COM10', 115200)  # Adjust baudrate as per your requirement
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_position)
        self.timer.start(10)  # Update every 100 milliseconds

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(255, 0, 0))
        painter.drawEllipse(self.dot_x, 500, 20, 20)

    def update_position(self):
        while self.serial_port.in_waiting:
            data = process_steering_data(self.serial_port)
            try:
                value = int(data)
                # Map the value to the position on the screen
                self.dot_delta_x = value
                self.dot_x = self.dot_delta_x + self.dot_x
                self.update()  # Trigger repaint
            except ValueError:
                print("Invalid data received from serial port:", data)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DotWidget()
    window.show()
    sys.exit(app.exec_())