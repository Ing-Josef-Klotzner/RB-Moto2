#!/usr/bin/env python3
# -*- coding: utf-8 -*

import RPi.GPIO as GPIO
from motors_2 import * #init, vorM1, retourM1, vorM2, retourM2

def main ():
    # schreibe hier Dein Hauptprogramm
    fak = 1
    x2 = False
    # Wegstrecke in mm
    weg = float (input ("Bitte die Wegstrecke (in mm) eingeben: "))
    steigung = 0.75
    umdr = round (weg / steigung)

    while True:
        print ("Motor 1 macht", umdr, "Umdrehung(en) gegen Uhrzeigersinn, Zeitfaktor", fak, "x2", x2)
        retourM1 (umdr * 512, fak, x2)
        input ("Enter")
        
        print ("Motor 1 macht", umdr, "Umdrehung(en) im Uhrzeigersinn, Zeitfaktor", fak, "x2", x2)
        vorM1 (umdr * 512, fak, x2)
        input ("Enter")
    
    # Ende Hauptprogramm

if __name__ == "__main__":
    try:
        init ()
        main ()
        # sleep nur für test
        sleep (0)
        GPIO.cleanup ()
    except KeyboardInterrupt:
        print ("Programm unterbrochen. GPIO wurde ausgeschalten")
        GPIO.cleanup ()
