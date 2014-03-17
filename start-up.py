#!/usr/bin/python

#=====> Libraries:

import sys, select, tty, termios, bluetooth, time
from evdev import InputDevice, categorize, ecodes       # Device Input
from controller.lib import xbox_read                # Controller Lib

#======> Car functions:

def connect(bdr_addr, port):
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((bdr_addr, port))
    return sock

def movement(stuff): sock.send(stuff)

def stop(): print"stop"

#=====> Devices:

def keyboard():
    dev = InputDevice('/dev/input/event0')

    for event in dev.read_loop():
        if event.type == ecodes.EV_KEY:
            key = categorize(event)
            if 'KEY_W' in str(key) and (key.keystate == key.key_down or key.keystate == key.key_hold): movement('\x1A')
            if 'KEY_S' in str(key) and (key.keystate == key.key_down or key.keystate == key.key_hold): movement('\x2A')
            if 'KEY_A' in str(key) and (key.keystate == key.key_down or key.keystate == key.key_hold): movement('\x3A')
            if 'KEY_D' in str(key) and (key.keystate == key.key_down or key.keystate == key.key_hold): movement('\x4A')
            if 'KEY_Q' in str(key) and (key.keystate == key.key_down or key.keystate == key.key_hold): movement('\x5A')
            if 'KEY_E' in str(key) and (key.keystate == key.key_down or key.keystate == key.key_hold): movement('\x6A')

            if key.keystate == key.key_up: movement('\x00')
            if 'KEY_ESC' in str(key): break
    print '[...] Stoping Keyboard [...]'
def controllerXbox():
    for event in xbox_read.event_stream(deadzone=12000):
        if event.key == 'A' and event.value == 1: movement('\x1A')
        if event.key == 'X' and event.value == 1: movement('\x2A')
        if event.key == 'dl' and event.value == 1: movement('\x5A')
        if event.key == 'dr' and event.value == 1: movement('\x6A')

        if event.value == 0: movement('\x00')
        if event.key == 'guide': break
def controllerPs3():
    print 'Ps3'

#=====> Starting point:

if __name__ == '__main__':
    try:
        with open("macFile.txt","r+") as macFile:
            macaddr = macFile.readline().rstrip("\n")
            # TODO: go through all theMACs if it fails to connect
    except IOError: #should be unecesary cause "r+" should create a file if it doesn't exist
        print "The MAC file does not seem to exist."

    sock = connect(macaddr,1)

    keyboard()
    sock.close()
    print "[...] Program stopped [...]"
