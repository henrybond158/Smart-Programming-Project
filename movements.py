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



def threewayturn():
	startTime = time.time()
	while time.time() < startTime +3:
		move(5, 11)
	while time.time() < startTime + 6:
		move(7,11)

def spazzOut():
	"""
	Spazz out for 12 seconds, making random move every 3 seconds
	"""
	startTime = time.time()
	timeElapsed = startTime
	while time.time() < startTime +12:
		moveTime = time.time()
		direction = random.randint(1,8)
		while time.time() < moveTime + 3:
			move(direction,11)