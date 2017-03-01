'''
This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import os
import sys
import time
import serial
from serial.tools import list_ports
import random
import numpy as np
from datetime import datetime as dt

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from PyQt5.QtQuick import QQuickView

import matplotlib.dates as md
from matplotlib import style

line = " "
draw = " "
serial_on = 0
LARGE_FONT = ("Verdana", 12)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.mdiArea = QMdiArea()
        self.mdiArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.setCentralWidget(self.mdiArea)

        self.create_actions()
        self.create_menu()
        self.create_toolbar()
        self.create_status_bar()

        self.setWindowTitle("Programmable optic sensor GUI 0.9.1")
        self.setWindowIcon(QIcon('icons/logo.png'))

    def closeEvent(self, event):
        quit_question = QMessageBox.question(self, "Confirm exit", "Exit application?",
                                             QMessageBox.Yes | QMessageBox.No)

        if quit_question == QMessageBox.Yes:
            event.accept()

        else:
            event.ignore()

    def create_menu(self):
        """MENU BAR"""
        menu_bar = self.menuBar()

        # File
        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(self.serial_port_act)
        file_menu.addAction(self.exit_act)

        # Tools
        tools_menu = menu_bar.addMenu('&Tools')
        tools_menu.addAction(self.config_act)
        tools_menu.addAction(self.calibrate_act)
        tools_menu.addAction(self.display_graph_act)
        tools_menu.addAction(self.log_plotter_act)
        tools_menu.addAction(self.log_editor_act)
        tools_menu.addAction(self.debug_act)

        # Help
        help_menu = menu_bar.addMenu('&About')
        help_menu.addAction(self.help_act)
        help_menu.addAction(self.about_qt_act)

    def create_toolbar(self):
        """TOOLBAR"""

        self.toolbar = self.addToolBar('Toolbar')

        self.toolbar.addAction(self.serial_port_act)
        self.toolbar.addAction(self.config_act)
        self.toolbar.addAction(self.calibrate_act)
        self.toolbar.addAction(self.display_graph_act)
        self.toolbar.addAction(self.debug_act)
        self.toolbar.addAction(self.exit_act)
        self.addToolBar(Qt.LeftToolBarArea, self.toolbar)

    def create_status_bar(self):
        self.statusBar().showMessage("Ready")

    def create_actions(self):
        # Icon made by[Freepik in technology] from www.flaticon.com
        self.serial_port_act = QAction(QIcon('icons/usb-connector.png'), '&Serial port', self)
        self.serial_port_act.setStatusTip('Serial port')
        self.serial_port_act.triggered.connect(self.config_serial)

        # Icon made by[Freepik in interface] from www.flaticon.com
        self.calibrate_act = QAction(QIcon('icons/calibration-mark.png'), '&Calibrate sensor', self)
        self.calibrate_act.setStatusTip('Calibrate sensor')
        self.calibrate_act.triggered.connect(self.calibrate_sensor)

        # Icon made by[Gregor Cresnar in Tools and utensils] from www.flaticon.com
        self.config_act = QAction(QIcon('icons/settings.png'), '&Config sensor', self)
        self.config_act.setShortcut('Ctrl+C')
        self.config_act.setStatusTip('Config sensor')
        self.config_act.triggered.connect(self.config_sensor)

        # Icon made by[Freepik in business] from www.flaticon.com
        self.display_graph_act = QAction(QIcon('icons/icon.png'), '&Display graph', self)
        self.display_graph_act.setStatusTip('Display graph')
        self.display_graph_act.triggered.connect(self.select_graph)

        # Icon made by[Freepik in interface] from www.flaticon.com
        self.log_plotter_act = QAction(QIcon('icons/log-file-format-draw.png'), '&Log plotter', self)
        self.log_plotter_act.setStatusTip('Log plotter')
        self.log_plotter_act.triggered.connect(self.log_plotter)

        # Icon made by[Freepik in interface] from www.flaticon.com
        self.log_editor_act = QAction(QIcon('icons/log-file-format-edit.png'), '&Log editor', self)
        self.log_editor_act.setStatusTip('Log plotter')
        self.log_editor_act.triggered.connect(self.log_editor)

        # Icon made by[Freepik in interface] from www.flaticon.com
        self.debug_act = QAction(QIcon('icons/debug.png'), '&Debug console', self)
        self.debug_act.setStatusTip('Debug console')
        self.debug_act.triggered.connect(self.debug)

        # Icon made by[Freepik in interface] from www.flaticon.com
        self.help_act = QAction(QIcon('icons/customer-service.png'), '&About', self)
        self.help_act.setShortcut('Ctrl+H')
        self.help_act.setStatusTip('About')
        self.help_act.triggered.connect(self.help)

        # Icon made from www.qt.io
        self.about_qt_act = QAction(QIcon('icons/Apps-Qt-icon.png'), '&About Qt', self)
        self.about_qt_act.setStatusTip('About Qt')
        self.about_qt_act.triggered.connect(self.about_qt)

        # Icon made by[Lucy G in signs] from www.flaticon.com
        self.exit_act = QAction(QIcon('icons/logout.png'), '&Exit', self)
        self.exit_act.setShortcut('Ctrl+x')
        self.exit_act.setStatusTip('Exit application')
        self.exit_act.triggered.connect(self.exit)

    def config_serial(self):
        self.config_ser = ConfigSerial()
        #self.mdiArea.addSubWindow(self.config_ser)
        self.config_ser.show()

    def config_sensor(self):
        self.config_sen = ConfigSensor()
        #self.mdiArea.addSubWindow(self.config_sen)

        self.config_sen.show()

    def calibrate_sensor(self):
        self.calibrate = CalibrateSensor()
        self.calibrate.show()

    def select_graph(self):
        self.select_graph = MplDrawGraph()
        self.mdiArea.addSubWindow(self.select_graph)
        self.select_graph.showMaximized()

    def log_plotter(self):
        self.log_plot = MplLogPlotter()
        self.mdiArea.addSubWindow(self.log_plot)
        self.log_plot.showMaximized()

    def log_editor(self):
        self.log_edit = MplLogEditor()
        self.mdiArea.addSubWindow(self.log_edit)
        self.log_edit.showMaximized()

    def debug(self):
        self.debugwindow = DebugWindow()
        self.mdiArea.addSubWindow(self.debugwindow)
        self.debugwindow.showMaximized()

    def help(self):
        text = "<qt>Programmable optic sensor GUI, is part of a thesis with a title:</qt><qt>Koncept programabilnega optičnega senzorja (The concept of </qt><qt> programmable optical sensor), from Andrej Zadnik of University of Ljubljana Faculty of Electrical Engineering.</qt><qt>Source code is located in github repository:</qt> <qt><a href = https://github.com/andrejzadnik/programmable-optic-sensor>\n https://github.com/andrejzadnik/programmable-optic-sensor-gui</a></qt>"        
        
        help_message = QMessageBox.information(self, 'About', text, QMessageBox.Ok)

    def about_qt(self):
        qt_message = QMessageBox.aboutQt(self)

    def exit(self, event):
        quit_question = QMessageBox.question(self, "Confirm exit", "Exit application?",
                                             QMessageBox.Yes | QMessageBox.No)

        if quit_question == QMessageBox.Yes:
            sys.exit()

'''
----------   Config Serial   ----------
'''


class ConfigSerial(QWidget):
    def __init__(self):
        super().__init__()

        self.init()
        self.show()

    def init(self):

        self.setGeometry(300, 300, 150, 120)
        self.setWindowTitle('Config serial port')

        available_ports = [port[0] for port in list_ports.comports()]

        '''
            **********QComboBox*****************
        '''
        combo = QComboBox(self)
        combo.addItem("")
        for i in range(0, len(available_ports)):
            combo.addItem(available_ports[i])

        # combo.AdjustToContents
        combo.move(110, 30)
        combo.resize(110, 20)
        combo.activated[str].connect(self.serial_port_select)

        '''
             **********Buttons*****************
        '''
        self.connectButton = QPushButton("Test connection")
        self.connectButton.clicked.connect(self.serial_button_colour)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.ok)

        hbox = QHBoxLayout()
        hbox.addStretch(1)

        hbox.addWidget(self.connectButton)
        hbox.addSpacing(100)
        hbox.addWidget(ok_button)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def ok(self):
        self.close()

    def serial_port_select(self, text):
        self.port = text

    def serial_button_colour(self):

        # self.connectButton.setStyleSheet("background-color: green")
        # sudo chmod 777 /dev/ttyUSB0

        #ser = serial.Serial(port, 9600)

        self.serial = serial.Serial(
            port=self.port,
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1)

        self.serial.write(b'IR_SW_INFO')

        #with serial.Serial(port, 9600, timeout=1) as ser:

        s = self.serial.read(10)  # read up to ten bytes (timeout)

        line = self.serial.readline()  # read a '\n' terminated line

        if line == b'le IR Switch Version: 0.9.0 2016\r\n':
            self.connectButton.setStyleSheet("background-color: green")

        elif line != b'le IR Switch Version: 0.9.0 2016\r\n':
            self.connectButton.setStyleSheet("background-color: red")

'''
----------  Config sensor window  ----------
'''


class ConfigSensor(QWidget):
    def __init__(self):
        super(ConfigSensor, self).__init__()
        self.serial_selected = 0
        self.out_type = 0 # 1: NC 2: NO
        self.pulse = 0 # 1: 10ms 2: random
        self.sensor_adc = 0 # 1: adc_ON 2: adc_OFF
        self.calibrate = 0 # ne izvedi kalibracije

        self.config_sensor(self)

    def closeEvent(self, event):
        self.config_exit()

    def config_sensor(self, ConfigSensor):
        ConfigSensor.resize(389, 322)
        ConfigSensor.move(600, 400)
        ConfigSensor.setWindowTitle("Config Sensor")

        self.buttonBox = QDialogButtonBox(ConfigSensor)
        self.buttonBox.setGeometry(QRect(200, 290, 166, 23))
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.comboBox = QComboBox(ConfigSensor)
        self.comboBox.setGeometry(QRect(170, 20, 116, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem(" ")

        available_ports = [port[0] for port in list_ports.comports()]

        for i in range(0, len(available_ports)):
            self.comboBox.addItem(available_ports[i])

        self.groupBox = QGroupBox(ConfigSensor)
        self.groupBox.setGeometry(QRect(20, 70, 167, 81))
        self.groupBox.setObjectName("groupBox")
        self.groupBox.setTitle("Sensor output type:")
        self.groupBox.setEnabled(False)

        self.radioButton = QRadioButton(self.groupBox)
        self.radioButton.setGeometry(QRect(10, 20, 171, 18))
        self.radioButton.setObjectName("radioButton")
        self.radioButton.setText("NC (normally closed)")

        self.radioButton_2 = QRadioButton(self.groupBox)
        self.radioButton_2.setGeometry(QRect(10, 50, 161, 18))
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_2.setText("NO (normally open)")

        self.groupBox_2 = QGroupBox(ConfigSensor)
        self.groupBox_2.setGeometry(QRect(195, 70, 171, 80))
        self.groupBox_2.setObjectName("groupBox_2")
        self.groupBox_2.setTitle("Generated pulse duration:")
        self.groupBox_2.setEnabled(False)

        self.radioButton_3 = QRadioButton(self.groupBox_2)
        self.radioButton_3.setGeometry(QRect(10, 20, 91, 18))
        self.radioButton_3.setObjectName("radioButton_3")
        self.radioButton_3.setText("10ms")

        self.radioButton_4 = QRadioButton(self.groupBox_2)
        self.radioButton_4.setGeometry(QRect(10, 50, 91, 18))
        self.radioButton_4.setObjectName("radioButton_4")
        self.radioButton_4.setText("random")

        self.groupBox_3 = QGroupBox(ConfigSensor)
        self.groupBox_3.setGeometry(QRect(20, 160, 167, 111))
        self.groupBox_3.setObjectName("groupBox_3")
        self.groupBox_3.setTitle("ADC pulse verification:")
        self.groupBox_3.setEnabled(False)

        self.radioButton_5 = QRadioButton(self.groupBox_3)
        self.radioButton_5.setGeometry(QRect(10, 20, 110, 18))
        self.radioButton_5.setObjectName("radioButton_5")
        self.radioButton_5.setText("ADC mode ON")

        self.radioButton_6 = QRadioButton(self.groupBox_3)
        self.radioButton_6.setGeometry(QRect(10, 50, 115, 18))
        self.radioButton_6.setObjectName("radioButton_6")
        self.radioButton_6.setText("ADC mode OFF")

        self.checkBox = QCheckBox(self.groupBox_3)
        self.checkBox.setGeometry(QRect(10, 80, 131, 18))
        self.checkBox.setObjectName("checkBox")
        self.checkBox.setText("Callibrate sensor")
        self.checkBox.setEnabled(False)

        self.label = QLabel(ConfigSensor)
        self.label.setGeometry(QRect(93, 20, 71, 20))
        font = QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label.setText("Serial port:")

        self.buttonBox.raise_()
        self.comboBox.raise_()
        self.groupBox.raise_()
        self.groupBox_2.raise_()
        self.groupBox_3.raise_()
        self.label.raise_()

        self.retranslateUi(ConfigSensor)
        QMetaObject.connectSlotsByName(ConfigSensor)

    def retranslateUi(self, ConfigSensor):
        self.comboBox.activated[str].connect(self.serial_port_select)

        self.radioButton.clicked.connect(self.sensor_nc)
        self.radioButton_2.clicked.connect(self.sensor_no)

        self.radioButton_3.clicked.connect(self.sensor_pulse)
        self.radioButton_4.clicked.connect(self.sensor_pulse_r)

        self.radioButton_5.clicked.connect(self.sensor_adc_on)
        self.radioButton_6.clicked.connect(self.sensor_adc_off)

        self.checkBox.stateChanged.connect(self.enable_calibrate)

        self.buttonBox.accepted.connect(self.sensor_programming)
        self.buttonBox.rejected.connect(self.config_exit)

    def serial_port_select(self, text):
        self.port = text

        if self.serial_selected == 1:
            self.ser.close()
            self.serial_selected = 0

        if text != " ":
            self.ser = serial.Serial(
                port=self.port,
                baudrate=9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1)

            self.serial_selected = 1

            self.groupBox.setEnabled(True)
            self.groupBox_2.setEnabled(True)
            self.groupBox_3.setEnabled(True)

        elif text == " ":
            self.groupBox.setEnabled(False)
            self.groupBox_2.setEnabled(False)
            self.groupBox_3.setEnabled(False)

    def sensor_nc(self):
        self.out_type = 1

    def sensor_no(self):
        self.out_type = 2

    def sensor_pulse(self):
        self.pulse = 1

    def sensor_pulse_r(self):
        self.pulse = 2

    def sensor_adc_on(self):
        self.sensor_adc = 1
        self.checkBox.setEnabled(True)

    def sensor_adc_off(self):
        self.sensor_adc = 2
        self.checkBox.setEnabled(False)

    def enable_calibrate(self):
        if self.calibrate == 1:
            self.calibrate = 0

        elif self.calibrate == 0:
            self.calibrate = 1

    def config_exit(self):
        if self.serial_selected == 1:
            self.ser.close()

        self.close()

    def error_programming(self):
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Critical)

        self.msg.setWindowTitle("Error message")
        self.msg.setText("Error while programming!")
        #self.msg.setDetailedText("feee")
        self.msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        self.msg.buttonClicked.connect(self.exit_msg)

    def compeate_programming(self):
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Information)

        self.msg.setWindowTitle("Message")
        self.msg.setText("programming finished with no errors!")

        self.msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        self.msg.buttonClicked.connect(self.exit_msg)

    def exit_msg(self):
        self.msg.close()

    def sensor_programming(self):
        error = 2

        if self.out_type == 1: # 1: NC 2: NO
            self.ser.write(b'SW_MODE_NC')
            s = self.ser.read(0)
            line = self.ser.readline()
            if line in (b'Izhod deljuje kot NC!\r\n',  b'Izhod ze deljuje kot NC.\r\n'):
                error = 0

            else:
                error = 1

        elif self.out_type == 2:  # 1: NC 2: NO
            self.ser.write(b'SW_MODE_NO')
            s = self.ser.read(0)
            line = self.ser.readline()
            if line in (b'Izhod deljuje kot NO!\r\n', b'Izhod ze deljuje kot NO.\r\n'):
                error = 0

            else:
                error = 1

        if self.pulse == 1:  # 1: 10ms 2: random
            self.ser.write(b'PULSEMODE0')
            s = self.ser.read(0)
            line = self.ser.readline()
            if line in (b'Osnovni nacin generiranja pulza: Pulz = 10ms\r\n', b'Osnovni nacin generiranja pulza je ze vkljucen!\r\n'):
                error = 0

            else:
                error = 1

        elif self.pulse == 2:  # 1: 10ms 2: random
            self.ser.write(b'PULSEMODE1')
            s = self.ser.read(0)
            line = self.ser.readline()
            if line in (b'Random nacin generiranja pulza vkljucen!\r\n', b'Random nacin generiranja pulza je ze vkljucen!'):
                error = 0

            else:
                error = 1

        if self.sensor_adc == 1:  # 1: adc_ON 2: adc_OFF
            self.ser.write(b'ADC_MODE_1')
            s = self.ser.read(0)
            line = self.ser.readline()
            if line in (b'ADC preverjanje pulza aktivirano!\r\n', b'ADC preverjanje pulza je ZE aktivirano!\r\n'):
                error = 0

            else:
                error = 1

        elif self.sensor_adc == 2:  # 1: adc_ON 2: adc_OFF
            self.ser.write(b'ADC_MODE_0')
            s = self.ser.read(0)
            line = self.ser.readline()
            if line in (b'ADC preverjanje pulza je deaktivirano!\r\n', b'ADC preverjanje pulza je ZE deaktivirano!\r\n'):
                error = 0

            else:
                error = 1

        if self.calibrate == 1:  # ne izvedi kalibracije
            self.ser.write(b'CALIBRATE1')
            s = self.ser.read(0)
            line = self.ser.readline()
            if line == b'Izvaja se ADC kalibracijski proces senzorja!\r\n':
                error = 0

            else:
                error = 1

        if error == 1:
            self.error_programming()
            self.msg.show()

        elif error == 0:
            self.compeate_programming()
            self.msg.show()

            self.config_exit()

        elif error == 2:
            pass

'''
----------  Debug window  ----------
'''


class DebugWindow(QWidget):
    def __init__(self):
        super(DebugWindow, self).__init__()
        self.serial_on = serial_on
        self.setupUi(self)

    def closeEvent(self, event):
        self.debug_exit()

    def setupUi(self, Debug_window):
        Debug_window.setObjectName("Debug_window")
        Debug_window.resize(643, 577)
        Debug_window.setWindowTitle("Debug")

        textEdit_font = QFont()
        textEdit_font.setPointSize(14)
        self.textEdit = QTextEdit(Debug_window)
        self.textEdit.setGeometry(QRect(30, 20, 891, 701))
        self.textEdit.setFont(textEdit_font)

        comboBox_font = QFont()
        comboBox_font.setPointSize(14)
        self.comboBox = QComboBox(Debug_window)
        self.comboBox.setGeometry(QRect(30, 730, 140, 30))

        self.comboBox.setFrame(False)
        self.comboBox.addItem(" ")

        available_ports = [port[0] for port in list_ports.comports()]

        for i in range(0, len(available_ports)):
            self.comboBox.addItem(available_ports[i])

        self.comboBox.setFont(comboBox_font)

        lineEdit_font = QFont()
        lineEdit_font.setPointSize(14)
        self.lineEdit = QLineEdit(Debug_window)
        self.lineEdit.setGeometry(QRect(180, 730, 540, 30))
        self.lineEdit.setFont(lineEdit_font)

        send_font = QFont()
        send_font.setPointSize(16)
        self.send_button = QPushButton(Debug_window)
        self.send_button.setGeometry(QRect(730, 730, 100, 30))
        self.send_button.setText("Send")
        self.send_button.setFont(send_font)

        self.retranslateUi(Debug_window)
        QMetaObject.connectSlotsByName(Debug_window)

    def retranslateUi(self, Debug_window):
        self.send_button.clicked.connect(self.send)
        self.comboBox.activated[str].connect(self.serial_port_select)

    def serial_port_select(self, text):
        self.port = text

        self.serial_on = 0

        if text != " ":
            self.serial = serial.Serial(
                port=self.port,
                baudrate=9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1)

            self.debugthread = DebugThread(self.port)
            self.debugthread.debug_thread.connect(self.receive)
            self.debugthread.setTerminationEnabled()
            self.debugthread.start()

            self.serial_on = 1

    def send(self):
        command = self.lineEdit.text()

        if command == "clr":
            self.textEdit.clear()

        else:
            self.serial.write(command.encode('ascii'))
            self.clock = dt.now()
            self.textEdit.setTextColor(Qt.blue)
            self.textEdit.append(str(self.clock.strftime("%d.%m.%Y %H:%M")) + '<- ' + command)

        time.sleep(0.2)

    def receive(self, message):
        message = message.strip()
        self.clock = dt.now()
        self.textEdit.setTextColor(Qt.red)
        self.textEdit.append(str(self.clock.strftime("%d.%m.%Y %H:%M")) + '-> ' + message)

    def debug_exit(self):
        if self.serial_on == 1:
            self.serial_on = 0
            self.debugthread.closeEvent(self.closeEvent)
            self.serial.close()


class DebugThread(QThread):
    debug_thread = pyqtSignal(str)

    def __init__(self, port):
        super(DebugThread, self).__init__()

        self.port = port
        self.ser = serial.Serial(
            port=self.port,
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1)

        self.kill_thread = 0

    def closeEvent(self, event):
        self.kill_thread = 1

    def run(self):
        while True:
            if self.kill_thread == 0:
                s = self.ser.read(0)
                line = self.ser.readline()

                #line = line.decode("utf-8")

                if line in (b'\x00\x00\x00\x00\x00\x00\x000\x00\n', b'0\x00\n'):
                    self.debug_thread.emit("0")

                elif line == b'1\x00\n':
                    self.debug_thread.emit("1")

                elif len(line) >= 10:
                    line = line.strip()
                    line = line.decode("utf-8")

                    k = 1
                    message = []
                    for i in range(0, len(line)):
                        if line[i] != '\x00':
                            message.append(line[i])
                            k += 1

                    e = ""
                    for i in range(0, len(message)):
                        e += str(message[i])

                    f = e.strip()

                    self.debug_thread.emit(f)

                #elif len(line) > 10:
                 #   line = line.strip()
                  #  #line = line.decode("utf-8")

                   # line = str(line)
                    #self.debug_thread.emit(line)

                else:
                    pass

                time.sleep(0.4)

            elif self.kill_thread == 1:
                self.ser.close()
                time.sleep(0.4)
                self.terminate()

'''
----------   Calibrate Sensor   ----------
'''


class CalibrateSensor(QWidget):
    def __init__(self):
        super(CalibrateSensor, self).__init__()

        self.port = " "
        self.serial_selected = 0

        self.setWindowTitle('Sensor calibration')
        self.resize(350, 80)
        self.move(100, 200)

        self.progressbar = QProgressBar()
        self.progressbar.reset()  # resets the progress bar
        self.progressbar.setAlignment(Qt.AlignCenter)  # centers the text
        self.progressbar.setFormat('%p%')
        self.progressbar.valueChanged.connect(self.progress_changed)

        self.btn_close = QPushButton('Close')
        self.btn_close.clicked.connect(self.close)

        self.comboBox = QComboBox()
        self.comboBox.addItem(" ")

        available_ports = [port[0] for port in list_ports.comports()]

        for i in range(0, len(available_ports)):
            self.comboBox.addItem(available_ports[i])

        self.comboBox.activated[str].connect(self.serial_port_select)

        # timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.progress_simulation)

        self.palette = QPalette(self.palette())

        # vertical layout
        hbox = QHBoxLayout()
        hbox.addWidget(self.comboBox)
        hbox.addSpacing(110)
        hbox.addWidget(self.btn_close)
        hbox.addSpacing(5)

        vbox = QVBoxLayout()
        vbox.addWidget(self.progressbar)
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        self.show()

    def serial_port_select(self, port):
        self.port = port

        if self.port != " ":
            self.serial_selected = 1
            self.ser = serial.Serial(
                port=self.port,
                baudrate=9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=0)

            self.calibrate_sensor()
        else:
            self.serial_selected = 0

    def closeEvent(self, event):
        if self.serial_selected == 1:
            self.ser.close()

    def calibrate_sensor(self):
        self.ser.write(b'CALIBRATE1')

        time.sleep(0.1)

        s = self.ser.read(0)
        line = self.ser.readline()  # read a '\n' terminated line

        if line == b'Izvaja se ADC kalibracijski proces senzorja!\r\n':

            self.complite = 0
            self.start()

        elif line != b'Izvaja se ADC kalibracijski proces senzorja!\r\n':
            self.fail()

        self.setPalette(self.palette)

    def progress_simulation(self):
        self.value = self.progressbar.value()  # gets the current value of the progress bar
        self.progressbar.setValue(self.value + 1)  # adds 1 to the current value

    def fail(self):
        self.var_fail = 1
        self.timer.start(8)  # interval of 200 milliseconds
        self.palette.setColor(QPalette.Highlight, QColor(Qt.red))

    def start(self):
        self.var_fail = 0
        self.timer.start(75)  # interval of 200 milliseconds
        self.palette.setColor(QPalette.Highlight, QColor(Qt.blue))

    def progress_changed(self, value):
        if self.var_fail == 0:
            s = self.ser.read(0)  # read up to three bytes (timeout)
            line = self.ser.readline()  # read a '\n' terminated line

            if line == b'Kalibracijski proces uspesno zakljucen\r\n':
                self.palette.setColor(QPalette.Highlight, QColor(Qt.green))
                self.setPalette(self.palette)

                self.timer.stop()
                self.timer.start(1)

                self.complite = 1

            if self.complite == 0 and value == 98:
                self.palette.setColor(QPalette.Highlight, QColor(Qt.red))
                self.setPalette(self.palette)

                self.progressbar.setFormat('Calibration Failed')
                self.timer.stop()
                self.timer.start(1)

            if value == 99 and self.complite == 1:
                self.progressbar.setFormat('Calibration Complete')
                self.timer.stop()
                self.timer.start(1)

        elif self.var_fail == 1:
            if value == 99:
                self.progressbar.setFormat('Calibration Failed')
                self.timer.stop()
                self.timer.start(1)


        if value == 100:
                self.timer.stop
                time.sleep(3)
                self.close()

'''
----------   SelectGraph   ----------
'''


class MplDrawGraph(QWidget):
    def __init__(self):
        super(MplDrawGraph, self).__init__()

        draw = 0

        self.port = " "
        self.pause = 0  # je bila tipka Pause pritisnjena
        self.button_log = 0  # je bila tipka Ok (log file) pritisnjena
        self.draw_data = 0 # izris grafa je izbran
        self.log_data = 0 # log data je izbran
        self.lenght = 10 # amplituda
        self.stoped = 1 #vse je izklopljeno
        self.step_mode_enable = 0 #step nacin
        self.one_step = 0 #ne naredi koraka

        date = dt.now()
        self.log_name = "log_" + date.strftime("%Y%d%m") + ".txt" #default name log file
        self.log_style = "%Y-%d-%m %H:%M:%S"
        self.log_vejica = " , "
        self.selector = 0

        self.draw_graph(self)

    def closeEvent(self, event):
        if self.port != " ":
            if draw == 1:
                self.drawthread.terminate()
                #os.system("chmod 444 " + self.log_name) #read only log file

        if self.button_log == 1:
            self.log_data.close()

    def draw_graph(self, MplDrawGraph):
        MplDrawGraph.setObjectName("MplDrawGraph")
        MplDrawGraph.resize(643, 577)
        MplDrawGraph.setWindowTitle("Draw graph")

        MplDrawGraph.setLocale(QLocale(QLocale.Slovenian, QLocale.Slovenia))
        MplDrawGraph.setInputMethodHints(Qt.ImhEmailCharactersOnly | Qt.ImhPreferLowercase)

        self.horizontalLayoutWidget = QWidget(MplDrawGraph)
        self.horizontalLayoutWidget.setGeometry(QRect(10, 10, 1080, 852))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QVBoxLayout(self.horizontalLayoutWidget)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        self.horizontalLayout.addWidget(self.canvas)

        self.mpl_toolbar = NavigationToolbar(self.canvas, self)
        self.horizontalLayout.addWidget(self.mpl_toolbar)

        self.verticalLayoutWidget = QWidget(MplDrawGraph)
        self.verticalLayoutWidget.setGeometry(QRect(1100, 10, 121, 571))#1100, 10, 130, 200
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.combo = QComboBox(self.verticalLayoutWidget)
        self.combo.setFrame(True)
        self.combo.setObjectName("comboBox")
        self.combo.addItem(" ")

        available_ports = [port[0] for port in list_ports.comports()]

        for i in range(0, len(available_ports)):
            self.combo.addItem(available_ports[i])

        self.verticalLayout.addWidget(self.combo)

        self.pushButton = QPushButton(self.verticalLayoutWidget)
        self.pushButton.setText("Draw ADC \nvalue")
        self.pushButton.setStyleSheet("background-color: white")
        self.verticalLayout.addWidget(self.pushButton)

        self.pushButton_3 = QPushButton(self.verticalLayoutWidget)
        self.pushButton_3.setText("Draw output \nvalue")
        self.pushButton_3.setStyleSheet("background-color: white")
        self.verticalLayout.addWidget(self.pushButton_3)

        spacerItem = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)

        self.pushButton_4 = QPushButton(self.verticalLayoutWidget)
        self.pushButton_4.setText("Pause")
        self.pushButton_4.setStyleSheet("background-color: yellow")
        self.verticalLayout.addWidget(self.pushButton_4)

        self.pushButton_5 = QPushButton(self.verticalLayoutWidget)
        self.pushButton_5.setText("Stop")
        self.pushButton_5.setStyleSheet("background-color: red")
        self.verticalLayout.addWidget(self.pushButton_5)

        spacerItem1 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem1)

        self.checkBox = QCheckBox(self.verticalLayoutWidget)
        self.checkBox.setEnabled(True)
        self.checkBox.setText("Real time graph")
        self.verticalLayout.addWidget(self.checkBox)

        self.horizontalSlider = QSlider(self.verticalLayoutWidget)
        self.horizontalSlider.setEnabled(False)
        self.horizontalSlider.setMinimum(1)
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setSingleStep(5)
        self.horizontalSlider.setSliderPosition(30)

        self.horizontalSlider.setOrientation(Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.verticalLayout.addWidget(self.horizontalSlider)

        spacerItem3 = QSpacerItem(20, 3, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem3)

        self.label = QLabel()
        self.label.setText("Value:")
        self.verticalLayout.addWidget(self.label)

        spacerItem5 = QSpacerItem(20, 3, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem5)

        self.steplineEdit = QLineEdit(self.verticalLayoutWidget)
        self.steplineEdit.setGeometry(QRect(5, 50, 151, 20))
        self.steplineEdit.setToolTip("")
        self.steplineEdit.setText("")
        self.steplineEdit.setDisabled(True)
        self.steplineEdit.setObjectName("step_value")
        self.verticalLayout.addWidget(self.steplineEdit)

        spacerItem2 = QSpacerItem(20, 15, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem2)

        self.checkBox_step = QCheckBox(self.verticalLayoutWidget)
        self.checkBox_step.setEnabled(True)
        self.checkBox_step.setText("Step mode")
        self.verticalLayout.addWidget(self.checkBox_step)

        spacerItem4 = QSpacerItem(20, 3, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem4)

        self.step_button = QPushButton(self.verticalLayoutWidget)
        self.step_button.setText("Step")
        self.step_button.setDisabled(True)
        # self.step_button.setStyleSheet("background-color: yellow")
        self.verticalLayout.addWidget(self.step_button)

        spacerItem6 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem6)

        self.checkBox_2 = QCheckBox(self.verticalLayoutWidget)
        self.checkBox_2.setEnabled(True)
        self.checkBox_2.setText("Make log file")
        self.verticalLayout.addWidget(self.checkBox_2)

        spacerItem7 = QSpacerItem(10, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem7)

        self.horizontalLayoutWidget = QWidget(MplDrawGraph)
        self.horizontalLayoutWidget.setGeometry(QRect(10, 10, 661, 541))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")

        self.mpi = QHBoxLayout(self.horizontalLayoutWidget)
        self.mpi.setContentsMargins(0, 0, 0, 0)
        self.mpi.setObjectName("mpi")

        self.groupBox = QGroupBox(MplDrawGraph)
        self.groupBox.setEnabled(False)
        self.groupBox.setGeometry(QRect(1100, 430, 230, 95))# 1005, 570, 230, 95

        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())

        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMaximumSize(QSize(16777215, 16777215))
        self.groupBox.setSizeIncrement(QSize(0, 3))
        self.groupBox.setObjectName("groupBox")
        self.groupBox.setTitle("Log file:")

        self.comboBox_2 = QComboBox(self.groupBox)
        self.comboBox_2.setGeometry(QRect(5, 20, 220, 20))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("%Y-%d-%m %H:%M:%S , data")
        self.comboBox_2.addItem("%H:%M:%S , data")
        self.comboBox_2.addItem("%d-%m %H:%M:%S , data")
        self.comboBox_2.addItem("%d-%m-%H:%M:%S,data")
        self.comboBox_2.addItem("%H:%M:%S,data")
        self.comboBox_2.addItem("%H%M%S,data")

        self.lineEdit = QLineEdit(self.groupBox)
        self.lineEdit.setGeometry(QRect(5, 50, 151, 20))
        self.lineEdit.setToolTip("")
        self.lineEdit.setText("")
        self.lineEdit.setPlaceholderText(self.log_name)
        self.lineEdit.setObjectName("lineEdit")

        self.pushButton_2 = QPushButton(self.groupBox)
        self.pushButton_2.setGeometry(QRect(160, 50, 31, 20))
        self.pushButton_2.setText("Ok")

        self.retranslateUi(MplDrawGraph)
        QMetaObject.connectSlotsByName(MplDrawGraph)

    def retranslateUi(self, MplDrawGraph):
        self.combo.activated[str].connect(self.port_select) # izberi port

        self.pushButton.clicked.connect(self.button_adc) # tipka Draw ADC
        self.pushButton_3.clicked.connect(self.button_val) # tipka Draw value

        self.pushButton_4.clicked.connect(self.button_pause) # tipka Pause
        self.pushButton_5.clicked.connect(self.button_stop) # tipka Stop

        self.checkBox.stateChanged.connect(self.enable_plot) # prikaz grafa

        self.horizontalSlider.valueChanged.connect(self.amplitude) # slider amplituda

        self.checkBox_step.stateChanged.connect(self.step_mode) #stepmode

        self.step_button.clicked.connect(self.make_one_step)

        self.checkBox_2.stateChanged.connect(self.enable_log)  # ustvari log file

        self.pushButton_2.clicked.connect(self.button_start_log)  # Ok log file

        self.comboBox_2.activated[str].connect(self.log_style_selected)  # izberi log file style

        self.lineEdit.textChanged.connect(self.log_name_selected) # spremeni log file name

    def port_select(self, port):
        self.port = port

    def button_adc(self):
        draw = 1
        self.stoped = 0
        button_id = "button_adc"
        self.draw_selector(button_id)

    def button_val(self):
        draw = 1
        self.stoped = 0
        button_id = "button_val"
        self.draw_selector(button_id)

    def button_pause(self):
        if self.stoped == 0:
            # self.init_figure()
            if self.pause == 1:
                self.pause = 0
                if self.draw_data == 1 or self.log_data == 1:
                    self.drawthread.start()

            elif self.pause == 0:
                self.pause = 1
                if self.draw_data == 1 or self.log_data == 1:
                    self.drawthread.requestInterruption()

    def button_stop(self):
        self.stoped = 1
        button_id = "button_stop"
        self.draw_selector(button_id)

    def enable_plot(self):
        if self.horizontalSlider.isEnabled() == True:
            self.horizontalSlider.setEnabled(False)
            self.steplineEdit.setDisabled(True)
            self.steplineEdit.clear()

            self.draw_data = 0

            plt.clf() # zapremo figure

        else:
            self.horizontalSlider.setEnabled(True)
            self.steplineEdit.setDisabled(False)
            self.steplineEdit.clear()

            self.draw_data = 1

            self.init_figure() # inicializiramo figure

    def amplitude(self, val):
        self.lenght = val

    def step_mode(self):
        if self.step_mode_enable == 0:

            self.step_button.setDisabled(False)

            self.step_mode_enable = 1

        elif self.step_mode_enable == 1:

            self.step_button.setDisabled(True)

            self.step_mode_enable = 0

    def make_one_step(self):
        self.one_step = 1

    def enable_log(self):
        if self.button_log == 0:
            if self.groupBox.isEnabled() == True:
                self.groupBox.setEnabled(False)
            else:
                self.groupBox.setEnabled(True)
        else:
            self.button_log = 0
            self.log_data.close()

    def button_start_log(self):
        self.groupBox.setEnabled(False)
        self.button_log = 1
        self.header_created = 0

        self.log_data = open(self.log_name, 'a', encoding='utf8')

    def log_style_selected(self, style):
        if style == "%Y-%d-%m %H:%M:%S , data":
            self.log_style = "%Y-%d-%m %H:%M:%S"
            self.log_vejica = " , "

        elif style == "%H:%M:%S , data":
            self.log_style = "%H:%M:%S"
            self.log_vejica = " , "

        elif style == "%d-%m %H:%M:%S , data":
            self.log_style = "%d-%m %H:%M:%S"
            self.log_vejica = " , "

        elif style == "%d-%m-%H:%M:%S,data":
            self.log_style = "%d-%m %H:%M:%S"
            self.log_vejica = ","

        elif style == "%H:%M:%S,data":
            self.log_style = "H:%M:%S"
            self.log_vejica = ","

        elif style == "%H%M%S,data":
            self.log_style = "%H%M%S"
            self.log_vejica = ","
                    
    def log_name_selected(self, name):
        self.log_name = name

    def draw_selector(self, button_id):
        if self.port != " ":
            ser = serial.Serial(
                port=self.port,
                baudrate=9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1)

            if self.selector == 1 or self.selector == 2:
                button_id = "button_stop"

            if button_id == "button_adc":
                self.selector = 1
                ser.write(b'SW_VALUE_0')
                s = ser.read(0)  # read up to three bytes (timeout)
                line = ser.readline()  # read a '\n' terminated line

                ser.write(b'SHOW_ADC_1')
                s = ser.read(0)  # read up to ten bytes (timeout)
                line1 = ser.readline()  # read a '\n' terminated line

                if line1 == b'Ispisuj ADC vrednosti!\r\n':
                    s = ser.read(0)  # read up to ten bytes (timeout)
                    line2 = ser.readline()  # read a '\n' terminated line

                    if line2 == b'Omogoci ADC pretvornik z uporabo ukaza: ADC_MODE_1.\r\n':
                        ser.write(b'ADC_MODE_1')
                        s = ser.read(0)  # read up to ten bytes (timeout)
                        line3 = ser.readline()  # read a '\n' terminated line

                    self.pushButton.setStyleSheet("background-color: green")
                    self.pushButton_3.setStyleSheet("background-color: white")

                    ser.close()

                    self.drawthread = DrawThread(self.port)
                    self.drawthread.draw_thread.connect(self.change_value)
                    self.drawthread.setTerminationEnabled()
                    self.drawthread.start()

                else:
                    ser.close()
                    self.pushButton.setStyleSheet("background-color: red")
                    self.pushButton_3.setStyleSheet("background-color: white")

            elif button_id == "button_val":
                self.selector = 2
                ser.write(b'SHOW_ADC_0')
                s = ser.read(0)  # read up to ten bytes (timeout)
                line = ser.readline()  # read a '\n' terminated line

                if line in (b'Ne ispisuj ADC vrednosti.\r\n', b'Ispisovanje ADC vrednosti je ze deaktivirano.\r\n'):
                    ser.write(b'SW_VALUE_1')
                    self.pushButton.setStyleSheet("background-color: white")
                    self.pushButton_3.setStyleSheet("background-color: green")

                    ser.close()

                    self.drawthread = DrawThread(self.port)
                    self.drawthread.draw_thread.connect(self.change_value)
                    self.drawthread.setTerminationEnabled()
                    self.drawthread.start()

                else:
                    self.pushButton.setStyleSheet("background-color: white")
                    self.pushButton_3.setStyleSheet("background-color: red")

                    ser.close()

            if button_id == "button_stop":
                if self.selector == 1 or self.selector == 2:
                    self.selector = 0
                    ser.close()

                    time.sleep(0.2)

                    self.drawthread.closeEvent(self.closeEvent)

                    self.pushButton.setStyleSheet("background-color: white")
                    self.pushButton_3.setStyleSheet("background-color: white")

                    time.sleep(0.8)

                    ser = serial.Serial(
                        port=self.port,
                        baudrate=9600,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS,
                        timeout=1)

                ser.write(b'SHOW_ADC_0')
                s = ser.read(1)  # read up to ten bytes (timeout)
                line = ser.readline()  # read a '\n' terminated line

                ser.write(b'SW_VALUE_0')
                s = ser.read(1)  # read up to ten bytes (timeout

                ser.close()

        else:
            pass

    def init_figure(self):
        if self.draw_data == 1:

            self.ax = self.figure.add_subplot(1, 1, 1)

            plt.ion()  # Set interactive mode ON, so matplotlib will not be blocking the window

            # meje osi
            self.axes = plt.gca()
            self.ax.set_autoscale_on(False)

            self.x = []
            self.y = []

            self.ax.plot(self.x, self.y)

            #plt.tight_layout()

            self.canvas.draw()

        elif self.draw_data == 0:
            pass

    def change_value(self, value):

        if self.step_mode_enable == 1 and self.one_step == 1 or self.step_mode_enable == 0:

            if self.draw_data == 1 and self.pause == 0 and self.stoped == 0:
                self.ax.clear()

                self.ax.set_title("Izris trenutne vrednosti")
                self.ax.set_xlabel('Čas [h:m:s]')  # x os label

                self.x.append(dt.now())
                self.y.append(value)

                background = self.figure.canvas.copy_from_bbox(self.ax.bbox)

                self.ax.plot(self.x, self.y)
                self.ax.xaxis.set_major_formatter(md.DateFormatter('%H:%M:%S'))
                for label in self.ax.xaxis.get_ticklabels():
                    label.set_rotation(45)

                if self.selector == 1:
                    self.ax.set_ylabel('Trenutna ADC vrednost senzorja')  # y os label
                    self.axes.set_ylim([-0.4, 1020])

                if self.selector == 2:
                    self.ax.set_ylabel('Trenutna vrednost izhoda senzorja [1 = ON], [0 = OFF]')  # y os label
                    self.axes.set_ylim([-0.1, 1.1])

                if len(self.x) > self.lenght:
                    del self.y[0]
                    del self.x[0]
                self.canvas.draw()

                self.steplineEdit.clear()
                self.steplineEdit.setText(str(value))

            if self.button_log == 1 and self.pause == 0 and self.stoped == 0:
                if self.header_created == 0:
                    self.header_created = 1

                    self.log_data.writelines(["#TITLE = " + "Izris trenutne vrednosti" + "\n"])
                    self.log_data.writelines(["#X = " + "Cas [h:m:s]" + "\n"])

                    if self.selector == 1:
                        self.log_data.writelines(["#Y = " + "Trenutna ADC vrednost senzorja" + "\n"])

                    elif self.selector == 2:
                        self.log_data.writelines(
                            ["#Y = " + "Trenutna vrednost izhoda senzorja [1 = ON], [0 = OFF]" + "\n"])

                    self.log_data.writelines(
                        ["#------------------------------------------------------------------" + "\n"])

                datum = dt.now()
                self.log_data.writelines([datum.strftime(self.log_style) + self.log_vejica + str(value) + "\n"])

            else:
                pass

            if self.step_mode_enable == 1 and self.one_step == 1:
                self.one_step = 0


class DrawThread(QThread):
    draw_thread = pyqtSignal(int)

    def __init__(self, port):
        super(DrawThread, self).__init__()
        self.kill_thread = 0
        self.ser = serial.Serial(
            port=port,
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1)

    def __del__(self):
        pass

    def closeEvent(self, event):
        self.kill_thread = 1

    def run(self):
        while True:
            if self.kill_thread == 0:
                time.sleep(0.1)
                s = self.ser.read(0)
                line = self.ser.readline()

                if line == b'0\x00\n':
                    self.draw_thread.emit(0)

                elif line == b'1\x00\n':
                    self.draw_thread.emit(1)

                elif len(line) == 10:
                    line = line.strip()
                    line = line.decode("utf-8")

                    k = 1
                    message = []
                    for i in range(0, len(line)):
                        if line[i] != '\x00':
                            message.append(line[i])
                            k += 1

                    e = ""
                    for i in range(0, len(message)):
                        e += str(message[i])

                    recived = int(e)

                    self.draw_thread.emit(recived)

                else:
                    pass

            elif self.kill_thread == 1:
                self.ser.close()
                time.sleep(0.4)
                self.terminate()

'''
----------   Log plotter   ----------
'''


class MplLogPlotter(QWidget):
    def __init__(self):
        super(MplLogPlotter, self).__init__()

        self.color = QColor(Qt.darkBlue) # modra barva

        self.draw_line = 1 # izris line 1: ON 0: OFF
        self.draw_dots = 0 # izris dots 1: ON 0: OFF
        self.file_open = 0 # dokuent je odprt
        self.read_error = 1

        self.draw_log_ui(self)

    def closeEvent(self, event):
        if self.file_open == 0:
            self.close

    def draw_log_ui(self, MplLogPlotter):
        MplLogPlotter.setObjectName("MplLogPlotter")
        MplLogPlotter.setWindowTitle("Log File Plotter")
        MplLogPlotter.resize(815, 664)
        MplLogPlotter.setLocale(QLocale(QLocale.Slovenian, QLocale.Slovenia))
        MplLogPlotter.setInputMethodHints(Qt.ImhEmailCharactersOnly | Qt.ImhPreferLowercase)

        self.horizontalLayoutWidget = QWidget(MplLogPlotter)
        self.horizontalLayoutWidget.setGeometry(QRect(10, 50, 1630, 920))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QVBoxLayout(self.horizontalLayoutWidget)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        self.horizontalLayout.addWidget(self.canvas)

        self.mpl_toolbar = NavigationToolbar(self.canvas, self)
        self.horizontalLayout.addWidget(self.mpl_toolbar)

        self.groupBox = QGroupBox(MplLogPlotter)
        self.groupBox.setGeometry(QRect(580, 0, 175, 50))
        self.groupBox.setTitle("Plot:")
        self.groupBox.setEnabled(True)

        self.QCheckBox1 = QCheckBox(self.groupBox)
        self.QCheckBox1.setGeometry(QRect(10, 25, 45, 20))
        self.QCheckBox1.setText("line")
        self.QCheckBox1.setEnabled(True)
        self.QCheckBox1.setChecked(True)

        self.QCheckBox2 = QCheckBox(self.groupBox)
        self.QCheckBox2.setGeometry(QRect(55, 25, 45, 20))
        self.QCheckBox2.setText("dots")
        self.QCheckBox2.setEnabled(True)
        self.QCheckBox2.setChecked(False)

        self.label = QLabel(self.groupBox)
        self.label.setGeometry(QRect(105, 25, 60, 20))
        self.label.setText("color:")

        self.color_selector = QPushButton(self.groupBox)
        self.color_selector.setGeometry(QRect(145, 25, 20, 20))
        #self.color_selector.visibleRegion()
        self.color_selector.setStyleSheet("background-color:" + self.color.name())

        self.horizontalLayoutWidget_2 = QWidget(MplLogPlotter)
        self.horizontalLayoutWidget_2.setGeometry(QRect(18, 25, 522, 20))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.lineEdit = QLineEdit(self.horizontalLayoutWidget_2)
        self.lineEdit.setToolTip("")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setPlaceholderText("log file location:")
        self.lineEdit.setReadOnly(False)
        self.lineEdit.setFixedSize(QSize(500, 20))
        self.horizontalLayout.addWidget(self.lineEdit)

        #spacerItem = QSpacerItem(1, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        #self.horizontalLayout.addItem(spacerItem)

        self.pushButton = QPushButton(self.horizontalLayoutWidget_2)

        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())

        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setFixedSize(QSize(20, 20))

        # Icon made by[ Dave Gandy in shapes] from www.flaticon.com
        self.pushButton.setIcon(QIcon('icons/open-folder.png'))
        self.horizontalLayout.addWidget(self.pushButton)

        #self.horizontalSlider = QSlider(MplLogPlotter)
        #self.horizontalSlider.setGeometry(QRect(300, 930, 150, 30))
        #self.horizontalSlider.setOrientation(Qt.Horizontal)
        #self.horizontalSlider.setObjectName("horizontalSlider")

        self.retranslateUi(MplLogPlotter)
        QMetaObject.connectSlotsByName(MplLogPlotter)

    def retranslateUi(self, MplLogPlotter):
        self.pushButton.clicked.connect(self.find_log_location)  # najdi lokacijo log file

        self.lineEdit.textChanged.connect(self.log_location_is)  # lokacija log file je =

        self.QCheckBox1.stateChanged.connect(self.draw_line_select)

        self.QCheckBox2.stateChanged.connect(self.draw_dots_select)

        self.color_selector.clicked.connect(self.pick_color)

    def find_log_location(self):
        location = QFileDialog.getOpenFileName(self, "Open log file", "", "Text files (*.txt *.log)")

        if location != ('', ''):
            log_location = ''.join(location) # convert tuple to string
            self.log_location = log_location.replace("Text files (*.txt *.log)", "")

            self.lineEdit.setText(self.log_location)
            self.lineEdit.setReadOnly(True)

            self.log_file_data()
            self.log_file_init_figure()

    def log_location_is(self, file):
        self.log_location = file

    def draw_line_select(self):
        if self.draw_line == 0:
            self.draw_line = 1

        elif self.draw_line == 1:
            self.draw_line = 0

        self.log_file_init_figure()

    def draw_dots_select(self):
        if self.draw_dots == 0:
            self.draw_dots = 1

        elif self.draw_dots == 1:
            self.draw_dots = 0

        self.log_file_init_figure()

    def pick_color(self):
        self.color = QColorDialog.getColor(Qt.darkBlue)
        self.color_selector.setStyleSheet("background-color:" + self.color.name())

        self.log_file_init_figure()

    def log_file_data(self):
        self.log_data = open(self.log_location, 'r').read()
        self.file_open = 1

        lines = []
        lines = self.log_data.split('\n')

        header = []

        xs = []
        self.ys = []

        for line in range(0, len(lines)):
            if line < 3:
                header.append(lines[line])

            elif line > 3:
                if lines[line] not in ("", " "):

                    x, y = lines[line].split(",")

                    # odstranimo presledke iz vrednosti
                    y = y.strip(" ")

                    xs.append(x)
                    self.ys.append(y)

                elif lines[line] == " ":
                    pass

        # log file header
        for n in range(0, len(header)):
            read_line = header[n]

            if read_line[0:9] == "#TITLE = ":
                self.title = read_line[9:len(read_line)]

            elif read_line[0:5] == "#X = ":
                self.x_label = read_line[5:len(read_line)]

            elif read_line[0:5] == "#Y = ":
                self.y_label = read_line[5:len(read_line)]


        # log file data
        slot = np.chararray((len(xs), 12), itemsize=5)
        slot[:] = '0'

        xsss = []
        for i in range(0, len(xs)):
            xss = xs[i]
            # print(xss)

            a = ''
            b = 0
            for j in range(0, len(xss)):
                if xss[j] not in ('-', ':', ' '):
                    a += xss[j]

                elif xss[j] in ('-', ':', ' '):
                    slot[i, b] = a
                    b += 1

                    if j != (len(xss)):
                        slot[i, b] = xss[j]
                        b += 1
                        a = ''

                    # ce je zadnji char ' ' ga odstranimo:
                    if xss[j] == ' ' and j == len(xss) - 1:
                        xss = xss[:-1]

            xsss.append(xss)

        # Testne tocke [1],[3],[5]
        a = 0
        column_a = []
        for k in range(0, len(slot)):
            column_a.append(slot[k, 1])

            if k > 0:
                if column_a[0] != column_a[k]:
                    a += 1

        b = 0
        column_b = []
        for k in range(0, len(slot)):
            column_b.append(slot[k, 3])

            if k > 0:
                if column_b[0] != column_b[k]:
                    b += 1

        c = 0
        column_c = []
        for k in range(0, len(slot)):
            column_c.append(slot[k, 5])

            if k > 0:
                if column_c[0] != column_c[k]:
                    c += 1

        if a == 0 and b == 0 and c == 0:
            self.read_error = 0

        else:
            self.read_error = 1

        if column_a[5] == b'-':
            if column_b[5] == b'-':
                if column_c[5] == '':
                    self.log_style = "%Y-%d-%m %H:%M:%S "

                elif column_c[5] == b':':
                    self.log_style = "%d-%m-%H:%M:%S"

            elif column_b[5] == b':':
                self.log_style = "%d-%m %H:%M:%S"

        elif column_a[5] == b':':
            if column_b[5] == b':':
                if column_c[5] == '':
                    self.log_style = "%H:%M:%S"

                elif column_c[5] == '':
                    self.log_style = "%H:%M:%S"

        elif column_a[5] not in (b':', b'-'):
            self.log_style = "H%M%S"

        self.xi = []
        for i in range(0, len(xs)):
            xd = dt.strptime(xs[i], self.log_style)
            self.xi.append(xd)

    def error_message(self):
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Critical)

        self.msg.setWindowTitle("Error message")
        self.msg.setText("Can't read log file!")
        # self.msg.setDetailedText("feee")
        self.msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        self.msg.buttonClicked.connect(self.exit_msg)

    def log_file_init_figure(self):
        if self.read_error == 0:
            # print(self.xi)
            # print(self.ys)

            self.ax = self.figure.add_subplot(1, 1, 1)
            plt.ion()  # Set interactive mode ON, so matplotlib will not be blocking the window

            # meje osi
            self.axes = plt.gca()

            self.ax.clear()

            if self.draw_line == 1 and self.draw_dots == 0:
                self.ax.plot(self.xi, self.ys, color=self.color.name())

            elif self.draw_line == 0 and self.draw_dots == 1:
                self.ax.plot(self.xi, self.ys, 'o', color=self.color.name(), marker='.')

            elif self.draw_line == 1 and self.draw_dots == 1:
                self.ax.plot(self.xi, self.ys, color=self.color.name(), marker='.')

            self.ax.set_title(self.title)
            self.ax.set_xlabel(self.x_label)
            self.ax.set_ylabel(self.y_label)

            self.ax.xaxis.set_major_formatter(md.DateFormatter('%H:%M:%S'))
            for label in self.ax.xaxis.get_ticklabels():
                label.set_rotation(45)

            self.canvas.draw()

        elif self.read_error == 1:
            self.error_message

'''
----------   Log editor   ----------
'''


class MplLogEditor(QWidget):
    def __init__(self):
        super(MplLogEditor, self).__init__()

        self.title = ""
        self.x_label = ""
        self.y_label = ""

        self.header = 0
        self.log_location = ""


        self.edit_log_ui(self)

    def closeEvent(self, event):
        pass

    def edit_log_ui(self, MplLogEditor):
        MplLogEditor.setWindowTitle("Log file editor")
        MplLogEditor.resize(815, 664)
        MplLogEditor.setLocale(QLocale(QLocale.Slovenian, QLocale.Slovenia))
        MplLogEditor.setInputMethodHints(Qt.ImhEmailCharactersOnly | Qt.ImhPreferLowercase)

        '''
           -------------------- Header ------------------------
        '''
        self.verticalLayoutWidget = QWidget(MplLogEditor)
        self.verticalLayoutWidget.setGeometry(QRect(880, 50, 250, 205))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.groupBox_2 = QGroupBox(self.verticalLayoutWidget)
        self.groupBox_2.setTitle("Log file header:")
        self.groupBox_2.setEnabled(False)

        self.verticalLayoutWidget_2 = QWidget(self.groupBox_2)
        self.verticalLayoutWidget_2.setGeometry(QRect(10, 20, 230, 180))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")

        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel(self.verticalLayoutWidget_2)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())

        self.label.setSizePolicy(sizePolicy)
        self.label.setText("Plot title:")
        self.verticalLayout_2.addWidget(self.label)

        spacerItem = QSpacerItem(20, 3, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem)

        self.lineEdit_3 = QLineEdit(self.verticalLayoutWidget_2)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.verticalLayout_2.addWidget(self.lineEdit_3)

        spacerItem1 = QSpacerItem(20, 8, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem1)

        self.label_2 = QLabel(self.verticalLayoutWidget_2)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setText("X-axis label:")
        self.verticalLayout_2.addWidget(self.label_2)

        spacerItem2 = QSpacerItem(20, 3, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem2)
        self.lineEdit_2 = QLineEdit(self.verticalLayoutWidget_2)
        self.verticalLayout_2.addWidget(self.lineEdit_2)

        spacerItem3 = QSpacerItem(20, 8, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem3)
        self.label_3 = QLabel(self.verticalLayoutWidget_2)

        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setText("Y-axis label:")
        self.verticalLayout_2.addWidget(self.label_3)

        spacerItem4 = QSpacerItem(20, 3, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem4)

        self.lineEdit_4 = QLineEdit(self.verticalLayoutWidget_2)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.verticalLayout_2.addWidget(self.lineEdit_4)
        self.verticalLayout.addWidget(self.groupBox_2)

        '''
            -------------------- Tools ------------------------
        '''

        self.pushButton_3 = QPushButton(MplLogEditor)
        # Icon made by[ Dave Gandy in shapes] from www.flaticon.com
        self.pushButton_3.setIcon(QIcon('icons/open-folder.png'))
        self.pushButton_3.setStatusTip('Open log file')
        self.pushButton_3.setGeometry(QRect(10, 10, 20, 20))

        self.pushButton_2 = QPushButton(MplLogEditor)
        # Icon made by[Sarfraz Shoukat in interface] from www.flaticon.com
        self.pushButton_2.setIcon(QIcon('icons/add-new-document.png'))
        self.pushButton_2.setStatusTip('Create new log file')
        self.pushButton_2.setGeometry(QRect(35, 10, 20, 20))

        self.pushButton = QPushButton(MplLogEditor)
        # Icon made by[Freepik in technology] from www.flaticon.com
        self.pushButton.setIcon(QIcon('icons/diskette.png'))
        self.pushButton.setStatusTip('Save log file')
        self.pushButton.setGeometry(QRect(60, 10, 20, 20))

        self.lineEdit_1 = QLineEdit(MplLogEditor)
        self.lineEdit_1.setGeometry(QRect(85, 10, 500, 20))
        self.lineEdit_1.setReadOnly(False)

        self.QCheckBox1 = QCheckBox(MplLogEditor)
        self.QCheckBox1.setText('Make log file header')
        self.QCheckBox1.setGeometry(QRect(880, 10, 180, 20))
        self.QCheckBox1.setChecked(False)

        '''
            -------------------- Text edit ------------------------
        '''

        self.text_editor = QTextEdit(MplLogEditor)
        self.text_editor.setGeometry(QRect(10, 50, 850, 890))

        self.retranslateUi()

    def retranslateUi(self):
        #Tools buttons:
        self.pushButton_3.clicked.connect(self.file_location) # OPEN LOG FILE
        self.pushButton_2.clicked.connect(self.new_file) # NEW LOG FILE
        self.pushButton.clicked.connect(self.save_file)  # SAVE LOG FILE

        self.lineEdit_3.textChanged.connect(self.change_title)
        self.lineEdit_2.textChanged.connect(self.change_x_label)
        self.lineEdit_4.textChanged.connect(self.change_y_label)

        self.QCheckBox1.stateChanged.connect(self.header_enable)

    def header_enable(self):
        if self.header == 0:
            self.header = 1
            self.groupBox_2.setEnabled(True)

        elif self.header == 1:
            self.header = 0
            self.groupBox_2.setEnabled(False)

    def change_title(self, title):
        self.title = title

    def change_x_label(self, label):
        self.x_label = label

    def change_y_label(self, label):
        self.y_label = label

    def file_location(self):
        location = QFileDialog.getOpenFileName(self, "Open log file", "", "Text files (*.txt *.log)")

        if location != ('', ''):
            log_location = ''.join(location)  # convert tuple to string
            self.log_location = log_location.replace("Text files (*.txt *.log)", "")

            self.lineEdit_1.setText(self.log_location)
            self.lineEdit_1.setReadOnly(True)

            #preberimo file:
            self.open_file()

        else:
            pass

    def open_file(self):
        location = open(self.log_location, 'r')

        data = location.read()

        self.file_open = 1

        self.text_editor.clear()

        lines = []
        lines = data.split('\n')

        for line in range(0, len(lines)):
            read_line = lines[line]

            if line < 3:
                if read_line[0:9] == "#TITLE = ":
                    self.title = read_line[9:len(read_line)]

                    self.lineEdit_3.setText(self.title)
                    self.QCheckBox1.setChecked(True)

                elif read_line[0:5] == "#X = ":
                    self.x_label = read_line[5:len(read_line)]

                    self.lineEdit_2.setText(self.x_label)
                    self.QCheckBox1.setChecked(True)

                elif read_line[0:5] == "#Y = ":
                    self.y_label = read_line[5:len(read_line)]

                    self.lineEdit_4.setText(self.y_label)
                    self.QCheckBox1.setChecked(True)

                else:
                    self.text_editor.append(read_line)

            elif line > 3:
                self.text_editor.append(read_line)

        location.close()

    def save_file(self):
        location = QFileDialog.getSaveFileName(self, "Save log file", self.log_location, "Text files (*.txt *.log)")

        if location != ('', ''):
            log_location = ''.join(location)  # convert tuple to string
            location_open = log_location.replace("Text files (*.txt *.log)", "")

            data_out = open(location_open, 'w')

            self.lineEdit_1.setText(self.log_location)
            self.lineEdit_1.setReadOnly(True)

            data_in = self.text_editor.toPlainText()

            lines = []
            lines = data_in.split('\n')


            if self.header == 1:
                for line in range(0, (len(lines) + 4)):
                    if line == 0:
                        data_out.writelines(["#TITLE = " + self.title + "\n"])
                        print(self.title)

                    elif line == 1:
                        data_out.writelines(["#X = " + self.x_label + "\n"])
                        print(self.x_label)

                    elif line == 2:
                        data_out.writelines(["#Y = " + self.y_label + "\n"])
                        print(self.y_label)

                    elif line == 3:
                        data_out.writelines(["#------------------------------------------------------------------" + "\n"])

                    elif line > 3:

                        read_line = lines[line - 4]
                        data_out.writelines([read_line + "\n"])

            elif self.header == 0:
                for line in range(0, len(lines)):
                    read_line = lines[line]

                    data_out.writelines([read_line + "\n"])

            data_out.close()

    def new_file(self):
        self.log_location = ""
        self.lineEdit_1.setText(self.log_location)
        self.lineEdit_1.setReadOnly(False)

        self.QCheckBox1.setChecked(False)

        self.text_editor.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainWin = MainWindow()
    mainWin.showMaximized()
    #mainWin.show()

    '''
      ---- Splash screen -----
    '''
    splash = QQuickView()
    splash.setSource(QUrl('splash.qml'))
    splash.setFlags(Qt.FramelessWindowHint | Qt.Window | Qt.WindowSystemMenuHint)
    splash.setX(550)
    splash.setY(400)

    #splash.setX(330)
    #splash.setY(200)
    splash.show()

    for i in range(0, 2000000):
        app.processEvents()

    splash.close()

    sys.exit(app.exec_())
