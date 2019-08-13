#!/usr/bin/env python3

from light import Light
from time import sleep

if __name__ == '__main__':
	l = Light(4, 0.0, 0.5)
	l.on()
	sleep(1000)
	l.off()	
