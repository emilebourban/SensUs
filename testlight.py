#!/usr/bin/env python3

from light import Light
from time import sleep

if __name__ == '__main__':
	l = Light(6, 4, 0.4)
	l.on()
	sleep(1000)
	l.off()	
