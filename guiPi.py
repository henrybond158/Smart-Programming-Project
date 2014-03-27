#!/usr/bin/python
import pygtk
pygtk.require('2.0')
import gtk
import wheel

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

  def main(self):
    gtk.main()

if __name__ == "__main__":
  base = Base()
  base.main()
