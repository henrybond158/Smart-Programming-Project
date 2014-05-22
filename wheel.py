#/usr/bin/python2

import pygame
import sys
import time


class WheelClass:
	def __init__(self):
<<<<<<< HEAD
		self.d = 0
		
		size = [600,400]
=======

		self.d = 0

		self.size = [300,200]
>>>>>>> ed222dd65f3997bd48bda748fa58f152ff07e080

		screen = pygame.display.set_mode(self.size)	

		pygame.joystick.init()

		self.joystick = pygame.joystick.Joystick(0)
		self.joystick.init()
	def getMov(self):
	
		pygame.event.pump()
	        #print self._joystick.get_axis(0) #WHEEL
		if (self.joystick.get_axis(0) > 0.075):
			turning=2 #right
		elif (self.joystick.get_axis(0) < -0.055):
			turning=0 #left
		else:
			turning=1 #straight

		#print self._joystick.get_axis(1) #THROTTLE/BRAKE
		speed = (self.joystick.get_axis(1) * -1) #THROTTLE is negative
		speed = int(speed * 15)
		print speed
		if (speed > 0):
			direction = 0
<<<<<<< HEAD
		else:
			direction = 2

		if (direction == 2):
			rSpeed = (self.joystick.get_axis(1)) #BRAKE is positive
			rSpeed = int(rSpeed * 15) #Otherwise it will not get up to 15
			if (rSpeed > 0):
				#if (speed > 255): speed = 255
				direction = 2
				speed =  rSpeed
				print ("this is your speed " + str(speed))

		return direction, turning, speed
=======
		#print self.joystick.get_axis(2) 
		#rSpeed = 0.0 #(self.joystick.get_axis(3) + 1) / 2
		#rSpeed = 1 - rSpeed
		#rSpeed = int(rSpeed * 15)
		if (direction == 0):
			speed = (self.joystick.get_axis(1))
			speed = int(speed * 15.1)
			if (speed > 0):
				direction = 1
		#print speed
		print direction
		#sys.stdout.write("BRAKE: ")
		#print self.joystick.get_axis(3) 
		#print self.joystick.get_axis(4) 
		#print self.joystick.get_axis(5) 
		return direction, turning, speed

	def launchGUI(self):
		screen = pygame.display.set_mode(self.size)		
		img = pygame.image.load("GUIPic.png").convert()
		screen.blit(img, (0, 0)) #Display image at 0, 0
		pygame.display.flip()   #Update screen
>>>>>>> ed222dd65f3997bd48bda748fa58f152ff07e080
