#!/usr/bin/python

import subprocess, os
import re

def menu():
    print('welcome to our rasbpi car controller program, please select your option')
    print('1: Enter Mac address of car')
    print('2: keyboard control of car')
    print('3: GUI controller')
    print('4: gamepad controller')

def checkMac(mac):
    # HAving 99 problems? Let's add RegEx to them to round 'em up nicely
    print ("running checkMac function")
    isMac = re.match("[0-9a-f]{2}([-:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac.lower())
    print("Regular expressions running")
    if isMac != None:
        mac = mac.replace("-",":")
        # if it was a Windows user, replace all the - with : for usability
        print("All good")
        return True
    print("not a mac")
    return False


def macAddressChanging():
    try:
	isInFile = False
        mac = raw_input('Please enter new mac address\n XX:XX:XX:XX:XX:XX\n')
        if checkMac(mac): #if true
	    print("in if statement, MAC was okay")
            try:    #try to open a file, if not, quit
                with open("macFile.txt","w+") as macFile: # or w+? 
		    print("Mac file open")
                    for fileMac in macFile:
			print fileMac + "<>" + mac
                        if mac == fileMac.rstrip("\n"):
                            isInFile = True
                            break
                    if isInFile == False:
                        # Append to the beginning
                        content = macFile.read()
                        macFile.seek(0,0)
                        macFile.write(mac.rstrip("\n") + "\n" + content)
                        print('Sucess =]')
                    else: print("Mac is alredy in file, not gonna write it down")


            except IOError: #should be unecesary cause "r+" should create a file if it doesn't exist
                print "The MAC file does not seem to exist."
        else:
            print("MAC Address is wrong, mate")

    except Exception as detail:
        print('something went wrong', detail)

def macFileExists():
    if os.path.exists("macFile.txt"):return True
    return False

while True:
    menu()
    try:
	mode = int(raw_input('Enter Your Choice: '))
    except ValueError:
        print "not a number"

    if mode == 1:
        print('calling the mac address change function')
        macAddressChanging()
    elif mode == 2:
        if macFileExists():
            print('calling the keyboard control function')
            subprocess.call(["python", "start-up.py"])
        else:
            print("Please, enter a MAC address as there is none predefined")
            macAddressChanging()
    elif mode == 3:
        print('calling the gui control program')
        subprocess.call(["python", "guiPI.py"])
    elif mode == 4:
        print('calling the gamepad control function')
        #game pad stuff
