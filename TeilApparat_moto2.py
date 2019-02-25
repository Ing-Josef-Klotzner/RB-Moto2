#!/usr/bin/env python3
# -*- coding: utf-8 -*

import RPi.GPIO as GPIO
from motors_2 import * #init, vorM1, retourM1, vorM2, retourM2
from time import sleep

def Teilungsliste (Teilungen, Kreisschritte = 4096):
    # Methode mit mathematischer Rundung
    liste = []    
    Fliesszahl = Kreisschritte / Teilungen
    Schritte_bisher = 0
    #print (Fliesszahl)
    for i in range (1, Teilungen + 1):
        Schritte = round (Fliesszahl * i) - Schritte_bisher
        liste.append (Schritte)
        Schritte_bisher += Schritte
    return (liste)
        
def main ():
    # schreibe hier Dein Hauptprogramm

    Teilungen = int (input ("Bitte geben Sie die Anzahl der gewünschten Teilungen ein: "))
    Pause = float(input ("Bitte geben Sie die Pause (s) zwischen Teilschritten ein: "))
    #Teilungen = 12
    #Pause = 1
#    for i in range (1, 21):
#        liste = Teilungsliste (i)
#        print ("Teilungsliste", liste, "Summe", sum (liste))
    liste = Teilungsliste (Teilungen)
    print (liste)
    for i in range (30):
        vorStepM2 (liste, Pause)

#    for i, steps in zip (range (1, Teilungen + 1), liste):
#        print ("Bewege Motor im Segment", i, "um", steps, "Schritte")
#        print ("Pause von", Pause, "Sekunden")
#        sleep (Pause)

#    fak = 1
#    x2 = False
#    umdr = 5
#    print ("Motor 1 macht", umdr, "Umdrehung(en) gegen Uhrzeigersinn, Zeitfaktor", fak, "x2", x2)
#    retourM1 (umdr * 512, fak, x2)

#    umdr = 5
#    print ("Motor 1 macht", umdr, "Umdrehung(en) im Uhrzeigersinn, Zeitfaktor", fak, "x2", x2)
#    vorM1 (umdr * 512, fak, x2)
    
    # Ende Hauptprogramm

if __name__ == "__main__":
    try:
        init ()
        main ()
        GPIO.cleanup ()
    except KeyboardInterrupt:
        print ("Programm unterbrochen. GPIO wurde ausgeschalten")
        GPIO.cleanup ()
