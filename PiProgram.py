#!/usr/bin/python
import pygtk
pygtk.require('2.0')
import gtk
import wheel
import sys, select, tty, termios, bluetooth, time
from evdev import InputDevice, categorize, ecodes       # Device Input
from lib import xbox_read                               # Controller Lib

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

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_size_request(500,300)
        fixed = gtk.Fixed()
        #button left
        self.button1 = gtk.Button("Left")
        self.button1.connect("clicked", self.left)

        
      
        fixed.put(self.button1, 20, 50)

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

        #Prog Bar == Accelerometer
        self.progbar = gtk.ProgressBar()
        fixed.put(self.progbar,140, 50)

        self.window.add(fixed)
        self.window.show_all()
        self.window.connect("destroy",self.destroy)

    def main(self):
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

        sock = connecting(macaddr)

        if sock != '': 
            print '[...] Starting up the Car [...]'
            
    def connecting(self,bdr_addr):
        try:
            sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            sock.connect((bdr_addr, port))
            return sock
        except:
            return ''

    def moveX(self, st): x = st
    def moveY(self, st): y = st
    def move(self, spd):
        arra = [[5,1,6], [3,0,4], [7,2,8]]
        sock.send(chr((dir * arra[y + 1][x + 1]) + spd))
        x = 0
        y = 0
        axelmeter(spd)

    
    def keyboard(self):
        try:
            dev = InputDevice('/dev/input/event0')

            for event in dev.read_loop():
                if event.type == ecodes.EV_KEY:
                    key = categorize(event)

                    if 'KEY_W' in str(key) and (key.keystate == key.key_down): moveY(1)
                    if 'KEY_S' in str(key) and (key.keystate == key.key_down): moveY(-1)
                    if 'KEY_A' in str(key) and (key.keystate == key.key_down): moveX(-1)
                    if 'KEY_D' in str(key) and (key.keystate == key.key_down): moveX(1)

                    if (key.keystate != key.key_hold): move(15)
                    if 'KEY_ESC' in str(key): break
                    
            print '[...] Stoping Keyboard [...]'
        except:
            print '[...] Error With Keyboard [...]'
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
        progbar.set_fraction(speed/11.0)

if __name__ == "__main__":
    base = Base()
    
    wheel = Wheel()

    base.main()