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
    dir_ = 0
    decsn = dir_ == 1 or dir_ == 2
    while not decsn:
        dir_ = int (input ("Richtung angeben (RETOUR - 1 und Enter) (VOR - 2 und Enter)"))
        decsn = dir_ == 1 or dir_ == 2
        if not decsn:
            print ("Bitte nochmal eingeben; Richtung muss 1 oder 2 sein")
    # Abfrage für generische Lösung
    #motor = int (input ("Welcher Motor? (1 oder 2 und Enter eingeben"))
    #motor_f = motor - 1
    if dir_ == 1:
        dir_txt = "retour"
    else:
        dir_txt = "vor"
    # Festlegung auf Motor1
    motor = 0
    steigung = 0.75
    steps = round (teilungen * weg / steigung)

    print ("Motor", motor + 1, "bewegt sich", weg, "mm", dir_txt, "(das sind", steps, "Schritte)")
    goXS (steps, fak , motor, dir_)

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
