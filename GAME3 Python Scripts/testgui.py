import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import QTimer, QObject, pyqtSignal, pyqtSlot
import serial
import numpy as np
import threading

steering_sensitivity = 200

def process_steering_data(serial_port):
    line = serial_port.readline().decode("utf-8").strip()
    steering_angle = 0
    if line:
        data = line.split(",")
        steering_angle = float(data[2])  # Angle

    return -steering_angle / steering_sensitivity

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

class DotWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 400, 200)
        self.delta_angle = 0
        self.pos_x = 200
        self.pos_y = 500
        self.angle = 0
        self.steering_output = 0
        self.serial_port = serial.Serial('COM10', 115200)  # Adjust baudrate as per your requirement
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
        painter.setBrush(QColor(255, 0, 0))
        painter.drawEllipse(int(self.pos_x) - 10, int(self.pos_y) - 10, 20, 20)
        painter.drawLine(int(self.pos_x) + int(30 * np.cos(self.steering_output)),
                         int(self.pos_y) + int(30 * np.sin(self.steering_output)), int(self.pos_x), int(self.pos_y))

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