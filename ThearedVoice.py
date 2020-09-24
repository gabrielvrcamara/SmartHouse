import multiprocessing
import os, time

class ThearedVoice:
    def __init__(self):
        self,status = False
        self.process = None

    def hang(self):
        while self.status:
            


    def start(self):
        if self.process == None:
            self.process = multiprocessing.Process(target=self.hang)