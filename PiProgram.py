#!/usr/bin/python
import pygtk
import pygame
from pygame.locals import *
pygtk.require('2.0')
import gtk
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
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_size_request(500,300)
        self.mainbox = gtk.VBox()
        self.window.add( self.mainbox)
        
        fixed = gtk.Fixed()
        #button left
        self.button1 = gtk.Button("Left")
        self.button1.connect("clicked", self.left)

        
      
        #fixed.put(self.button1, 20, 50)
        self.mainbox.pack_start(self.button1,expand=False)

        #button cruise
        self.button2 = gtk.Button("Cruise")
        self.button2.connect("clicked", self.cruise)

        fixed.put(self.button2, 55, 50)
        #button forward
        self.button3 = gtk.Button("Forward")
        self.button3.connect("clicked", self.forward)

        fixed.put(self.button3, 50, 20)

        #button right
        self.button4 = gtk.Button("Right")
        self.button4.connect("clicked", self.right)

      
        fixed.put(self.button4, 100, 50)
        #button backwards
        self.button5 = gtk.Button("Backwards")
        self.button5.connect("clicked", self.backwards)

        fixed.put(self.button5, 50, 80)

        #create vbox for radio buttons
      
        radio1 = gtk.RadioButton( None, "Python script")
        self.mainbox.pack_start( radio1, expand=False)
        radio1.show()
        radio1.connect( "toggled", self.selection_changed, "Keyboard")
        for text in ["Wheel","XboxController","PS3 Controller"]:
            radio = gtk.RadioButton( radio1, text)
            self.mainbox.pack_start( radio, expand=False)
            radio.connect( "toggled", self.selection_changed, text)
        radio1.set_active( True)
        # this forces the 'toggled' signal to be emitted 
        radio1.toggled()  
        # show the box
        self.mainbox.show()
        #Prog Bar == Accelerometer
        self.progbar = gtk.ProgressBar()
        fixed.put(self.progbar,140, 50)

        self.window.add(fixed)
        self.window.show_all()
        self.window.connect("destroy",self.destroy)

    def main(self):
        carClass = Car()
        gtk.main()

# =====> Car Class
class Car:

  
    def __init__(self):
        x = 0
        y = 0

        try:
            with open("macFile.txt","w+") as macFile: macaddr = macFile.readline().rstrip("\n")
        except IOError:
            print "[...] MAC address File doesn't seem to Exist [...]"

        sock = self.connecting(macaddr)

        if sock != '': 
            print '[...] Starting up the Car [...]'

        self.keyboard()
   
    def moveX(self, st): x = st
    def moveY(self, st): y = st
    def move(self, spd):
        arra = [[5,1,6], [3,0,4], [7,2,8]]
        #sock.send(chr((dir * arra[y + 1][x + 1]) + spd));
        print " >> " +  str(dir * arra[y + 1][x + 1]) + " - " + spd
        axelmeter(spd)

    
    #def keyboard(self):
     #   try:
      #      dev = InputDevice('/dev/input/event0')
#
 #           for event in dev.read_loop():
  #              if event.type == ecodes.EV_KEY:
   #                 key = categorize(event)
#
 #                   if 'KEY_W' in str(key) and (key.keystate == key.key_down): moveY(1)
  #                  if 'KEY_S' in str(key) and (key.keystate == key.key_down): moveY(-1)
   #                 if 'KEY_A' in str(key) and (key.keystate == key.key_down): moveX(-1)
    #                if 'KEY_D' in str(key) and (key.keystate == key.key_down): moveX(1)
#
 #                   if (key.keystate != key.key_hold): move(15)
  #                  if 'KEY_ESC' in str(key): break
   #                 
    #        print '[...] Stoping Keyboard [...]'
     #   except:
      #      print '[...] Error With Keyboard [...]'
    def keyboard(self):
        print 'hit the keyboard'
        pygame.event.pump()
        while True:
            pygame.event.pump()
            self.pressed = pygame.key.get_pressed()

            if self.pressed[K_UP]: self.moveY(1)
            if self.pressed[K_DOWN]: self.moveY(-1)
            if self.pressed[K_LEFT]: self.moveX(1)
            if self.pressed[K_RIGHT]: self.moveX(-1)

            if self.pressed[KEY_ESC]: break

            move(15)
    def connecting(self,bdr_addr):
        try:
            sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            sock.connect((bdr_addr, port))
            return sock
        except:
            return ''


    def controllerXbox(self):
        print '[...] Xbox Controller [...]'
        try:
            for event in xbox_read.event_stream(deadzone=12000):

                if event.key == 'Y1' and event.value > 1: moveY(1)
                if event.key == 'Y1' and event.value < 1: moveY(-1)
                if event.key == 'X1' and event.value > 1: moveX(1)
                if event.key == 'X1' and event.value < 1: moveX(-1)

                move((int(event.value) /2200))
        except:
            print '[...] Error With Controller [...]'
    def controllerPs3(self):
        print '[...] Ps3 Controller [...]'

    ##### Accelerometer #####
    def axelmeter(self, speed):
        self.progbar.set_fraction(speed/11.0)

if __name__ == "__main__":
       base = Base()
    
    wheelClass = wheel.WheelClass()
    array=wheelClass.getMov

    base.main()
