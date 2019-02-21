#!/usr/bin/env python3
# -*- coding: utf-8 -*
from __future__ import print_function
# dummy module RPi.GPIO
# for use in Virtual Machine being able to test code
# which uses GPIO
from random import randint

"""
Programm / Python Modul
Autor: Ing. Josef Klotzner
20190111
"""

BCM = 0
BOARD = 1
IN = "input"
OUT = "output"

def setmode (dummy):
    if dummy == 0:
        print ("GPIO.setmode 'GPIO.BCM' emulated")
    if dummy == 1:
        print ("GPIO.setmode 'GPIO.BOARD' emulated")
def setup (dummy1, dummy2):
    print ("GPIO.setup emulated - set GPIO", dummy1, " to ", dummy2)
def output (dummy1, dummy2):
    pass
    #print (dummy1," ",dummy2,end = ',  ')
    #print ("GPIO.output emulated on output ", dummy1, "value: ", dummy2)
def input (dummy):
    rnd = randint (0, 1)
    print ("GPIO.input emulated - returning random ", rnd, " for input ", dummy)
    return (rnd)
def setwarnings(flag):
   print ("GPIO.setwarnings emulated with flag ", flag)
def cleanup():
   print ("GPIO.cleanup emulated")
