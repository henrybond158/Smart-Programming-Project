#!/usr/bin/python
import pygame
from pygame.locals import *
import os
import wheel
import sys, select, tty, termios, bluetooth, time, re
from evdev import InputDevice, categorize, ecodes # Device Input
from lib import xbox_read # Controller Lib
import random

# =====> Main Class

class Base():
	def getMacAddress(self):
		try:
			with open("macFile","r+") as macFile:
				mc = macFile.readline().rstrip("\n")
				if re.match("[0-9a-f]{2}([-:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mc.lower()):
					return mc
				else: return ''
		except IOError:
			print "[...] MAC address File doesn't seem to Exist [...]"
			return ''

	def mainMenu(self):
		menu = {}
		menu['1']=": Keyboard with GUI"
		menu['2']=": Wheel"
		menu['3']=": Xbox Controller"
		menu['4']=": Playstation3 Controller"
		menu['p']=": Pre-set Figures"
		menu['r']=": Reconnected"
		menu['q']=": Quit"

		print "[...] Menu [...]\n"
		options=menu.keys()
		options.sort()

		for entry in options: 
			print "\t" + entry, menu[entry]

	def __init__(self):
		os.system(['clear','cls'][os.name == 'nt'])
		carClass = Car()

		print "[...] Connecting to the Car : " + self.getMacAddress() + " [...]"

		if Car().test(self.getMacAddress()):
			print "[...]\033[92m Connection Successful \033[0m[...]"
			carClass.connecting(self.getMacAddress())
		else:
			print "[...]\033[91m Connection Failed \033[0m [...]"

		

		while True: 
			mainMenu()
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
			elif selection == 'p':
				carClass.subPreMenu()
			elif selection == 'r':
				if Car().test(self.getMacAddress()):
					print "[...]\033[92m Connection Successful \033[0m[...]"
					carClass.connecting(self.getMacAddress())
				else:
					print "[...]\033[91m Connection Failed or Already Connected \033[0m [...]"
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
	speed = 8
	maxSpeed = 15
	minSpeed = 0
	wheelClass = wheel.WheelClass()

	#def __init__(self):


	def moveX(self, st): 
		if(st > -1 or st < 3):
			self.x = st
	def moveY(self, st): 
		if(st > -1 or st < 3):
			self.y = st
	def moveXY(self, xBit, yBit, spd, tim):
		self.x = xBit
		self.y = yBit
		self.move(spd)
		time.sleep(tim)
	def move(self, spd):
		arra = [[5,1,6], [3,0,4], [7,2,8]]
		ch = (16 * arra[self.y][self.x]) + spd
		if self.last != ch and (ch >= 0 or ch <= 255) :
			self.sock.send(chr(ch))
			self.last = ch
	def setSpeed(self, spd):
		if(spd >= self.maxSpeed or spd <= self.minSpeed):
			self.speed += spd


	def keyboard(self):
		# loop around each key press
		self.wheelClass.launchGUI()
		while True:
		# Starts pulling keyboard inputs from pygame
			pygame.event.pump()
		# Sets keyboard inputs to a variable
			self.pressed = pygame.key.get_pressed()

			# Get events
			event = pygame.event.poll()

		# if either the up/down button is pressed, set the Y axes to
			if self.pressed[K_UP]: self.moveY(0)
			elif self.pressed[K_DOWN]: self.moveY(2)
			else: self.moveY(1)

		# if either the left/right button is pressed, set the X axes to
			if self.pressed[K_LEFT]: self.moveX(0)
			elif self.pressed[K_RIGHT]: self.moveX(2)
			else: self.moveX(1)

		# if either the plus/minus buttons are pressed, increment/decrement the speed
			if self.pressed[K_PLUS]: self.setSpeed(1)
			elif self.pressed[K_MINUS]: self.setSpeed(-1)

		# Will run the move function, move with set the X/Y vars and move the car accordingly
			self.move(self.speed)
		# If the escape key is pressed, exit
			if self.pressed[K_ESCAPE]: break

			if event.type == pygame.MOUSEBUTTONDOWN: #and event.button == LEFT:
				self.mouse_click_handler(event.pos)

	def controllerXbox(self):
		# loop around xbox events
		while True:
			self.speed = 0
			for event in xbox_read.event_stream(deadzone=12000):

			# if either the up/down button is pressed, set the Y axes to
				if (event.key == 'RT' or event.key == 'LT'):
					if event.key == 'RT' and event.value > 1:
						self.speed = int(event.value)/17
						self.moveY(0)
					elif event.key == 'LT' and event.value > 1:
						self.speed = int(event.value)/17
						self.moveY(2)
					else: self.moveY(1)

			# if either the left/right button is pressed, set the X axes to
				if(event.key == 'dl' or event.key == 'dr'):
					if event.key == 'dl' and event.value == 1: self.moveX(0)
					elif event.key == 'dr' and event.value == 1: self.moveX(2)
					else: self.moveX(1)



				#if(event.key == 'RT' or event.key == 'LT') and self.speed != int(event.value)/17:
				#	self.speed = int(event.value)/17
				
				self.move(self.speed)

				if(event.key == 'guide'): break


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

	def subPreMenu(self):
		os.system(['clear','cls'][os.name == 'nt'])
		menu = {}

		menu['1']=": Circle"
		menu['2']=": Random*"
		menu['3']=": Three Point Turn"
		menu['4']=": Figure of Eight"
		menu['q']=": Quit"

		while True: 
			print "[...] Pre-defined Figures [...]\n"
			options=menu.keys()
			options.sort()

			for entry in options: 
				print "\t" + entry, menu[entry]

			selection=raw_input("\nPlease Select: ") 
			os.system(['clear','cls'][os.name == 'nt'])

			if selection == '1': 
				print '[...] Circle [...]'
				self.circle()
			elif selection == '2': 
				print '[...] Random* [...]'
				#self.leftCircle()
			elif selection == '3': 
				print '[...] Three Point Turn [...]'
				self.threePointTurn()
			elif selection == '4': 
				print '[...] Figure of Eigth [...]'
				self.eigth()
			elif selection == 'q':
				break
			else: 
				print "Unknown Option Selected!"
				time.sleep(1)


	def threePointTurn(self):
		self.moveXY(1, 2, 8, .4)		# backwards
		self.moveXY(2, 2, 8, 1.6)		# backwards, right
		self.moveXY(0, 0, 8, 1.8)		# forward, left
		self.moveXY(1, 0, 8, .5)		# forward
		self.moveXY(1,1,0,0)

	def circle(self):
		self.moveXY(2, 0, 6, 16)	# forward right
		self.moveXY(1,1,0,0)		# stop

	def eigth(self):
		self.moveXY(2, 0, 8, 7.2)	# forward right
		self.moveXY(1, 0, 8, .1)	# forward
		self.moveXY(0, 0, 8, 7.2)	# forward left
		self.moveXY(1, 0, 8, .1)	# forward
		self.moveXY(1,1,0,0)		# stop

	def randomMoves(self):
		"""
		Spazz out for 12 seconds, making random move every 3 seconds
		"""
		for x in range(1,5): #running 4 times
			dirX = random.choice([0,1,2])
			dirY = random.choice([0,2]) #not using 1 as it would just turn wheels
			speed = random.randint(5,10)
			self.moveXY(dirX,dirY,speed,3)
		
	def cruise(self):
		"""
		Cruising for 10 seconds
		"""
		self.moveXY(1,0,9,10)


	##### Accelerometer #####
	def axelmeter(self, speed):
		self.progbar.set_fraction(speed/11.0)

	def mouse_click_handler(self, pos):
		if pos[0] > 110 and pos[0] < 190:
			if pos[1] >110 and pos[1] < 140:
				print "Do 8 function"
				self.eigth()

			if pos[1] >160 and pos[1] < 190:	
				self.randomMoves()
		if pos[0] > 210 and pos[0] < 290:
			if pos[1] >110 and pos[1] < 140:
				print "Circle"
				self.circle()
			if pos[1] >160 and pos[1] < 190:
				self.threePointTurn()
		if pos[0] >10 and pos[0] <90:
			if pos[1] >110 and pos[1] < 140:
				self.cruise()
			if pos[1] >160 and pos[1] < 190:
				sys.exit(0)

if __name__ == "__main__":
	Base()
