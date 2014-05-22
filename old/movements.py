# speed 1-15

#3 way turn 

import time
import random

def timeFunction(t):
	"""
	Times the execution of the Function by making it sleep
	Making it sleep might be easier for executuion
	Needs to be tested
	"""


def oldmove(dir, spd):
	if (dir < 15) or (spd < 15):
		sock.send(chr((dir*16) + spd))

def threewayturn():
	startTime = time.time()
	while time.time() < startTime +3
		oldmove(5, 11)
	while time.time() < startTime + 6:
		oldmove(7,11)

def spazzOut():
	"""
	Spazz out for 12 seconds, making random move every 3 seconds
	"""
	startTime = time.time()
	timeElapsed = startTime
	while time.time() < startTime +12:
		moveTime = time.time()
		# direction = random.randint(1,8) # Not using this as just turning weels is useless
		direction = random.choice([1,2,5,6,7,8])
		while time.time() < moveTime + 3:
			oldmove(direction,11)