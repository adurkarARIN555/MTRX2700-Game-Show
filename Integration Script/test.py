import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('QLineEdit Example')

        # Create a QLineEdit instance
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setGeometry(10, 10, 200, 30)  # (x, y, width, height)
        self.lineEdit.returnPressed.connect(self.on_enter_pressed)

    def on_enter_pressed(self):
        # Retrieve text from QLineEdit when Enter key is pressed
        text = self.lineEdit.text()
        print("Text entered:", text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.setGeometry(100, 100, 220, 50)  # (x, y, width, height)
    widget.show()
    sys.exit(app.exec_())
