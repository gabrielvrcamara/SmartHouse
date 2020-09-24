import serial
import json
class Comodo:
    def __init__(self, serial, Comodo):
        self.comodo = Comodo
        self.ser = serial
    def corLed(self, red, green, blue):
        a = {"red" : red,
            "green" : green,
            "blue": blue
            }
        a = json.dumps(a)
        self.ser.write(a.encode('utf-8'))
        
    def luz(self, saida_serial):
        self.ser.write(str(chr(saida_serial)).encode('utf-8'))

    def traca(self,saida_serial):
        self.ser.write(str(chr(saida_serial)).encode('utf-8'))

    
    def getStatusLuz(self,status):
        return status[self.comodo]["Status"]
    
    def getItemJson(self,item, status):
        return status[self.comodo][item]
    def getTemperatura(self,status):
        return status[self.comodo]["Temperatura"]
    def getTranca(self,status):
        return status["Tranca"]
    def rStatus(self):
        self.ser.write(str(chr(115)).encode('utf-8'))
        Status = self.ser.readline().decode('utf-8')
        self.ser.flush()
        Status_json = json.loads(Status)
        # print("Arduino: " + str(Status) + "\n")    
        return Status_json
    
    


