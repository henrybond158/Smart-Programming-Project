#!/usr/bin/python
import pygtk
import pygame
from pygame.locals import *
pygtk.require('2.0')
import gtk
import os
import wheel
import sys, select, tty, termios, bluetooth, time
from evdev import InputDevice, categorize, ecodes       # Device Input
#from lib import xbox_read                               # Controller Lib

# =====> GUI Class
class Base:
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
	self.menu()
        
        # gtk.main()
    def menu(self):
        os.system(['clear','cls'][os.name == 'nt'])
        menu = {}

        carClass = Car()

        menu['1']=": Keyboard"
        menu['2']=": Wheel"
        menu['3']=": Xbox Controller"
        menu['4']=": Playstation3 Controller"
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
            elif selection == '2': 
            	print '[...] Xbox Controller [...]'
                carClass.controllerXbox()
            elif selection == '2': 
            	print '[...] Playstation3 Controller [...]'
                carClass.controllerPs3()
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
        

    def __init__(self):


        try:
            with open("macFile","r+") as macFile: macaddr = macFile.readline().rstrip("\n")
        except IOError:
            print "[...] MAC address File doesn't seem to Exist [...]"

        self.sock = self.connecting(macaddr)
   
    def moveX(self, st): self.x = st
    def moveY(self, st): self.y = st
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
        print "[...] Connecting to Car [...]"
        try:
            sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            sock.connect((bdr_addr, 1))
            print "[...] Connection Success [...]"
            return sock
        except:
            print "[...] Connection Failed [...]"
            return ''




    ##### Accelerometer #####
    def axelmeter(self, speed):
        self.progbar.set_fraction(speed/11.0)

if __name__ == "__main__":
    base = Base()

    base.main()
