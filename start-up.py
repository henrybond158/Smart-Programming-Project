#!/usr/bin/python

#=====> Libraries:

import sys, select, tty, termios, bluetooth, time
from evdev import InputDevice, categorize, ecodes		# Device Input
#from controller.lib import xbox_read				# Controller Lib

#======> Car functions:

def connect(bdr_addr, port):
	sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
	sock.connect((bdr_addr, port))
	return sock

def movement(dirct, speed):
	print str(bytes('0/' + dirct + speed))
	sock.send(bytes(dirct + speed))
	#time.sleep(0.035)
	time.sleep(1)

def stop():
	print"stop"

#=====> Devices:

def keyboard():
	dev = InputDevice('/dev/input/event0')

	for event in dev.read_loop():
		if event.type == ecodes.EV_KEY:
			key_pressed = str(categorize(event))
			if 'KEY_W' in key_pressed:
				movement('1','F')
			if 'KEY_S' in key_pressed:
				movement('2','F')
			if 'KEY_A' in key_pressed:
				movement('5','F')
			if 'KEY_D' in key_pressed:
				movement('6','F')
			if 'KEY_SPACE' in key_pressed:
				movement('0','0')
			if 'KEY_ESCAPE' in key_pressed:
				break
	print '[...] Stoping Keyboard [...]'

def controllerXbox():

	for event in xbox_read.event_stream(deadzone=12000):
		print event

#=====> Starting point:

if __name__ == '__main__':
	sock = connect("00:12:05:09:94:45",1)
	keyboard()
	sock.close()
	print "[...] Program stopped [...]"
