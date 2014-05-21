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

import gobject
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
		super(Base, self).__init__()

		if Car().test("00:12:05:09:94:45"):
			print "[...]\033[92m Connection Successful \033[0m[...]"
		else:
			print "[...]\033[91m Connection Failed \033[0m [...]"


		carClass = Car()
		carClass.connecting("00:12:05:09:94:45")

		WINX = 300
		WINY = 200

		self.set_title("Car GUI")
		self.set_size_request(WINX, WINY)
		self.set_position(gtk.WIN_POS_CENTER)
		self.set_resizable(False)


		# Creating the buttons and other widgets
		btn3Turn = gtk.Button("3-P Turn")
		btnMenu = gtk.Button("Menu")
		btnCruise = gtk.Button("Cruise")
		btnSpazz = gtk.Button("Random")
		btnStop = gtk.Button("STOP!!!")

		self.progbar = gtk.ProgressBar()
		self.progbar2 = gtk.ProgressBar()

		frame = gtk.Frame("Car's Movement")

		lblAction = gtk.Label("<b>The car is moving / action /</b>")
		lblAction.set_justify(gtk.JUSTIFY_CENTER)
		lblAction.set_size_request(235,60)
		lblAction.set_use_markup(True)

		frame.set_label_align(0.5,0.5)
		frame.add(lblAction)
		

		#setting size
		btnSpazz.set_size_request(80,30)
		btnCruise.set_size_request(80, 30)
		btnMenu.set_size_request(80, 40)
		btn3Turn.set_size_request(80, 30)
		btnStop.set_size_request(80,30)

		fixed = gtk.Fixed()
		self.progbar.set_orientation(gtk.PROGRESS_BOTTOM_TO_TOP)
		self.progbar2.set_orientation(gtk.PROGRESS_BOTTOM_TO_TOP)
		fixed.put(frame, 30,10)

		# positioning the widgets
		fixed.put(btnCruise ,110 ,110)
		fixed.put(btnSpazz ,210 ,110)
		fixed.put(btnMenu ,10 , 110)
		fixed.put(btn3Turn ,210 , 160)
		fixed.put(btnStop,110, 160)
		fixed.put(self.progbar,10, 10)
		fixed.put(self.progbar2,275, 10)

		self.add(fixed)
		self.realize()
		print '1'

		self.connect("destroy", gtk.main_quit)

		# Force SDL to write on our drawing area
		os.putenv('SDL_WINDOWID', str(self.window.xid))
		gtk.gdk.flush()
		pygame.init()
		pygame.display.set_mode((WINX,WINY),0,0)
		screen = pygame.display.get_surface()

		gobject.idle_add(pygame.display.update)
		self.show_all()

		# screen = pygame.display.get_surface()
		# self.joystick = pygame.joystick.Joystick(0)
		# self.joystick.init()

		# wheelClass = wheel.WheelClass(self.joystick)
		# carClass.keyboard()
		



# =====> Car Class
class Car:
	x = 1
	y = 1
	last = 0

	# screen = pygame.display.get_surface()
	pygame.joystick.init()
	joystick = pygame.joystick.Joystick(0)
	# self.joystick.init()

	wheelClass = wheel.WheelClass(joystick)
		

	#def __init__(self):


	def moveX(self, st): self.x = st
	def moveY(self, st): self.y = st
	def move(self, spd):
		arra = [[5,1,6], [3,0,4], [7,2,8]]
		ch = (16 * arra[self.y][self.x]) + spd
		if self.last != ch:
			self.sock.send(chr(ch))
			self.last = ch

	def keyboard(self):
		print "Keyboard"
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
			time.sleep(1)
			return True
		except:
			return False


	##### Accelerometer #####
	def axelmeter(self, speed):
		self.progbar.set_fraction(speed/11.0)


if __name__ == "__main__":

	# cli_menu()
	Base()
	gtk.main()
