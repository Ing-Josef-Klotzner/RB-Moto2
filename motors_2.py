#!/usr/bin/env python3
# -*- coding: utf-8 -*
from __future__ import print_function
# modul motors_2

from time import sleep
import RPi.GPIO as GPIO

from sys import version_info
if version_info.major == 3:
    pass
elif version_info.major == 2:
    input = raw_input
else:
    print ("Unknown python version - input function not safe")

"""
Programm / Python Modul für 2 Schrittmotore - Modul "RB-Moto2" (Conrad Elektronik)
Autor: Ing. Josef Klotzner
20190111 - 20190225

Beschreibung:
Das Getriebe hat 1/512
Zusammen mit 8 Motorsteps macht das 512 x 8 = 4096 Schritte für eine Umdrehung

das Programm hier kann auch als Python Modul "motors_2" geladen werden um die darin definierten Funktionen zu nutzen wie

motor.vorM1 (512 [, 2[, False]])
... macht eine Drehung des Motors 1 (512 Schritte) im Uhrzeigersinn (auf Motorachse gesehen mit Zeitfaktor 2 (= halbe Geschwindigkeit)) mit 8 Halbschritten für eine Motorumdrehung (False Parameter; True wären nur 4 Vollschritte - 40% höhere Geschwindigkeit)

Mit Strg-C läßt sich Programm unterbrechen ... mit beliebiger Taste wieder fortsetzen.
Bei Unterbrechung wird sicher gestellt, dass Motor letzte Bewegung vollendet und sich kein Stromfluß durch Spulen ergibt (stromlos sicher gestellt)
Es ist sicher gestellt, dass bei völliger Programmunterbrechung und bei Beenden des Programms GPIO sauber ausgeschalten wird.

Beim Zeitfaktor über 10 wurde durch Tests ermittelt, dass 0,01 s Strom zum Anfahren für Einzelschritte ein dennoch hohes Drehmoment sicher stellt. Der Rest des geforderten Zeitfaktors wird stromlos abgewartet (geringer Stromverbrauch und sicher stellen, dass Motor kalt bleibt). Es sind dadurch beliebig lange Zeitfaktoren möglich. Für Uhren oder ähnliches mit geringem Drehmomentbedarf kann MaximumPulseWidth von 10 auf 6 oder 4 reduziert werden (weniger nicht empfehlenswert, weil sonst Anfahren im Motor nicht mehr gewährleistet ist)

"""

# PIN - Zuweisung am Raspberry
# Motor 1:
# A [0] ... A von Motor 1 (ist 22); A [1] ... A von Motor 2 (ist 4)
A = [22, 4]; B = [27, 25]; C = [18, 24]; D = [17, 23]

TIME = 0.001

# Pins definieren
# für Motoren 1 und 2:
# Definition in Schleife besser - Vorteil: je nur eine Zeile Eingabe
def init ():
    # Motoren definiert auf Position des Step1 setzen
    GPIO.setmode (GPIO.BCM)
    for m in [0, 1]:
        for x in [A [m], B [m], C [m], D [m]]:
            GPIO.setup (x, GPIO.OUT)
            GPIO.output (x, False)
    initToStep1_M1 ()
    initToStep1_M2 ()

# Ansteuerung der Spulen der Motoren 1 und 2:
# Definition in Schleife besser - Vorteil: je nur eine Zeile Eingabe

# folgende 2 Funktionen nicht direkt verwenden!
# (außer Sie wissen was sie tun)
# sonst werden eventuell Schritte am Motor1 übersprungen
# es könnte sein, dass Motor nicht anläuft!
# Schritt mit halbem Drehmoment
def StepH (s, Puls, Wait):
    GPIO.output (s, True)
    sleep (TIME * Puls)
    GPIO.output (s, False)
    sleep (TIME * Wait)
# Schritt mit vollem Drehmoment
def StepV (s1, s2, Puls, Wait):
    GPIO.output (s1, True)
    GPIO.output (s2, True)
    sleep (TIME * Puls)
    GPIO.output (s1, False)
    GPIO.output (s2, False)
    sleep (TIME * Wait)

def PulseWait (Faktor):
    MaximumPulseWidth = 10
    if Faktor <= MaximumPulseWidth:
        return (Faktor, 0)
    else:
        return (MaximumPulseWidth, Faktor - MaximumPulseWidth)

def Step1 (Puls, Wait, Motor): StepH (A [Motor], Puls, Wait)
def Step2 (Puls, Wait, Motor): StepV (A [Motor], B [Motor], Puls, Wait)
def Step3 (Puls, Wait, Motor): StepH (B [Motor], Puls, Wait)
def Step4 (Puls, Wait, Motor): StepV (B [Motor], C [Motor], Puls, Wait)
def Step5 (Puls, Wait, Motor): StepH (C [Motor], Puls, Wait)
def Step6 (Puls, Wait, Motor): StepV (C [Motor], D [Motor], Puls, Wait)
def Step7 (Puls, Wait, Motor): StepH (D [Motor], Puls, Wait)
def Step8 (Puls, Wait, Motor): StepV (D [Motor], A [Motor], Puls, Wait)

#  - Motor 1
# eine ganze Umdrehung der Achse = 512 Teilungen
# im Uhrzeigersinn
#                 Zeitfaktor 1 ist Maximalgeschwindigkeit
def vorM1 (Teilungen, Faktor = 1, x2 = False): go (Teilungen, Faktor, 0, 0, x2)
# gegen Uhrzeigersinn
def retourM1 (Teilungen, Faktor = 1, x2 = False): go (Teilungen, Faktor, 0, 1, x2)
#  - Motor 2
# eine ganze Umdrehung (= 512 Teilungen)
# im Uhrzeigersinn
def vorM2 (Teilungen, Faktor = 1, x2 = False): go (Teilungen, Faktor, 1, 0, x2)
# gegen Uhrzeigersinn
def retourM2 (Teilungen, Faktor = 1, x2 = False): go (Teilungen, Faktor, 1, 1, x2)
def go (Teilungen, Faktor, m, d, x2):
    f = abs (Faktor)
    if f < 1: f = 1
    if x2: funcs = [Step2, Step4, Step6, Step8]; f *= 1.6
    else: funcs = [Step1, Step2, Step3, Step4, Step5, Step6, Step7, Step8]
    (p, w) = PulseWait (f)
    if m == 0: Mtxt = "M1"
    else: Mtxt = "M2"
    if d == 1:
        text = "retour" + Mtxt
        funcs = funcs [::-1]
    else:
        text = "vor" + Mtxt
    for i in range (Teilungen):
        for func in funcs:
            try:
                func (p, w, m)
            except KeyboardInterrupt:
                func (p, w, m)
                print ("Unterbrechung in Funktion", text," in", func, "in Teilung", i)
                input ("Fortsetzen mit ENTER")
                print ("Es wird fortgesetzt ...")

#  - Motor 1
# Einzelschritte (4096 Schritte für eine Achsendrehung)
# im Uhrzeigersinn  ...  TP ... Tastaturpause von Hand, wenn Pause = -1
def vorStepM1 (Teilungsliste, Pause = 1, Faktor = 1):
    goS (Teilungsliste, Pause, Faktor, 0, 0)
# gegen Uhrzeigersinn
def retourStepM1 (Teilungsliste, Pause = 1, Faktor = 1):
    goS (Teilungsliste, Pause, Faktor, 0, 1)
#  - Motor 2
# eine ganze Umdrehung (= 512 Teilungen)
# im Uhrzeigersinn
def vorStepM2 (Teilungsliste, Pause = 1, Faktor = 1):
    goS (Teilungsliste, Pause, Faktor, 1, 0)
# gegen Uhrzeigersinn
def retourStepM2 (Teilungsliste, Pause = 1, Faktor = 1):
    goS (Teilungsliste, Pause, Faktor, 1, 1)
def goS (Teilungsliste, Pause, Faktor, m, d):
    TEILUNGEN = 4096
    ListCnt = 0
    TP = False
    if Pause == -1: TP = True; Pause = 0
    elif Pause < 0: Pause = 0
    f = abs (Faktor)
    if f < 1: f = 1
    funcs = [Step1, Step2, Step3, Step4, Step5, Step6, Step7, Step8]
    (p, w) = PulseWait (f)
    if m == 0: Mtxt = "M1"
    else: Mtxt = "M2"
    if d == 1:
        text = "retour" + Mtxt
        funcs = funcs [::-1]
    else:
        text = "vor" + Mtxt
    Schritte_gesamt = 0
    for i in range (1, TEILUNGEN + 1, 8):
        for step8, func in zip (range (8), funcs):
            try:
                func (p, w, m)
                if i + step8 == Schritte_gesamt + Teilungsliste [ListCnt] and i + step8 != TEILUNGEN:
                    print ("Pause zwischen Teilungsschritten von", Pause, "Sekunden", end = ", ")
                    print ("bei step", i + step8)
                    if TP:
                        input ("Fortsetzen mit ENTER")
                        print ("Es wird fortgesetzt ...")
                    else: sleep (Pause)
                    Schritte_gesamt += Teilungsliste [ListCnt]
                    ListCnt += 1
            except KeyboardInterrupt:
                func (p, w, m)
                print ("Unterbrechung in Funktion", text,\
                    "in", func, "in Teilschritt", i + step8)
                if i + step8 == Schritte_gesamt + Teilungsliste [ListCnt]:
                    Schritte_gesamt += Teilungsliste [ListCnt]
                    ListCnt += 1
                input ("Fortsetzen mit ENTER")
                print ("Es wird fortgesetzt ...")

        #p = p - 0.5 / 50
        #if p < 1.4: p = 1.4
        #print (p, end =",")
# wird erstmalig benötigt für Feinpositionierung
# (stop zwischen Step1 und Step8), um Motor1 anfangs
# definiert auf Position des Step1_1 zu bringen
def initToStep1_M1 ():
    vorM1 (1)
    retourM1 (1)

# wird erstmalig benötigt für Feinpositionierung
# (stop zwischen Step1 und Step8), um Motor2 anfangs
# definiert auf Position des Step1_2 zu bringen
def initToStep1_M2 ():
    vorM2 (1)
    retourM2 (1)

def main ():
    # Hauptprogramm

    # x2 Geschwindigkeit durch überspringen der Halbschritte
    x2 = True
    # Geschwindigkeitsfaktor kann Fließkommazahl sein größer oder gleich 1
    fak = 1
    # Umdrehungen muss ganze Zahl sein
    umdr = 1
    print ("Motor 1 macht", umdr, "Umdrehung(en) im Uhrzeigersinn, Zeitfaktor", fak, "x2", x2)
    vorM1 (umdr * 512, fak, x2)
    x2 = False
    fak = 2
    umdr = 1
    print ("Motor 1 macht", umdr, "Umdrehung(en) gegen Uhrzeigersinn, Zeitfaktor", fak, "x2", x2)
    retourM1 (umdr * 512, fak)
    umdr = 1
    fak = 3
    print ("Motor 2 macht", umdr, "Umdrehung(en) im Uhrzeigersinn, Zeitfaktor", fak, "x2", x2)
    vorM2 (umdr * 512, fak)
    umdr = 1
    fak = 4
    print ("Motor 2 macht", umdr, "Umdrehung(en) gegen Uhrzeigersinn, Zeitfaktor", fak, "x2", x2)
    retourM2 (umdr * 512, fak)

    # Ende Hauptprogramm

if __name__ == "__main__":
    try:
        init ()
        main ()
        GPIO.cleanup ()
    except KeyboardInterrupt:
        print ("Programm unterbrochen. GPIO wurde ausgeschalten")
        GPIO.cleanup ()
