#!/usr/bin/python

import sys, select, tty, termios, bluetooth, time
from evdev import InputDevice, categorize, ecodes


def connect(bdr_addr, port):
	
	sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
	sock.connect((bdr_addr, port))

	return sock	
	
	
	
def movement(dir, speed):

	print "this is where the movement happens"


def stop(sock):
	sock.send('\x00')
	sock.close()
	print 'Stopping Car...'
	
if __name__ == '__main__':

	dev = InputDevice('/dev/input/event0')
	sock = connect("00:12:05:09:92:74",1)
	
	for event in dev.read_loop():
		if event.type == ecodes.EV_KEY:
			key_pressed = str(categorize(event))
			if 'KEY_W' in key_pressed:
				sock.send('\x1F')
				time.sleep(0.035)
			if 'KEY_S' in key_pressed:
                                sock.send('\x2F')
                                time.sleep(0.035)
			if 'KEY_A' in key_pressed:
                                sock.send('\x5F')
                                time.sleep(0.035)
			if 'KEY_D' in key_pressed:
                                sock.send('\x6F')
                                time.sleep(0.035)
			if '' in key_pressed:
				sock.send('\x00')

