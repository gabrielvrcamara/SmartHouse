import cv2, time
import numpy as np
from datetime import datetime 
import json
import multiprocessing
import os

ds_factor=1.0

class VideoCamera(object):
    def __init__(self, Q=None):
        self.static_back = None
        self.motion_list = [ None, None ] 
        self.gravar = False
        self.on = True
        self.startRec = False
        self.video = None
        self.out = None
        self.Q = Q
        self.stop = False
        self.inicioMin = ""
        self.inicioSeg = ""
        self.time = 0
        self.nome = ""


    
    def delete(self):
        self.video.release()
    
    def Video_Start(self):
        self.video = cv2.VideoCapture(0)
    def out(self, image):
        self.Q.put(image)

    def get_frame(self, rec):
        self.startRec = rec
        frame_width = int(self.video.get(3))
        frame_height = int(self.video.get(4))

        success, image = self.video.read()
        # rotacao
        altura, largura = image.shape[:2]
        ponto = (largura / 2, altura / 2)
        rotacao = cv2.getRotationMatrix2D(ponto, 180, 1.0)
        image = cv2.warpAffine(image, rotacao, (largura, altura))
        # clareamento
        image= cv2.add(image,np.array([80.0]))

        image=cv2.resize(image,None,fx=ds_factor,fy=ds_factor,interpolation=cv2.INTER_AREA)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 


        motion = 0

        # Converting gray scale image to GaussianBlur 
		# so that change can be find easily 
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 

        # Converting gray scale image to GaussianBlur 
        # so that change can be find easily 
        gray = cv2.GaussianBlur(gray, (21, 21), 0) 

        # In first iteration we assign the value 
        # of static_back to our first frame 
        if self.static_back is None: 
            self.static_back = gray
            # continue

        # Difference between static background 
        # and current frame(which is GaussianBlur) 
        diff_frame = cv2.absdiff(self.static_back, gray) 

        # If change in between static background and 
        # current frame is greater than 30 it will show white color(255) 
        thresh_frame = cv2.threshold(diff_frame, 10, 255, cv2.THRESH_BINARY)[1] 
        thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2) 

        # # Finding contour of moving object 
        _ ,cnts, hierarchy = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # cnts = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in cnts: 
            if cv2.contourArea(contour) < 10000: 
                continue
            motion = 1

            (x, y, w, h) = cv2.boundingRect(contour) 
            # making green rectangle arround the moving object 
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Appending status of motion 
        self.motion_list.append(motion) 
        self.motion_list = self.motion_list[-2:]         # Appending Start time of motion

        self.Q.put(image)
        # self.out(image=image)
        if self.startRec: 
            # print(self.startRec)

            if self.motion_list[-1] == 1 and self.motion_list[-2] == 0: 
                data = datetime.now()
                print("Iniciando Gravacao :" + str(data))
                self.time = 0
                fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
                nomeArray = list(str(data))
                nome = ""
                for i in nomeArray:
                    if i == ":" or i == ".":
                        i = "_"
                    nome += i
                nome = nome.split()
                self.nome = nome[0] + "_" + nome[1]

                self.out = cv2.VideoWriter("Videos/" + nome +'.avi',fourcc, 10, (frame_width,frame_height))
                self.gravar = True
            if(self.gravar):
                # print("gravando")
                self.out.write(image)
            # Appending End time of motion 
            if self.motion_list[-1] == 0 and self.motion_list[-2] == 1:
                print(2)
                self.inicioMin = datetime.now().strftime('%M')
                self.inicioSeg = datetime.now().strftime('%S')
                self.stop = True


            if(self.stop):
                print("Finalizando gravacao")

                if(int(datetime.now().strftime('%M')) > int(self.inicioMin)):
                    print("Finalizacao de gravacao")
                    self.gravar = False
                    self.stop = False

                else:      
                    if int(datetime.now().strftime('%S')) > self.time:
                        print(int(datetime.now().strftime('%S')))
                    x = int(datetime.now().strftime('%S')) - int(self.inicioSeg)
                    if x < 0:
                        x *= -1
                    if x >= 30:
                        print("Finalizacao de gravacao")
                        self.gravar = False
                        self.stop = False
                        self.convert_avi_to_mp4("Videos/"+self.nome + ".avi", "static/" + self.nome)
                    self.time = int(datetime.now().strftime('%S'))

            

    def get_frame_jpg(self, image):
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    
    def convert_avi_to_mp4(avi_file_path, output_name):
        os.popen("ffmpeg -i '{input}' -ac 2 -b:v 2000k -c:a aac -c:v libx264 -b:a 160k -vprofile high -bf 0 -strict experimental -f mp4 '{output}.mp4'".format(input = avi_file_path, output = output_name))
        return True