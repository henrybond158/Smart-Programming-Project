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

def movement(stuff): sock.send(stuff)
def movement2(drc, spd): sock.send(drc + spd)

def stop():
	print"stop"

#=====> Devices:

def keyboard():
	dev = InputDevice('/dev/input/event0')

	for event in dev.read_loop():
		if event.type == ecodes.EV_KEY:
			key = categorize(event)
			if 'KEY_W' in str(key) and key.keystate == key.key_down: movement2('1','F')
			elif 'KEY_S' in str(key) and key.keystate == key.key_down: movement('\x2F')
			elif 'KEY_A' in str(key) and key.keystate == key.key_down: movement('\x5F')
			elif 'KEY_D' in str(key) and key.keystate == key.key_down: movement('\x6F')
			elif 'KEY_C' in str(key): break
			elif key.key_down == key.key_up: movement('\x00')
			else: movement('\x00')
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
