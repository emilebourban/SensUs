#!/usr/bin/env python3
#Application.run() créera une machine avec toutes les param (capture)
from light import Light
from time import sleep
from gui import kleinapp
#from camera import Camera



class Machine:

    def __init_(self):
        self.light = Light(6, 4, 0.4)
        self.kleinapp

    def get_stream(self):
        self.light.on()
        sleep(10)
        self.kleinapp.reintialise()

    def get_detectionSpot(self):

    def get_measure(self):
        self.kleinapp
        self.light.off()

    def release(self):
