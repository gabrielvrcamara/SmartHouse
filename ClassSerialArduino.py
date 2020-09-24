import serial
import json
class Arduino:
    def __init__(self):
        self.ser = None
    def conectar(self):
        print("Conectando Hardware")
        for i in range(3):
                print(".")
        portas = self.search_Port()
        if len(portas) == 1:
                porta = portas[0]
                print("Serial detectado.")
                print("Conectando...")
        else:
                pass
        velSaida = 115200
        try:
                print(porta)
                self.ser = serial.Serial(porta,velSaida)
                print(type(self.ser))
                print("Serial conectado...")
        except:
                print ("Nao conectado")
        return self.ser

    def search_Port(self):
        
        list_port = []
        cont = 0
        print("Procurando portas...")
        while(cont < 10):
                ports = "/dev/ttyACM"
                ports = ports + "{}".format(cont)
                try:
                        ser = serial.Serial(ports,9600,timeout = 1)
                        list_port.append(ports)
                        ser.close()
                except:
                        pass
                cont +=1
        print("Lista de Portas:")
        for cont, i in enumerate(list_port,1):
                print(str(cont) + "-" + i)      
        print("")
        return list_port


