#!/usr/bin/python


print('welcome to our rasbpi car controller program, please select your option')
print('1: Enter Mac address of car')
print('2: keyboard control of car')
print('3: GUI controller')
print('4: gamepad controller')
raw_input('Enter Your Choice')
try:
	mode = int(raw_input('enter your choice:'))
except ValueError:
	print "not a number"

if mode == 1:
	print('calling the mac address change function')
	macAddressChanging()
elif mode == 2:
	print('calling the keyboard control function')
	#keyboard call
elif mode == 3:
	print('calling the gui control program')
	#gui stuff here
elif mode == 4:
	print('calling the gamepad control function')
	#game pad stuff



def macAddressChanging():
	try:
		mac = raw_input('Please enter new mac address')
		f = open('macFile','w')
		f.write(mac)
		f.close
	except:
		print('something went wrong')
