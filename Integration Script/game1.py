import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QSlider, QLabel, QDial
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QPointF
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QConicalGradient
from PyQt5.QtGui import QPixmap

import struct
import serial
import time
import math
from enum import Enum



class ColorfulDial(QDial):
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
    data_received = pyqtSignal(int, int, int)
    color_change = pyqtSignal(bool)

    def __init__(self, port, baud_rate=9600, timeout=1):
        super().__init__()
        self.port = port
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.game_num = 0
        self.time_last = 3
        self.p1_score = 0
        self.p2_score = 0

        self.end_condition = False



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

                    value1 = int(value[0])
                    value2 = int(value[1])

                    if((self.game_num == 3) and (self.time_last == (16))):
                        ser.close()

                    time_current = int(value[2])

                    # The purpose of this is to reset the time_last to some other value
                    if (time_current != 0):
                        if (self.time_last < (16)):
                            self.time_last = time_current
                            self.p1_score = value1
                            self.p2_score = value2
                    
                    # The purpose of this is to check whether the time_current is equal to zero and the time_last != 0
                    if ((time_current == 0) and (self.time_last != 0)):
                        self.game_num+=1
                        print("Game Number: " + str(self.game_num))
                        self.time_last = time_current
                        self.end_condition = True
                    
                    # print(f"Pot1: {value1}, Pot2: {value2}, time {time_current}\n")

                    #print(value)
                    # self.slider2.setValue(value)



                    #self.data_received.emit(value1, value2)

                    #worked
                    self.data_received.emit(value1, value2, time_current)
                    # worked

                except Exception as e:
                    #e
                    print("Error time", e)
        except Exception as e:
                    #e
                    print("Serial port error", e)



class GameWindow(QWidget):
    submitted = pyqtSignal(str)
    def __init__(self, argument):
        super().__init__()
        self.showFullScreen()
        self.layout = QVBoxLayout(self)

        # self.button = QPushButton('Change Values', self)
        # self.button.clicked.connect(self.update_values)
        # self.button.setMinimumHeight(50) 
        # self.layout.addWidget(self.button)

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
        self.players = argument.split("               ")
        self.players_permanent = self.players.copy()

        self.dial3 = ColorfulDial(self)
        self.dial3.setRange(0, 12)
        self.dial3.setFixedSize(200,200)

        self.image_label = QLabel()

        self.image_dial_lay = QHBoxLayout()

        # worked
        self.time_and_dial = QVBoxLayout()
        # worked

        pixmap = QPixmap("resources/ThePriceIsRight.png")
        scaled_pixmap = pixmap.scaled(5000,5000)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setPixmap(pixmap)
        # self.layout.addWidget(self.image_label)

        #worked
        self.time_curr = QLabel('', self) 
        self.time_curr.setStyleSheet("QLabel{font-size: 45pt;}")
        self.time_curr.setAlignment(Qt.AlignCenter)
        self.time_and_dial.addWidget(self.dial3)
        self.time_and_dial.addWidget(self.time_curr)
        self.image_dial_lay.addLayout(self.time_and_dial)
        #worked 
        
        # self.image_dial_lay.addWidget(self.dial3)
        # worked
        self.image_dial_lay.addWidget(self.image_label)
        self.layout.addLayout(self.image_dial_lay)

        
        
        self.time_current = QLabel("Time: ", self)
        self.layout.addWidget(self.time_current)
        self.time_current.setStyleSheet("QLabel{font-size: 60pt;}") 
        self.time_current.setAlignment(Qt.AlignCenter)

        # slider1 + dial
        # self.dial1 = ColorfulDial(self)
        # self.dial1.setRange(0, 12)
        # self.dial1.setFixedSize(100,100)


        self.slider_setup = QHBoxLayout()

        self.layout_dial_and_label1 = QHBoxLayout()

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
        # self.layout_dial_and_label1.addWidget(self.dial1)
        
        
        self.slider_setup1.addLayout(self.layout_dial_and_label1)
        self.slider_setup.addLayout(self.slider_setup1)
        
        
        

        # slider2 + Dial
        # self.dial2 = ColorfulDial(self)
        # self.dial2.setRange(0, 12)
        # self.dial2.setFixedSize(100,100)


        self.slider_setup2 = QVBoxLayout()

        self.layout_dial_and_label2 = QHBoxLayout()

        self.slider2 = QSlider(Qt.Horizontal, self)
        self.slider2.setRange(150, 3650)
        self.slider2.setMinimumHeight(50)  # Set the slider's minimum height
        self.slider_setup2.addWidget(self.slider2)
        self.slider2.setStyleSheet(slider_style)  # Set the slider's style 
        self.pot_val_2_label = QLabel('', self) 
        self.pot_val_2_label.setStyleSheet("QLabel{font-size: 40pt;}") 
        self.pot_val_2_label.setAlignment(Qt.AlignCenter)

        self.layout_dial_and_label2.addWidget(self.pot_val_2_label)
        # self.layout_dial_and_label2.addWidget(self.dial2)

        self.slider_setup2.addLayout(self.layout_dial_and_label2)
        self.slider_setup.addLayout(self.slider_setup2)


        self.slider_setup.setSpacing(75)

        self.layout.addLayout(self.slider_setup)

        # End of slider stuff



        self.setWindowTitle("Dials and Sliders")
        self.setGeometry(100, 100, 800, 600)  # Change the window size on startup


        # worked 

        # self.dials_layout = QHBoxLayout()
        # self.layout.addLayout(self.dials_layout)

        # self.dial1 = ColorfulDial(self)
        # self.dial1.setRange(0, 12)
        # self.dial1.setFixedSize(100,100)
        # self.layout.addWidget(self.dial1)
        
        # worked

        

        # worked
        



        # Labels for the price for each potentiometer


        # worked
        self.winning_str = ""
        self.final_loser = ""

        self.can_calculate_winner = True

        #self.setCentralWidget(self)

        # self.start_serial_reading('COM9')
        self.start_serial_reading('/dev/tty.usbmodem2103')


    def calculate_winner(self):
        current_price = 0

        if (self.serial_reader.game_num == 1):
            current_price = 1899
        elif (self.serial_reader.game_num == 2):
            current_price = 2100
        else:
            current_price = 450
        

        abs_1_score = abs(current_price - self.serial_reader.p1_score)
        abs_2_score = abs(current_price - self.serial_reader.p2_score)

        condition1 = (self.serial_reader.game_num > 0) and (self.serial_reader.game_num < 4)
        condition2 = self.serial_reader.end_condition and self.can_calculate_winner
        print(self.players)
        
        if (abs_1_score > abs_2_score) and (condition2):
            self.serial_reader.end_condition = False

            if (condition2 == False):
                return 2, self.winning_str
                
            if (self.serial_reader.game_num == 1):
                self.players.remove(self.players_permanent[0])
                self.winning_str = self.players_permanent[0]
            elif (self.serial_reader.game_num == 2):
                self.players.remove(self.players_permanent[2])
                self.winning_str = self.players_permanent[2]
            elif (self.serial_reader.game_num == 3):
                self.final_loser = self.players_permanent[1]
                self.winning_str = self.players_permanent[0]
                self.players.remove(self.players_permanent[0])
                
            return 2, self.winning_str
        # worked
        if(abs_1_score == abs_2_score):
            return 3, "Undecided."
        self.serial_reader.end_condition = False

        if (condition2 == False):
                return 1, self.winning_str
                
        
        if (self.serial_reader.game_num == 1):
            self.players.remove(self.players_permanent[1])
            self.winning_str = self.players_permanent[1]
        elif (self.serial_reader.game_num == 2):
            self.players.remove(self.players_permanent[3])
            self.winning_str = self.players_permanent[3]
        elif (self.serial_reader.game_num == 3):
            self.final_loser = self.players[0]
            self.winning_str = self.players_permanent[1]
            self.players.remove(self.players[1])
            
            # for elem in self.players:
            #     if ((elem == "P2") or (elem == "P4")):
            #         self.players.remove(elem)
            #         break
        
        #worked
        return 1, self.winning_str


    

    def update_values(self, new_value1, new_value2, time_t):
        

        if (time_t <= (16)):
            self.slider2.setValue(new_value1)
            self.slider1.setValue(new_value2)

        if (time_t <= (16)):
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

        # self.dial2.setValue(time_t)

        #worked
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

        if (time_t <= (16)):
            self.pot_val_2_label.setText(f"{P2_current}\n$ {str(new_value1)}")
            self.pot_val_1_label.setText(f"{P1_current}\n$ {str(new_value2)}")
        # https://www.facebook.com/marketplace/item/1553942341838619/?ref=search&referral_code=null&referral_story_type=post
        if (self.serial_reader.game_num == 1):
            self.image_label.setPixmap(QPixmap("resources/chair.png"))
        elif (self.serial_reader.game_num == 2):
            self.image_label.setPixmap(QPixmap("resources/art.png"))
            self.no_verdict = False
        elif (self.serial_reader.game_num == 3):
            self.image_label.setPixmap(QPixmap("resources/room.png"))

        if (self.serial_reader.time_last == (16)):
            winner = self.calculate_winner()
            #worked
            if(self.serial_reader.game_num == 4):
                
                self.time_current.setText(f"Loser: {str(self.players[1])}")
            # worked
            else:
                if (self.serial_reader.game_num == 3):
                    self.time_current.setText(f"Winner {winner[1]}\n{self.final_loser} is ELIMINATED!\n")
                    print(f"FINAL LOSER: {self.final_loser}")
                    self.submitted.emit(self.final_loser)
                    #self.serial_reader.ser.close()
                    self.close()
                else:
                    self.time_current.setText(f"Winner {winner[1]}")
        else:
            if (self.serial_reader.game_num == 0):
                self.time_current.setText(f"START")
                return
            self.time_current.setText(f"GAME " + str(self.serial_reader.game_num))

    def start_serial_reading(self, port, baud_rate=115200, timeout=1):
        self.serial_reader = SerialReader(port, baud_rate, timeout)
        self.serial_reader.data_received.connect(self.update_values)
        self.serial_reader.start()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = GameWindow("               ".join(["A","B","C","D"]))
    main_win.show()

    sys.exit(app.exec_())