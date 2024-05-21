import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QSlider, QLabel, QDial, QDesktopWidget
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QPointF
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QConicalGradient
from PyQt5.QtGui import QPixmap

import struct
import serial
import time
import math
from enum import Enum

# These are the variables that are used repeatedly throughout the game
end_game_timer = 16
invalid_time = 0
game_one_start = 1
game_two_start = 2
game_three_start = 3

class ColorfulDial(QDial):
    """
    A class to 

    Attributes:

        port: str
        baud_rate: float
        timeout: float
        game_num: float
        p1_score: int
        p2_score: int
        end_condition: bool

    Methods:

        process_message(message, banned_words)
        calculate_personality_score()
        final_personality_score(original_score)
    """
    def __init__(self, parent=None):
        super().__init__(parent)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        groove_rect = self.rect().adjusted(10, 10, -10, -10)
        groove_color = QColor(200, 200, 200)
        painter.setPen(QPen(groove_color, 4))
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(groove_rect)

        value_angle = (self.value() - self.minimum()) / (self.maximum() - self.minimum()) * 270 - 135
        gradient = QConicalGradient(self.rect().center(), value_angle - 90)
        gradient.setColorAt(0, QColor(255, 0, 0))
        gradient.setColorAt(1, QColor(0, 0, 255))
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(gradient))

        handle_radius = (groove_rect.width() - 10) / 2
        arrow_size = handle_radius / 2
        painter.translate(self.rect().center())
        painter.rotate(value_angle)

        arrow_points = [
            QPointF(-arrow_size / 2, -handle_radius + arrow_size),
            QPointF(arrow_size / 2, -handle_radius + arrow_size),
            QPointF(0, -handle_radius),
        ]
        painter.drawPolygon(*arrow_points)

        painter.end()

class SerialReader(QThread):
    """
    A class to read in serial data.

    Attributes:

        port: str
        baud_rate: float
        timeout: float
        game_num: float
        p1_score: int
        p2_score: int
        end_condition: bool

    Methods:
        __init__(message, port, baud_rate=9600, timeout=1)
        run()
    """
    data_received = pyqtSignal(int, int, int)
    color_change = pyqtSignal(bool)

    def __init__(self, port, baud_rate=9600, timeout=1):
        """
        Input:

        port: str
            Port being used to transmit serial data.
        baud_rate: int
            The baud_rate being used.
        timeout: 
            The timeout
        """
        super().__init__()
        self.port = port
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.game_num = 0
        self.time_last = 3
        self.p1_score = 0 # The score for player 1
        self.p2_score = 0 # The score for player 2
        self.end_condition = False # the end condition 

    def run(self):
        start = 0
        
        try:
            ser = serial.Serial(self.port, self.baud_rate, timeout=self.timeout)
            last_value = 0
            
            while True:
                value = ser.readline()
                try:
                    
                    value = value.decode('utf-8')
                    value = value.strip()
                    
                    value = value.split(',')

                    value1 = int(value[0]) # Get the first soft pot value
                    value2 = int(value[1]) # Get the second soft pot value

                    if((self.game_num == 3) and (self.time_last == (end_game_timer))):
                        ser.close()

                    time_current = int(value[2])

                    # The purpose of this is to reset the time_last to some other value
                    if (time_current != invalid_time):
                        if (self.time_last < (end_game_timer)):
                            self.time_last = time_current
                            self.p1_score = value1
                            self.p2_score = value2
                    
                    # The purpose of this is to check whether the time_current is equal to zero and the time_last != 0
                    if ((time_current == invalid_time) and (self.time_last != invalid_time)):
                        self.game_num += 1
                        print("Game Number: " + str(self.game_num))
                        self.time_last = time_current
                        self.end_condition = True

                    self.data_received.emit(value1, value2, time_current)
                except Exception as e:
                    print("Error time", e)
        except Exception as e:
                    print("Serial port error", e)

class GameWindow(QWidget):
    """
    A class to hold a subwindow.

    Attributes:

        argument: list
        width: int
        height: int
        players = list
        players_permanent = list
        dial3 = Qwidget
        image_label = QLabel
        image_dial_lay = QHBoxLayout
        time_and_dial = QVBoxLayout
        pixmap = QPixmap
        time_curr = QLabel
        image_dial_lay = QVBoxLayout
        time_current = QLabel
        slider_setup = QHBoxLayout
        layout_dial_and_label1 = QHBoxLayout
        slider_setup1 = QVBoxLayout
        slider1 = QSlider   
        pot_val_1_label = QLabel
        slider_setup2 = QVBoxLayout
        layout_dial_and_label2 = QHBoxLayout
        slider2 = QSlider
        pot_val_2_label = QLabel
        winning_str = str
        final_loser = str
        actual_price = str
        can_calculate_winner = Bool

    Methods:

        calculate_winner(message, banned_words)
        __init__(argument, width, height)
        update_values(new_value1, new_value2, time_t)
        start_serial_reading(port, baud_rate=115200, timeout=1):
    """
    submitted = pyqtSignal(str)
    def __init__(self, argument, width, height):
        """
        Input:

        argument: list
            List of players that are being passed from the mainwindow
        width: int
            The current size of the window
        height: int
            The current height of the window being used
        """
        super().__init__()

        self.showFullScreen()
        self.layout = QVBoxLayout(self)
        
        self.setFixedWidth(width)
        self.setFixedHeight(height)

        slider_style = '''
        QSlider::groove:horizontal {
            border: 1px solid #999999;
            height: 40px;
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #B1B1B1, stop:1 #c4c4c4);
            margin: 2px 0;
        }
        QSlider::handle:horizontal {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4444FF, stop:1 #6666FF);
            border: 1px solid #7777FF;
            width: 20px;
            margin: -2px 0;
            border-radius: 3px;
        }

        '''
        # This is the argument player list that is split thats originally taken from the main window
        self.players = argument.split("               ")
        self.players_permanent = self.players.copy() # This list is used to delete players without getting index errors

        # Create colorful dial to be used for count down timer
        self.dial3 = ColorfulDial(self)
        self.dial3.setRange(0, 12)
        self.dial3.setFixedSize(200,200)

        self.image_label = QLabel() # Create image label for alternating images

        self.image_dial_lay = QHBoxLayout()

        self.time_and_dial = QVBoxLayout()

        pixmap = QPixmap("resources/ThePriceIsRight.png")
        scaled_pixmap = pixmap.scaled(5000,5000)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setPixmap(pixmap)

        # Create a layout for the timer and timer label
        self.time_curr = QLabel('', self) 
        self.time_curr.setStyleSheet("QLabel{font-size: 45pt;}")
        self.time_curr.setAlignment(Qt.AlignCenter)
        self.time_and_dial.addWidget(self.dial3)
        self.time_and_dial.addWidget(self.time_curr)
        self.image_dial_lay.addLayout(self.time_and_dial)
        
        self.image_dial_lay.addWidget(self.image_label)
        self.layout.addLayout(self.image_dial_lay)

        # This is for showing the current game round
        self.time_current = QLabel("Time: ", self)
        self.layout.addWidget(self.time_current)
        self.time_current.setStyleSheet("QLabel{font-size: 60pt;}") 
        self.time_current.setAlignment(Qt.AlignCenter)

        self.slider_setup = QHBoxLayout()

        self.layout_dial_and_label1 = QHBoxLayout()

        # Create the slider setup for the slider
        self.slider_setup1 = QVBoxLayout()
        self.slider1 = QSlider(Qt.Horizontal, self)
        self.slider1.setRange(150, 3650)
        self.slider1.setMinimumHeight(50)  # Set the slider's minimum height
        self.slider_setup1.addWidget(self.slider1)
        self.slider1.setStyleSheet(slider_style)  # Set the slider's style     
        self.pot_val_1_label = QLabel('', self)  
        self.pot_val_1_label.setStyleSheet("QLabel{font-size: 40pt;}")
        self.pot_val_1_label.setAlignment(Qt.AlignCenter)

        self.layout_dial_and_label1.addWidget(self.pot_val_1_label)
        
        self.slider_setup1.addLayout(self.layout_dial_and_label1)
        self.slider_setup.addLayout(self.slider_setup1)

        self.slider_setup2 = QVBoxLayout()

        self.layout_dial_and_label2 = QHBoxLayout()

        # Create the slider setup for the slider
        self.slider2 = QSlider(Qt.Horizontal, self)
        self.slider2.setRange(150, 3650)
        self.slider2.setMinimumHeight(50)  # Set the slider's minimum height
        self.slider_setup2.addWidget(self.slider2)
        self.slider2.setStyleSheet(slider_style)  # Set the slider's style 
        self.pot_val_2_label = QLabel('', self) 
        self.pot_val_2_label.setStyleSheet("QLabel{font-size: 40pt;}") 
        self.pot_val_2_label.setAlignment(Qt.AlignCenter)

        self.layout_dial_and_label2.addWidget(self.pot_val_2_label)

        self.slider_setup2.addLayout(self.layout_dial_and_label2)
        self.slider_setup.addLayout(self.slider_setup2)

        self.slider_setup.setSpacing(75)

        self.layout.addLayout(self.slider_setup)

        self.setWindowTitle("Dials and Sliders")
        self.setGeometry(100, 100, 800, 600)  # Change the window size on startup

        # These variables are here to keep the 
        self.winning_str = ""
        self.final_loser = ""
        self.actual_price = ""

        self.can_calculate_winner = True

        # self.start_serial_reading('COM9')
        self.start_serial_reading('/dev/tty.usbmodem2103')


    def calculate_winner(self):
        """
        The purpose of this function is to calculate the final winner
        Output: Tuple
            This returns the 1,2 to tell whether the Left or Right slider has won. 
            This also returns the winning player name as taken from the mainwindow
        """
        current_price = 0

        if (self.serial_reader.game_num == game_one_start):
            current_price = 1899
        elif (self.serial_reader.game_num == 2):
            current_price = 2100
        else:
            current_price = 450
        self.actual_price = current_price
        
        abs_1_score = abs(current_price - self.serial_reader.p1_score)
        abs_2_score = abs(current_price - self.serial_reader.p2_score)

        condition1 = (self.serial_reader.game_num > 0) and (self.serial_reader.game_num < 4)
        condition2 = self.serial_reader.end_condition and self.can_calculate_winner
        print(self.players)
        
        # This is to check whether the winner is on the left hand slider and 
        # then appropriately increment the player
        if (abs_1_score > abs_2_score) and (condition2):
            self.serial_reader.end_condition = False

            if (condition2 == False):
                return 2, self.winning_str
                
            if (self.serial_reader.game_num == game_one_start):
                self.players.remove(self.players_permanent[0])
                self.winning_str = self.players_permanent[0]
            elif (self.serial_reader.game_num == game_two_start):
                self.players.remove(self.players_permanent[2])
                self.winning_str = self.players_permanent[2]
            elif (self.serial_reader.game_num == game_three_start):
                self.final_loser = self.players_permanent[1]
                self.winning_str = self.players_permanent[0]
                self.players.remove(self.players_permanent[0])
                
            return 2, self.winning_str
        if(abs_1_score == abs_2_score):
            return 3, "Undecided."
        self.serial_reader.end_condition = False

        if (condition2 == False):
                return 1, self.winning_str
                
        # This is to check whether the winner is on the right hand slider and 
        # then appropriately increment the player
        if (self.serial_reader.game_num == game_one_start):
            self.players.remove(self.players_permanent[1])
            self.winning_str = self.players_permanent[1]
        elif (self.serial_reader.game_num == game_two_start):
            self.players.remove(self.players_permanent[3])
            self.winning_str = self.players_permanent[3]
        elif (self.serial_reader.game_num == game_three_start):
            self.final_loser = self.players[0]
            self.winning_str = self.players_permanent[1]
            self.players.remove(self.players[1])
        return 1, self.winning_str

    def update_values(self, new_value1, new_value2, time_t):
        """
        The purpose of this function is to update the values of the winner
        Input:
            new_value1: int
                This is the first potentiometer value
            new_value2: int
                This is the second potentiometer value
            time_t: int
                This is the current time
        Output: Tuple
            This returns the 1,2 to tell whether the Left or Right slider has won. 
            This also returns the winning player name as taken from the mainwindow
        """
        # The purpose of this is to only set 
        if (time_t <= (end_game_timer)):
            self.slider2.setValue(new_value1)
            self.slider1.setValue(new_value2)

        # The purpose of this is to give the player a few seconds to take in the image
        if (time_t <= (end_game_timer)):
            if (time_t == 0):
                self.time_curr.setText("Game Start in 3...")
            elif (time_t == 1):
                self.time_curr.setText("Game Start in 2...")
            elif (time_t == 2):
                self.time_curr.setText("Game Start in 1...")
            elif (time_t == 3):
                self.time_curr.setText(f"Round {self.serial_reader.game_num} started!")

            else:
                self.time_curr.setText(f"{str(time_t-4)}")
                self.dial3.setValue(time_t-4)

        # This goes to different conditions to provide feedback for the player
        P1_current = ""
        P2_current = ""
        if (self.serial_reader.game_num == 1):
            P1_current = self.players_permanent[0]
            P2_current = self.players_permanent[1]
        elif(self.serial_reader.game_num == 2):
            P1_current = self.players_permanent[2]
            P2_current = self.players_permanent[3]
        elif (self.serial_reader.game_num == 3):
            if (self.serial_reader.end_condition):
                P1_current = self.players[0]
                P2_current = self.players[1]
        if (time_t <= (end_game_timer)):
            self.pot_val_2_label.setText(f"{P2_current}\n$ {str(new_value1)}")
            self.pot_val_1_label.setText(f"{P1_current}\n$ {str(new_value2)}")

        # Conditions to change the images 
        if (self.serial_reader.game_num == 1):
            self.image_label.setPixmap(QPixmap("resources/chair.png"))
        elif (self.serial_reader.game_num == 2):
            self.image_label.setPixmap(QPixmap("resources/art.png"))
            self.no_verdict = False
        elif (self.serial_reader.game_num == 3):
            self.image_label.setPixmap(QPixmap("resources/room.png"))

        # The purpose of the following conditions is change the final loser and winner
        if (self.serial_reader.time_last == (end_game_timer)):
            print(f"FINAL LOSER: {self.final_loser}")

            winner = self.calculate_winner()
            if(self.serial_reader.game_num == 4):
                self.time_current.setText(f"Loser: {str(self.players[1])}")
            else:
                if (self.serial_reader.game_num == 3):
                    self.time_current.setText(f"Winner {winner[1]}\n{self.final_loser} is ELIMINATED!\n")
                    print(f"FINAL LOSER: {self.final_loser}")
                    self.submitted.emit(self.final_loser)
                    self.close()
                else:
                    self.time_current.setText(f"Winner {winner[1]}\nActual Price: ${self.actual_price}")
                    
        else:
            if (self.serial_reader.game_num == 0):
                self.time_current.setText(f"START")
                return
            self.time_current.setText(f"GAME " + str(self.serial_reader.game_num))
    
    def start_serial_reading(self, port, baud_rate=115200, timeout=1):
        """
        Input:
            port: SerialPort
                This is the serial port that is being read from
            baud_rate: int
                This is the current baud_rate
            time_out: int
                This is the timeout value
        """
        # The purpose of this is to connect the update values function with the serial reader
        self.serial_reader = SerialReader(port, baud_rate, timeout)
        self.serial_reader.data_received.connect(self.update_values)
        self.serial_reader.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    desktop = QApplication.desktop()
    screen_geom = desktop.screenGeometry()
    width = screen_geom.width()
    height = screen_geom.height()
    main_win = GameWindow("               ".join(["A","B","C","D"]), width, height)
    main_win.showMaximized()

    sys.exit(app.exec_())