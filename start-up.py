#!/usr/bin/python

#=====> Libraries:

import sys, select, tty, termios, bluetooth, time
from evdev import InputDevice, categorize, ecodes       # Device Input
from lib import xbox_read                				# Controller Lib

#======> Car functions:

def connect(bdr_addr, port):
	try:
	    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
	    sock.connect((bdr_addr, port))
	    return sock
	except:
		return ''

def move(dir, spd):
	if (dir < 15) or (spd < 15):
		sock.send(chr((dir*16) + spd))

#=====> Devices:

def keyboard():
    dev = InputDevice('/dev/input/event0')

    for event in dev.read_loop():
        if event.type == ecodes.EV_KEY:
            key = categorize(event)

            if 'KEY_W' in str(key) and (key.keystate == key.key_down): move(1,15)
            if 'KEY_S' in str(key) and (key.keystate == key.key_down): move(2,15)
            if 'KEY_A' in str(key) and (key.keystate == key.key_down): move(3,15)
            if 'KEY_D' in str(key) and (key.keystate == key.key_down): move(4,15)
            if 'KEY_Q' in str(key) and (key.keystate == key.key_down): move(5,15)
            if 'KEY_E' in str(key) and (key.keystate == key.key_down): move(6,15)

            if (! key.keystate == key.key_hold): move(0,0)
            if 'KEY_ESC' in str(key): break

    print '[...] Stoping Keyboard [...]'
def controllerXbox():
    try:
        for event in xbox_read.event_stream(deadzone=12000):

            # Must build in truning and moving

            if event.key == 'Y1' and event.value > 1: move(1,(int(event.value) /2200))
            if event.key == 'Y1' and event.value < 1: move(2,(int(event.value) /2200))
            if event.key == 'X1' and event.value > 1: move(5,(int(event.value) /2200))
            if event.key == 'X1' and event.value < 1: move(6,(int(event.value) /2200))
    except:
        print '[...] Error With Controller [...]'
def controllerPs3():
	for event in xbox_read.event_stream(deadzone=12000):
		print event

#=====> Starting point:

if __name__ == '__main__':
	try:
		with open("macFile.txt","r+") as macFile:
			macaddr=macFile.readline().rstrip("\n")
			print macaddr
		# TODO: go through all theMACs if it fails to connect
	except IOError: #should be unecesary cause "r+" should create a file if it doesn't exist
		print "[...] MAC address File doesn't seem to Exist [...]"

    sock = connect(macaddr,1)
    if sock == '':
    	print '[...] Error When Connecting to Car [...]'
	else:
		controllerPs3()
    	sock.close()

    print "[...] Program stopped [...]"