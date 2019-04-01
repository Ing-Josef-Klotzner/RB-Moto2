#!/usr/bin/env python3
# -*- coding: utf-8 -*

import RPi.GPIO as GPIO
from motors_2 import * #init, vorM1, retourM1, vorM2, retourM2

def main ():
    # schreibe hier Dein Hauptprogramm
    fak = 1
    x2 = False
    # Wegstrecke in mm
    teilungen = 4096
    weg = float (input ("Bitte die Wegstrecke (in mm) eingeben: "))
    # Abfrage für generische Lösung
    #motor = int (input ("Welcher Motor? (1 oder 2 und Enter eingeben"))
    #motor_f = motor - 1
    # Festlegung auf Motor1
    motor = 0
    steigung = 0.75
    steps = round (teilungen * weg / steigung)
    while True:
        print ("Motor", motor + 1, "bewegt sich", weg, "mm vor (das sind", steps, "Schritte)")
        goXS (steps, fak , motor, 0)

        print ("Motor", motor + 1, "bewegt sich", weg, "mm retour (das sind", steps, "Schritte)")
        goXS (steps, fak , motor, 1)

        in_ = input ("Wiederholen mit ENTER   Abbrechen mit a + Enter ")
        if in_ == "a" or in_ == "A":
            break
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
