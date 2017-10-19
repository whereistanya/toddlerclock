## toddlerclock.py
toddlerclock.is a small extremely stupid clock built using pygame. Its goal is to tell my four year old when she can come wake me up. It... was not that successful? Oh well.

## Installing pygame for python3

There are a bunch of libraries pygame needs. Here's what I installed:

sudo apt-get install python-dev
sudo apt-get install libsdl-dev libportmidi-dev libsdl-ttf2.0-dev libsdl-image1.2-dev libsdl-mixer1.2-dev
sudo apt-get install python-pip3
sudo pip3 install pygame

## Using a raspberry pi display for toddlerclock

This is intended to run on a raspberry pi with a display. If run on a workstation, it will create a small window, so it's possible to test it locally without a raspberry pi. 

The code as-is works with the [PiTFT capacitive display](https://www.adafruit.com/product/1983). For the [7" touchscreen display](https://www.adafruit.com/product/2718), comment out ```os.putenv('SDL_FBDEV', '/dev/fb1')```, and it should use the right display by default. I haven't tested it with anything else.

You can modify the brightness (at least for the 7" display; I haven't tested the PiTFT) by editing ```/sys/devices/platform/rpi_backlight/backlight/rpi_backlight/brightness```

```
$ echo 255 > brightness   # completely on  
$ echo 0 > brightness     # completely off  
$ echo 120 > brightness   # somewhere in between  


