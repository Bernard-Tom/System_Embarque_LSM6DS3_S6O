# INTERFACE HOMME MACHINE / BERNARD TOM

# Lecture du port série et écriture dans un fichier CSV

import sys
import csv
import serial
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, QLabel, QPushButton

class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        #initialisation du port série
        def serial_init():
            ser = serial.Serial(
            port='/dev/ttyUSB0',\
            baudrate=9600,\
            parity=serial.PARITY_NONE,\
            stopbits=serial.STOPBITS_ONE,\
            bytesize=serial.EIGHTBITS,\
                timeout=0.05)
            print("port initialisé")
            return ser

        # Variables
        text_init = ("0")
        self.nb_data = 5
        self.database = [("")]*100
        self.ctn = 0
        self.ser = serial_init()

        # Label
        self.text = f'data: {text_init}'
        self.label = QLabel(self.text, self)

        # Boutton
        self.btn_start = QPushButton("Start")
        self.btn_clear = QPushButton("Clear DataBase")
        self.btn_start.clicked.connect(self.read_data)
        self.btn_clear.clicked.connect(self.clear_database)

        # Grid
        grid = QGridLayout()
        grid.addWidget(self.btn_start, 0, 0, Qt.AlignTop)
        grid.addWidget(self.btn_clear, 0, 1, Qt.AlignTop)
        grid.addWidget(self.label, 1, 0, Qt.AlignTop)
        self.setLayout(grid)

        # Window paramertes
        self.setGeometry(300, 300, 600, 300)
        self.setWindowTitle('EMB IHM')
        self.show()

    def clear_database(self):
        self.database = [("")]*100
        with open('data_base.csv',mode='w') as data_base:
            data_base_writer = csv.writer(data_base)
            data_base_writer.writerow("")
        self.ctn = 0

    def read_data(self):
            if (self.ser.in_waiting > 0):
                string = self.ser.readline()
                self.data = (string.decode('Ascii'))
                print(self.data)
                text = f'data: {self.data}'
                self.label.setText(text)
                self.database[self.ctn] = self.data
                self.send_csv(self.database)
                self.ctn = self.ctn +1
                 
    def send_csv(self,data):
        with open('data_base.csv',mode='w') as data_base:
            data_base_writer = csv.writer(data_base,delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL)
            data_base_writer.writerow(data)

def main():
    app = QApplication(sys.argv)
    w = Window()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()