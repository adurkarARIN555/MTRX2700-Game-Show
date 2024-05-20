# Import relevant libraries and modules
import sys
import cv2
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, pyqtSignal

class WebcamApp(QWidget):
    submitted = pyqtSignal()                                                                             # Used for syncing the integrations windows

    def __init__(self, argument):
        super().__init__()
        self.player_name = argument
        self.initUI()                                                                                     # Initialise the user interface
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)                                                     # Open the default camera
        self.timer = QTimer(self)                                                                         # Creating a timer to change the frame on
        self.timer.timeout.connect(self.update_frame)                                                     # Connects the timer to the frame of the interface
        self.timer.start(100)                                                                             # Starts the timer. triggering and update of the frame every 100 ms

    def initUI(self):
        # User-clickable button, that once pressed, will take a photo of the current frame of the webcam
        self.image_label = QLabel(self)
        self.capture_button = QPushButton('Capture', self)
        self.capture_button.clicked.connect(self.capture_photo)
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        vbox.addWidget(self.capture_button)

        # Sets a spot for the webcam feed on the UI
        self.setLayout(vbox)
        self.setWindowTitle('Webcam Photo Capture')
        self.setGeometry(100, 100, 800, 600)
        
    def update_frame(self):
        ret, frame = self.cap.read() 
        
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)                                                 # Converts to RGB
            height, width, channel = frame.shape                                                           # Gets the dimensions of the frame
            step = channel * width
            qimg = QImage(frame.data, width, height, step, QImage.Format_RGB888)                           # Creates an image for the GUI
            self.image_label.setPixmap(QPixmap.fromImage(qimg))                                            # Displays image
            
    def capture_photo(self):
        ret, frame = self.cap.read()
        
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)                                                 # Converts to RGB
            height, width, channel = frame.shape                                                           # Gets the dimensions of the frame
            step = channel * width
            qimg = QImage(frame.data, width, height, step, QImage.Format_RGB888)                           # Creates an image for the GUI
            pixmap = QPixmap.fromImage(qimg)                                                               # Converts the image to a pixmap
            self.image_label.setPixmap(pixmap)                                                             # Displays image
            cv2.imwrite("User Images/"+self.player_name+".png", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))    # Captures the current frame of the webcam
            print('Photo captured and saved in User Images folder')

            self.submitted.emit()                                                                          # Ensures the integration windows are synchronised
            self.cap.release()                                                                             # Closes the webcam
            self.close()                                                                                   # Closes the webcam window

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WebcamApp()                                                                                       # Create a webcam for each player
    ex.show()                                                                                              # Display the application window
    sys.exit(app.exec_())
