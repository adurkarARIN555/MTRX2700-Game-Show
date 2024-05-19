import sys
import cv2
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, pyqtSignal

class WebcamApp(QWidget):
    submitted = pyqtSignal()

    def __init__(self, argument):
        super().__init__()
        self.player_name = argument
        self.initUI()
        self.cap = cv2.VideoCapture(0)  # Open the default camera
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Update the frame every 30 ms

    def initUI(self):
        self.image_label = QLabel(self)
        self.capture_button = QPushButton('Capture', self)
        self.capture_button.clicked.connect(self.capture_photo)
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        vbox.addWidget(self.capture_button)
        
        self.setLayout(vbox)
        self.setWindowTitle('Webcam Photo Capture')
        self.setGeometry(100, 100, 800, 600)
        
    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            step = channel * width
            qimg = QImage(frame.data, width, height, step, QImage.Format_RGB888)
            self.image_label.setPixmap(QPixmap.fromImage(qimg))
            
    def capture_photo(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            step = channel * width
            qimg = QImage(frame.data, width, height, step, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qimg)
            self.image_label.setPixmap(pixmap)
            cv2.imwrite("User Images/"+self.player_name+".png", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            print('Photo captured and saved as captured_photo.png')

            self.submitted.emit()
            self.close()

    # def closeEvent(self, event):
    #     self.cap.release()
    #     event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WebcamApp()
    ex.show()
    sys.exit(app.exec_())
