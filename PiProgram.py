#!/usr/bin/python
import pygtk
pygtk.require('2.0')
import gtk
import wheel
import sys, select, tty, termios, bluetooth, time
from evdev import InputDevice, categorize, ecodes       # Device Input
from lib import xbox_read                               # Controller Lib


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



    self.window.add(fixed)
    self.window.show_all()
    self.window.connect("destroy",self.destroy)
  def connecting(self,bdr_addr):
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((bdr_addr,1))
    return sock
    def move(dir, spd): sock.send(chr((dir*16) + spd))
  def controllerXbox(self):
    try:
        for event in xbox_read.event_stream(deadzone=12000):

            # Must build in truning and moving

            if event.key == 'Y1' and event.value > 1: move(1,(int(event.value) /2200))
            if event.key == 'Y1' and event.value < 1: move(2,(int(event.value) /2200))
            if event.key == 'X1' and event.value > 1: move(5,(int(event.value) /2200))
            if event.key == 'X1' and event.value < 1: move(6,(int(event.value) /2200))
    except:
        print '[...] Error With Controller [...]'

    def keyboard(self):
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

  def main(self):
    gtk.main()

  
if __name__ == "__main__":
    base = Base()
    try:
        with open("macFile.txt","r+") as macFile:
            macaddr=macFile.readline().rstrip("\n")
            print macaddr
        # TODO: go through all theMACs if it fails to connect
    except IOError: #should be unecesary cause "r+" should create a file if it doesn't exist
        print "The MAC file does not seem to exist."

    # sock = base.connecting("00:12:05:09:97:76")
    sock = base.connecting(macaddr)


    wheel = Wheel()

    
    base.main()
