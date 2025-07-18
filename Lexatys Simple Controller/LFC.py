# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LFC_simple.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
from serial import Serial
from os import path
from threading import Thread, Event
from queue import Queue
from serial.serialutil import EIGHTBITS, STOPBITS_ONE
#from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6 import uic
import serial.tools.list_ports


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ui_location = path.abspath(path.dirname(__file__))
        templateFile = archive.filename
        uic.loadUi(ui_location + "/" + templateFile, self)
        f = funcs()
        #Custom Command triggers for controller
        self.connect_button.clicked.connect(lambda: f.CONNECT())
        self.disconnect_button.clicked.connect(lambda: f.DISCONNECT())
        self.band_amp_button.clicked.connect(lambda: f.BANDAMP())
        self.external_button.clicked.connect(lambda: f.EXTERNALSWITCH())
        self.firmware_button.clicked.connect(lambda: f.GETFIRMWARE())
        self.model_button.clicked.connect(lambda: f.GETPN())
        self.SLS_button.clicked.connect(lambda: f.STARTLOD())
        self.OffS_button.clicked.connect(lambda: f.OFF_STATE())
        self.tem_button.clicked.connect(lambda: f.GETTEMP())
        self.LPM_button.clicked.connect(lambda: f.STARTSLP())
        self.serial_button.clicked.connect(lambda: f.GETSERIAL())
        self.actionAdvanced_Mode.changed.connect(lambda: f.advMode())
        self.actionRefresh_COM_Ports.triggered.connect(lambda: f.ports())


class archive():
    filename = "LFC_simple_full.ui"

class funcs():   
    """Commands for Serial Communication Connection"""
    def CONNECT(self):
        """estabish connection"""
        com_id = ui.com_choice.currentText()
        com_id = com_id.strip()
        self.connection(com_id)

    def connection(self, com_id_):
        try:
            global ser
            ser = Serial(com_id_, 115200, timeout=1)
            ui.command_output.appendPlainText("Successfully Connected to "+ str(com_id_))
            ui.connection_label.setStyleSheet("color: rgb(0, 206, 34);")
            ui.connection_label.setText("Connected!")
            ui.misc_group.setEnabled(True)
            ui.band_amp_commands.setEnabled(True)
        except Exception as e:
            print(e)
            ui.command_output.appendPlainText("Failed to connect on port " + str(com_id_))

    def DISCONNECT(self):
        """close serial connection"""
        try:
            ser.close()
            ui.command_output.appendPlainText("\nSerial Connection has been disconnected")
            ui.connection_label.setStyleSheet("color: rgb(255, 0, 4);")
            ui.connection_label.setText('Disconnected!')
            ui.misc_group.setEnabled(False)
            ui.band_amp_commands.setEnabled(False)
        except:
            ui.command_output.appendPlainText("No Serial Connection found, please reconnect")
    
    def ports(self):
        ui.com_choice.clear()
        ports = [comport.device for comport in serial.tools.list_ports.comports()]
        for item in ports:
            ui.com_choice.addItem(item)


    def advMode(self):
        cCheck = 0
        cCom = ui.com_choice.currentText()
        if ui.actionAdvanced_Mode.isChecked():
            if ui.connection_label.text() == "Connected!":
                cCheck = 1
            ui.advModeUpdate()
            self.ports()
            if cCheck == 1:
                ui.connection_label.setStyleSheet("color: rgb(0, 206, 34);")
                ui.connection_label.setText("Connected!")
                ui.com_choice.setCurrentText(cCom)
                try:
                    ui.band_amp_commands.setEnabled(True)
                    ui.misc_group.setEnabled(True)
                except:
                    pass
        else:
            if ui.connection_label.text() == "Connected!":
                cCheck = 1
            ui.setupUi(MainWindow)
            self.ports()
            if cCheck == 1:
                ui.connection_label.setStyleSheet("color: rgb(0, 206, 34);")
                ui.connection_label.setText("Connected!")
                ui.com_choice.setCurrentText(cCom)
                try:
                    ui.band_amp_commands.setEnabled(True)
                    ui.misc_group.setEnabled(True)
                except:
                    pass

    def BANDAMP(self):
        bands = {-2:"0", -3:"1", -4:"2", -5:"3", -6:"4", -7:"5", -8:"6", -9:"7", -10:""}
        amps = {-2:"1", -3:"2", -4:"0"}
        band_choice = bands[ui.Bypass_group.checkedId()]
        amp_choice = amps[ui.Amp_group.checkedId()]
        default_command = "BND"
        if band_choice == "":
            default_command = "BYP"
        command = default_command + band_choice + amp_choice + "\n"
        b_command = bytes(command, 'utf-8')
        s.send(b_command)
        
    
    def GETTEMP(self):
        """get the unit's temp"""
        s.send(b'TMP?\n')
    
    def GETSERIAL(self):
        """get the unit's serial number"""
        s.send(b'SN?\n')

    def STARTSLP(self):
        """Switches Unit to Low Power State"""
        s.send(b'SLP\n')

    def GETFIRMWARE(self):
        """get the unit's firmware version"""
        s.send(b'FM?\n')
    
    def GETTEMP(self):
        """get the unit's temp"""
        s.send(b'TMP?\n')
    
    def EXTERNALSWITCH(self):
        """Switches unit to External Switch"""
        s.send(b'BYP3\n')
    
    def GETPN(self):
        """get the unit's part number"""
        s.send(b'PN?\n')

    def OFF_STATE(self):
        """Switches unit into Off State"""
        s.send(b'OFF\n')

    def STARTLOD(self):
        """Switches unit into Safety Load State"""
        s.send(b'LOD\n')


class ccommands(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while True:
            command = q.get(block=True, timeout=None)
            try:
                ser.write(command)
                data = ser.readline()
            except NameError:
                data = "No COM Port set! Connect to a COM Port"
            textq.put(data)

class survey(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        oldports = []
        while True:
            ports = [comport.device for comport in serial.tools.list_ports.comports()]
            if ports != oldports:
                ui.com_choice.clear()
                diffCOM = list(set(ports) ^ set(oldports))
                for item in ports:
                    ui.com_choice.addItem(item)
                ui.com_choice.setCurrentText(diffCOM[0])
                oldports = ports
            else:
                pass

class LSCommands():
    def send(self, command):
        q.put(command)
        text = (textq.get())
        try:
            text = text.decode(encoding='UTF-8')
            text = text.split("\n")
            text = text[0]
        except AttributeError:
            pass
        shelves = {
            "BND02":"Band 0 and 10 dB ampilfier selected",
            "BND00":"Band 0 and -20 dB ampilfier selected",
            "BND01":"Band 0 and THRU ampilfier selected",
            "BND12":"Band 1 and 10 dB ampilfier selected",
            "BND10":"Band 1 and -20 dB ampilfier selected",
            "BND11":"Band 1 and THRU ampilfier selected",
            "BND22":"Band 2 and 10 dB ampilfier selected",
            "BND20":"Band 2 and -20 dB ampilfier selected",
            "BND21":"Band 2 and THRU ampilfier selected",
            "BND32":"Band 3 and 10 dB ampilfier selected",
            "BND30":"Band 3 and -20 dB ampilfier selected",
            "BND31":"Band 3 and THRU ampilfier selected",
            "BND42":"Band 4 and 10 dB ampilfier selected",
            "BND40":"Band 4 and -20 dB ampilfier selected",
            "BND41":"Band 4 and THRU ampilfier selected",
            "BND52":"Band 5 and 10 dB ampilfier selected",
            "BND50":"Band 5 and -20 dB ampilfier selected",
            "BND51":"Band 5 and THRU ampilfier selected",
            "BND62":"Band 6 and 10 dB ampilfier selected",
            "BND60":"Band 6 and -20 dB ampilfier selected",
            "BND61":"Band 6 and THRU ampilfier selected",
            "BND72":"Band 7 and 10 dB ampilfier selected",
            "BND70":"Band 7 and -20 dB ampilfier selected",
            "BND71":"Band 7 and THRU ampilfier selected",
            "BYP2":"Bypass and 10 dB ampilfier selected",
            "BYP0":"Bypass and -20 dB ampilfier selected",
            "BYP1":"Bypass and THRU ampilfier selected",
            "BYP3":"External Switch is now active",
            "LOD":"Unit now in Safety Load State",
            "SLP":"Unit is now in Low Power State"
        }
        index = shelves.keys()
        if text in index:
            context = shelves[text]
            ui.command_output.appendPlainText(context)
        else:
            ui.command_output.appendPlainText(text)
        

if __name__ == "__main__":
    import sys
    version = " (1.5)"
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    trigger = Event()
    textq = Queue(maxsize=1)
    q = Queue(maxsize=1)
    c = ccommands()
    c.daemon = True
    c.start()
    surv = survey()
    surv.daemon = True
    surv.start()
    s = LSCommands()
    sys.exit(app.exec())
