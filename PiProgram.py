#!/usr/bin/python
import pygtk
import pygame
from pygame.locals import *
pygtk.require('2.0')
import gtk
import os
import wheel
import sys, select, tty, termios, bluetooth, time
from evdev import InputDevice, categorize, ecodes # Device Input
#from lib import xbox_read # Controller Lib

# =====> GUI Class

class Base(gtk.Window):

    def destroy(self, widget, data=None):
        print('you closed the window')
        gtk.main_quit()
    def forward(self, widget, data=None):
        print('you click the forward button')
    def backwards(self, widget, data=None):
        print('you clicked the back button')
    def left(self, widget, data=None):
        print('you clicked the left button')
    def right(self, widget, data=None):
        print('you clicked the right button')
    def cruise(self, widget, data=None):
        print("you be crusing")
    def selection_changed(self, widget, data=None):
        print ("keyboard selected")
    def xboxController(self, widget, data=None):
        print ("xbox selected")
    def wheelController(self, widget, data=None):
        print("wheel selected")
    def selection_changed( self, w, data=None):
        self.label.set_label( "Current selection: <b>%s</b>" % data)

    def __init__(self):
        os.system(['clear','cls'][os.name == 'nt'])
        menu = {}

        print "[...] Connecting to the Car [...]"

        if Car().test("00:12:05:09:94:45"):
            print "[...]\033[92m Connection Successful \033[0m[...]"
        else:
            print "[...]\033[91m Connection Failed \033[0m [...]"


        carClass = Car()
        carClass.connecting("00:12:05:09:94:45")

        menu['1']=": Keyboard"
        menu['2']=": Wheel"
        menu['3']=": Xbox Controller"
        menu['4']=": Playstation3 Controller"
        menu['m']=": Change the Mac Address"
        menu['q']=": Quit"

        while True: 
            print "[...] Menu [...]\n"
            options=menu.keys()
            options.sort()

            for entry in options: 
                print "\t" + entry, menu[entry]

            selection=raw_input("\nPlease Select: ") 
            os.system(['clear','cls'][os.name == 'nt'])

            if selection == '1': 
                print '[...] Keyboard [...]'
                carClass.keyboard()
            elif selection == '2': 
                print '[...] Wheel [...]'
                carClass.wheelHandler()
            elif selection == '3': 
                print '[...] Xbox Controller [...]'
                carClass.controllerXbox()
            elif selection == '4': 
                print '[...] Playstation3 Controller [...]'
                carClass.controllerPs3()
            elif selection == 'm':
                self.getMacAddress(True)
            elif selection == 'q':
                break
            else: 
                print "Unknown Option Selected!"
                time.sleep(1)

# =====> Car Class
class Car:
    x = 1
    y = 1
    last = 0
    wheelClass = wheel.WheelClass()

    #def __init__(self):


    def moveX(self, st): self.x = st
    def moveY(self, st): self.y = st
    def moveXY(self, xBit, yBit, spd, time):
    	self.x = xBit
    	self.y = yBit
    	self.move(spd)
    	time.sleep(time)

    def move(self, spd):
        arra = [[5,1,6], [3,0,4], [7,2,8]]
        ch = (16 * arra[self.y][self.x]) + spd
        if self.last != ch:
            self.sock.send(chr(ch))
            self.last = ch

    def keyboard(self):
        # loop around each key press
        while True:
        # Starts pulling keyboard inputs from pygame
            pygame.event.pump()
        # Sets keyboard inputs to a variable
            self.pressed = pygame.key.get_pressed()

        # if either the up/down button is pressed, set the Y axes to
            if self.pressed[K_UP]: self.moveY(0)
            elif self.pressed[K_DOWN]: self.moveY(2)
            else: self.moveY(1)

        # if either the left/right button is pressed, set the X axes to
            if self.pressed[K_LEFT]: self.moveX(0)
            elif self.pressed[K_RIGHT]: self.moveX(2)
            else: self.moveX(1)

        # Will run the move function, move with set the X/Y vars and move the car accordingly
            self.move(8)
        # If the escape key is pressed, exit
            if self.pressed[K_ESCAPE]: break
    def controllerXbox(self):
        # Will catch errors
        try:
        # loop around xbox events
            for event in xbox_read.event_stream(deadzone=12000):

            # if either the up/down button is pressed, set the Y axes to
                if event.key == 'Y1' and event.value > 1: self.moveY(2)
                elif event.key == 'Y1' and event.value < 1: self.moveY(0)
                else: self.moveY(1)

            # if either the left/right button is pressed, set the X axes to
                if event.key == 'X1' and event.value > 1: self.moveX(2)
                elif event.key == 'X1' and event.value < 1: self.moveX(0)
                else: self.moveX(1)

                move((int(event.value) /2200))
        except:
            print '[...] Error With Controller [...]'
    def controllerPs3(self):
        print '[...] Ps3 Controller [...]'
    def wheelHandler(self):
        while True:
            direction,turning,speed=self.wheelClass.getMov()
            self.y = direction
            self.x = turning
            self.move(speed)

    def connecting(self,bdr_addr):
        try:
            self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            self.sock.connect((bdr_addr, 1))
            return sock
        except: return ''
    def test(self,mac):
        try:
            testSock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            testSock.connect((mac, 1))

            testSock.close()
            time.sleep(.5)
            return True
        except:
            return False

    ##### Accelerometer #####
    def axelmeter(self, speed):
        self.progbar.set_fraction(speed/11.0)
class PreSetFunctions:
	def threePointTurn(self):
		moveXY(1, 2, 10, 1)		# backwards
		moveXY(2, 2, 10, 1.5)	# backwards, right
		moveXY(0, 0, 10, 1.5)	# forward, left
		moveXY(1, 0, 10, 1)		# forward

	def rightCircle(self):
		moveXY(2, 0, 10, 10)	# forward right
	def leftCircle(self):
		moveXY(0, 0, 10, 10)	# forward left
	def eigth(self):
		moveXY(2, 0, 10, 4)		# forward right
		moveXY(1, 0, 10, .2)	# forward
		moveXY(0, 0, 10, 10)	# forward left
		moveXY(1, 0, 10, .2)	# forward

if __name__ == "__main__":
    Base()