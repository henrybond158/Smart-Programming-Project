#/usr/bin/python
import os
import pygame
import sys
import time


class WheelClass:
	def __init__(self):
		self.d = 0

		self.size = [300,200]
		# I made changes, notice

		screen = pygame.display.set_mode(self.size)		
		# img = pygame.image.load("GUIPic.png").convert()
		# pygame.display.set_mode((1,1))
		# screen.blit(img, (0, 0)) #Display image at 0, 0
		# pygame.display.flip()   #Update screen

		pygame.joystick.init()

		self.joystick = pygame.joystick.Joystick(0)
		self.joystick.init()
		

	def getMov(self):
		pygame.event.pump()
		#sys.stdout.write("WHEEL: ")

                #print self.joystick.get_axis(0)
		if (self.joystick.get_axis(0) > 0.075):
			turning = 2
			#print "turning right"
		elif (self.joystick.get_axis(0) < -0.055):
			turning = 0
			#print "turning left"
		else:
			turning = 1
			#print "straight line"
		#sys.stdout.write("CLUTCH: ")
		#print self.joystick.get_axis(1) 	
		#sys.stdout.write("THROTTLE: ")
		speed = (self.joystick.get_axis(2) + 1) / 2
		speed = 1 - speed
		speed = int(speed * 15)
		if (speed > 0):
			direction = 0
		else:
			direction = 1
		#print self.joystick.get_axis(2) 
		rSpeed = (self.joystick.get_axis(3) + 1) / 2
		rSpeed = 1 - rSpeed
		rSpeed = int(rSpeed * 15)
		if (rSpeed > 0):
			direction = 2
			speed = rSpeed
		#print speed
		#print direction
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