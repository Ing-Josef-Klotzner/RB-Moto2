#!/usr/bin/python
# -*- coding: utf-8 -*

import RPi.GPIO as GPIO
from motors_2 import * #init, vorM1, retourM1, vorM2, retourM2

def main ():
    # schreibe hier Dein Hauptprogramm
    fak = 1
    x2 = False
    umdr = 5
    print ("Motor 1 macht", umdr, "Umdrehung(en) gegen Uhrzeigersinn, Zeitfaktor", fak, "x2", x2)
    retourM1 (umdr * 512, fak, x2)

    umdr = 5
    print ("Motor 1 macht", umdr, "Umdrehung(en) im Uhrzeigersinn, Zeitfaktor", fak, "x2", x2)
    vorM1 (umdr * 512, fak, x2)
    
    # Ende Hauptprogramm

if __name__ == "__main__":
    try:
        init ()
        main ()
        GPIO.cleanup ()
    except KeyboardInterrupt:
        print ("Programm unterbrochen. GPIO wurde ausgeschalten")
        GPIO.cleanup ()
