""" ultrasons réels
    encodeurs réels
    moteurs non alimentés / simulés

    Pour tester:
        1. Upload code arduinx
        2. fermer le moniteur série arduino
        3. lancer code python
        4. faire tourner les roues à la main
        5. python est censé afficher la distance parcourue
        6. quand 1000m environ sont atteints, python envoie STOP
"""

"""
    Arudino:
        lit ultrasons
        lit encodeurs
        envoie données à python

    Python:
        reçoit données
        si obstacle : STOP
        sinon : demander avance
        lire encodeurs réels
        calculer distance parcourue
        si distance >= 1 m : STOP
""" 





import serial
import time
import math

PORT = "..."
BAUDRATE = 9600

DISTANCE_OBJECTIF_MM = 1000

US_MIN_DIST = 20
US_MAX_DIST = 2000
SEUIL_SECURITE_LONGUEUR = 80

DIAMETRE_ROUE_MM = 100
TICKS_PAR_TOUR = 600

MM_PAR_TICK = (math.pi * DIAMETRE_ROUE_MM) / TICKS_PAR_TOUR

ticks_gauche_depart = None
ticks_droite_depart = None


def mesure_us_valide(distance: float) -> bool:
    return US_MIN_DIST <= distance <= US_MAX_DIST


def obstacle_detecte(distance_avant: float) -> bool:
    return distance_avant < SEUIL_SECURITE_LONGUEUR


def distance_parcourue(ticks_gauche: int, ticks_droite: int) -> float:
    global ticks_gauche_depart, ticks_droite_depart

    if ticks_gauche_depart is None or ticks_droite_depart is None:
        ticks_gauche_depart = ticks_gauche
        ticks_droite_depart = ticks_droite

    delta_gauche = ticks_gauche - ticks_gauche_depart
    delta_droite = ticks_droite - ticks_droite_depart

    distance_gauche = delta_gauche * MM_PAR_TICK
    distance_droite = delta_droite * MM_PAR_TICK

    return (distance_gauche + distance_droite) / 2


def envoyer_commande(ser, commande: str):
    ser.write((commande + "\n").encode("utf-8"))


ser = serial.Serial(PORT, BAUDRATE, timeout=1)
time.sleep(2)

print("Début test navigation 1 m")

while True:
    ligne = ser.readline().decode("utf-8").strip()

    if not ligne:
        continue

    try:
        distance_str, ticks_g_str, ticks_d_str = ligne.split(";")

        distance_avant = float(distance_str)
        ticks_gauche = int(ticks_g_str)
        ticks_droite = int(ticks_d_str)

    except ValueError:
        print("Ligne invalide :", ligne)
        continue

    if not mesure_us_valide(distance_avant):
        envoyer_commande(ser, "STOP")
        print("STOP : mesure ultrason invalide")
        continue

    distance = distance_parcourue(ticks_gauche, ticks_droite)

    # sécurité
    if obstacle_detecte(distance_avant):
        envoyer_commande(ser, "STOP")
        print(f"STOP : obstacle devant | distance ultrason={distance_avant:.1f} mm")
        continue

    if distance >= DISTANCE_OBJECTIF_MM:
        envoyer_commande(ser, "STOP")
        print(f"STOP : objectif atteint | distance={distance:.1f} mm")
        break

    envoyer_commande(ser, "AVANCE")

    print(
        f"AVANCE | ultrason={distance_avant:.1f} mm | "
        f"ticks G={ticks_gauche} | ticks D={ticks_droite} | "
        f"distance={distance:.1f} mm"
    )