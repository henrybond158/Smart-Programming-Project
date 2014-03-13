#!/usr/bin/python


print('welcome to our rasbpi car controller program, please select your option')
print('1: Enter Mac address of car')
print('2: keyboard control of car')
print('3: GUI controller')
print('4: gamepad controller')
raw_input('Enter Your Choice')
try:
	mode = int(raw_input('enter your choice:'))
except: ValueError:
	print "not a number"