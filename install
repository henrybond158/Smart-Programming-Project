#!/bin/bash

echo "[...] Bluetooth [...]"

sudo apt-get -qq install python-pip python-dev build-essential
sudo apt-get -qq install --no-install-recommends bluetooth
sudo apt-get -qq install bluez python-bluez bluez-hcidump
sudo pip install evdev

echo "[...] Connectioning to: $1 [...]"

/etc/init.d/bluetooth restart
bluez-simple-agent hci0 $1

echo "Controllers..."

# Link: mattdyson.org/blog/2013/01/using-an-xbox-360-wireless-controller-with-raspberry-pi/

sudo apt-get -qq install xboxdrv
#git clone https://github.com/zephod/lego-pi.git legopi
