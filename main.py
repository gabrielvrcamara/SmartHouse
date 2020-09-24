
from flask import Flask, render_template, Response
from flask_socketio import SocketIO ,send, emit
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from camera import VideoCamera
import multiprocessing
import time, os
import json
from thearedCam import ThearedCam
import subprocess
import ClassComodo
import ClassSerialArduino
from flask import jsonify
from flask import send_from_directory, abort
from ClassControl import Controle
import colorsys
import psutil
ser = ClassSerialArduino.Arduino().conectar()

Quarto = ClassComodo.Comodo(ser,"Quarto") 
Closet = ClassComodo.Comodo(ser,"Closet")
Banheiro = ClassComodo.Comodo(ser,"Banheiro")
Control = Controle(ser)
#
# Retorna Json
#
def updateStatus():
    while True:
        status = Quarto.rStatus() 
        porta = lambda x: True if (x == 180) else False 
        try:
            array = {
                "Quarto":{
                        'Temp': int(Quarto.getTemperatura(status)), 
                        "Status": bool(Quarto.getStatusLuz(status)),
                        "Tranca": porta(Quarto.getTranca(status)),
                        "Luminaria": bool(Quarto.getItemJson("Luminaria",status)),
                        "Camera":{
                            "Ligada" : bool(theared.getStatus()),
                            "Gravar" : bool(theared.getRec())
                        }
                },
                "Closet":{
                        "Status": bool(Closet.getStatusLuz(status)) 
                },
                "Banheiro":{
                        "Status": bool(Banheiro.getStatusLuz(status))
                },
                "Servidor":{
                    "Cpu":{
                        "Porcentagem": psutil.cpu_percent(),
                        "Atual": "%.1f" % psutil.cpu_freq().current,
                        "Min": psutil.cpu_freq().min,
                        "Max": psutil.cpu_freq().max
                    },
                "Memoria" :{
                    "Total" : psutil.virtual_memory().total,
                    "Usado" : psutil.virtual_memory().used,
                    "Porcentagem" : psutil.virtual_memory().percent

                }
                }
            }
            break
        except:
            print("Erro Status")
            pass

    json = json.dumps(array)
    return json


app = Flask(__name__, static_folder='static')
auth = HTTPBasicAuth()

Q = multiprocessing.Queue()
theared = ThearedCam(Q)

x = 0

@app.route('/')
def index():
    return render_template('index.html')


#
# Liga e desliga as luzes
#

@app.route('/Quarto')
def quarto():
    print ('/Quarto')
    Quarto.luz(1)
    return "Quarto"

@app.route('/Closet')
def closet():
    print ('/Closet')
    Closet.luz(2)
    return "Closet"

@app.route('/Banheiro')
def banheiro():
    print ('/Banheiro')
    Banheiro.luz(3)
    return "Banheiro"


@app.route('/Luminaria')
def luminaria():
    print ('/Luminaria')
    Quarto.luz(5)
    return "Luminaria"

@app.route('/Cor/<hue>/')
def cor(hue):
    r, g ,b = HSLToRGB(float(hue),100,50)
    print ('/Cor')
    Quarto.luz(6)
    print(255 - r, 255 - g, 255 - b)
    Quarto.corLed(255 - r, 255 - g, 255 - b)
    return "Cores red: "+ str(r) + " green: " + str(g) + " blue: " + str(b) 

x

@app.route('/Cor/Colorido')
def colorido():
    print ('/Cor/Colorido')
    Quarto.luz(7)
    return "Colorido"

#
# Tranca 
#

@app.route('/Tranca')
def tranca():
    print ('/Tranca')
    Quarto.traca(4)
    return "Tranca"

#
#   Controle Sky
#

@app.route('/Controle/sky/power')
def controleskypower():
    print ('/Controle/sky/power')
    Control.control(200)
    return "Controle/sky/power"
@app.route('/Controle/sky/ch+')
def controleskychUp():
    print ('/Controle/sky/ch+')
    Control.control(201)
    return "Controle/sky/ch+"    
@app.route('/Controle/sky/ch-')
def controleskychDown():
    print ('/Controle/sky/ch-')
    Control.control(202)
    return "Controle/sky/ch-"    
@app.route('/Controle/sky/vol+')
def controleskyVolUp():
    print ('/Controle/sky/vol+')
    Control.control(203)
    return "Controle/sky/sky/vol+"  
@app.route('/Controle/sky/vol-')
def controleskyVolDown():
    print ('/Controle/sky/vol-')
    Control.control(204)
    return "Controle/sky/sky/vol-" 
@app.route('/Controle/sky/mute')
def controleskyMute():
    print ('/Controle/sky/mute')
    Control.control(205)
    return "Controle/sky/sky/mute" 
@app.route('/Controle/sky/retornar')
def controleskyRetornar():
    print ('/Controle/sky/retornar')
    Control.control(206)
    return "Controle/sky/sky/retornar" 
@app.route('/Controle/sky/info')
def controleskyInfo():
    print ('/Controle/sky/info')
    Control.control(207)
    return "Controle/sky/sky/info" 
@app.route('/Controle/sky/plus')
def controleskyPlus():
    print ('/Controle/sky/plus')
    Control.control(208)
    return "Controle/sky/sky/plus" 

#
# retorna Status
#

@app.route('/Status')
def status():
    jsonTemp = updateStatus()
    print("Server: " + jsonTemp)
    return jsonTemp

#
# Camera
#

def gen():
    while True:
        frame = Q.get()
        frame = VideoCamera().get_frame_jpg(frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

#
# Liga e desliga Camera
#

@app.route('/Cam/<status>')
def ligaCam(status):
    if status == "On":
        a = theared.start()
        if a:
            print("Ligando Camera 1")
    elif status == "Off":
        a = theared.close()
        if a: 
            print("Desligando Camera 1")

    return str(status) + " -- " + str(a)

#
# Liga e desliga gravação
#
@app.route('/Cam/rec/<status>')
def recCam(status):
    if status == "True":
        if theared.getStatus:
            theared.close()
            theared.recCam(True)
            theared.start()
    else:
        theared.close()
        theared.recCam(False)
        theared.start()
    return str(status)

@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/movies')
def movies():
    lista = os.listdir("static")
    return json.dumps(lista)
    
@app.route("/get-movies/<path:movie_name>")
def getMovies(movie_name):
    try:
        return send_from_directory(app.config["CLIENT_MOVIES"], filename=movie_name)
    except FileNotFoundError:
        print("error 404")
        abort(404)

#
# Converte cores HSL para RGB
#
def HSLToRGB(h,s,l):
    s = s/100
    l = l/100
    c = (1 - abs(2 * l - 1)) * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = l - c/2
    r = 0
    g = 0 
    b = 0
    if (0 <= h and h < 60):
        r = c
        g = x
        b = 0
    elif (60 <= h and h < 120):
        r = x
        g = c
        b = 0
    elif (120 <= h and h < 180):
        r = 0
        g = c
        b = x
    elif (180 <= h and h < 240):
        r = 0 
        g = x 
        b = c
    elif (240 <= h and h < 300):
        r = x 
        g = 0 
        b = c
    elif (300 <= h and h < 360):
        r = c
        g = 0
        b = x
    r = round((r + m) * 255)
    g = round((g + m) * 255)
    b = round((b + m) * 255)

    return (r,g,b)

if __name__ == '__main__':
    app.run(host='192.168.1.206', debug=True)
