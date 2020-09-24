import serial
class Controle:
    def __init__(self, serial):
        self.ser = serial
    def control(self, saida_serial):
        self.ser.write(str(chr(saida_serial)).encode('utf-8'))
