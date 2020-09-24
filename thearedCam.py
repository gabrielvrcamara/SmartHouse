import multiprocessing
import os, time
from camera import VideoCamera

class ThearedCam:
    def __init__(self, q):
        self.status = False
        self.V = VideoCamera(Q=q)
        self.p = None
        self.q = q
        self.rec = False

    def recCam(self, rec):
        self.rec = rec

    def getStatus(self):
        return self.status

    def getRec(self):
        return self.rec

    def hang(self):
        self.V.Video_Start()
        while self.status:
            self.V.get_frame(self.rec)
            
    def start(self):
        print("self.p:  " + str(self.p))
        if self.p == None:
            self.p = multiprocessing.Process(target=self.hang)
            self.status = True
            self.p.start()
            print(" --- " + str(self.p.pid))
            return True
        else:
            return "Start Thread Erro"

    def close(self):
        if self.p != None and self.p.is_alive():
            self.status = False
            print(self.p.is_alive())
            self.p.terminate()
            os.kill(self.p.pid, 9)
            time.sleep(0.5)
            print(self.p.is_alive())
            if not self.p.is_alive():
                del self.p 
                self.p = None
                return True
            
        else:
            return "Close Thread Erro"
