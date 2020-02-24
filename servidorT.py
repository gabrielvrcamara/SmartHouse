from http.server import HTTPServer, BaseHTTPRequestHandler
import serial
import json
import os
def search_Port():
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
        
        
print("Iniciando Servidor")
for i in range(3):
        print(".")
portas = search_Port()
if len(portas) == 1:
        porta = portas[0]
        print("Serial detectado.")
        print("Conectando...")
else:
        #CONTINUAR      
        pass
velSaida = 115200
try:
        ser = serial.Serial(porta,velSaida)
        print("Serial conectado...")
except:
        print ("Nao conectado")


class StaticServer(BaseHTTPRequestHandler):
 
    def do_GET(self):
        print(self.path)
        if self.path == "/Quarto":
	        ser.write(b'1')
        elif self.path == "/Closet":
                ser.write(b'3')
        elif self.path == "/Banheiro":
                ser.write(b'5')
        self.send_response(200)
        self.end_headers ()
        if self.path == "/Status":
                ser.write(b's')
                Status_Room = ser.readline().decode('utf-8')
                ser.flush()
                print("--Status--")
                print(Status_Room)
                self.flush_headers()
                if int(Status_Room) == 1:
                        print("1 -- LUZ: ON")
                        Status_Room = True
                elif  int(Status_Room) == 0:
                       print("0 -- LUZ: OFF")
                       Status_Room = False
                else:
                        print("--------------------")
                        print("- Retorno Invalido -")
                        print("--------------------")
                        
                ser.write(b'4')
                Temperatura = ser.readline().decode('utf-8')
                self.flush_headers()
                array = {
                        "Quarto":{
                                'tempQuarto': int(Temperatura), 
                                "statusQuarto": bool(Status_Room) 
                        },
                        "Closet":{
                                'tempCloset': None , 
                                "statusCloset": None , 
                        },
                        "Banheiro":{
                                'tempBanheiro': None , 
                                "statusBanheiro": None
                        }

                        }
                jsonTemp =  json.dumps(array)
                print(jsonTemp)
                self.wfile.write(str.encode(jsonTemp))
                
        if self.path == "/Test":
                self.wfile.write(b'1')

 
def run(server_class=HTTPServer, handler_class=StaticServer, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd on port {}'.format(port))
    httpd.serve_forever()
 
run()
