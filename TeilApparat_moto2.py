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
    # Pause = 0 ... 
    Pause = float (input ("Eingabe von -1 ist 'Handpause' (warten auf Taste 'Enter')\n"
                        "Bitte geben Sie die Pause (s) zwischen Teilschritten ein: "))

    liste = Teilungsliste (Teilungen)
    print (liste)
    # nur zu Testzwecken mehrfach aufrufbar (range (x))
    for i in range (1):
        # vorStepM2 (Teilungsliste, Pause, Zeitfaktor)
        # Pause = -1 ... Handpause (wartet auf "Enter")
        vorStepM2 (liste, Pause, 1)
        print ("Kreise vollendet", i + 1)

    # Ende Hauptprogramm

if __name__ == "__main__":
    try:
        init ()
        main ()
        GPIO.cleanup ()
    except KeyboardInterrupt:
        print ("Programm unterbrochen. GPIO wurde ausgeschalten")
        GPIO.cleanup ()
