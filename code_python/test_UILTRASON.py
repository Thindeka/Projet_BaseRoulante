import serial
import time

 
# TEST PIPELINE AVEC UN SEUL UTRASON : L'AVANT

# DISTANCES
US_MIN_DIST = 20
US_MAX_DIST = 2000

# FILTRAGE
US_ALPHA = 0.3

# SEUILS
SEUIL_SECURITE_LONGUEUR = 80   # avant / arrière
SEUIL_SECURITE_LARGEUR = 60    # gauche / droite

d_avant_filtre = 0.0
d_arriere_filtre = 0.0
d_gauche_filtre = 0.0
d_droite_filtre = 0.0
init_filtre_us = False


def mesure_valide(distance: float) -> bool:
    return US_MIN_DIST <= distance <= US_MAX_DIST


def filtrer(nouvelle_val: float, ancienne_val: float) -> float:
    return US_ALPHA * nouvelle_val + (1 - US_ALPHA) * ancienne_val


def obstacle_longueur(distance: float) -> bool:
    return distance < SEUIL_SECURITE_LONGUEUR


def obstacle_largeur(distance: float) -> bool:
    return distance < SEUIL_SECURITE_LARGEUR


def boucle_controle_ultrasons(
    d_avant_brut: float,
    d_arriere_brut: float,
    d_gauche_brut: float,
    d_droite_brut: float
) -> dict:
    global d_avant_filtre, d_arriere_filtre, d_gauche_filtre, d_droite_filtre
    global init_filtre_us

    if (
        not mesure_valide(d_avant_brut)
        or not mesure_valide(d_arriere_brut)
        or not mesure_valide(d_gauche_brut)
        or not mesure_valide(d_droite_brut)
    ):
        return {
            "stop": True,
            "raison": "Mesure invalide"
        }

    if not init_filtre_us:
        d_avant_filtre = d_avant_brut
        d_arriere_filtre = d_arriere_brut
        d_gauche_filtre = d_gauche_brut
        d_droite_filtre = d_droite_brut
        init_filtre_us = True
    else:
        d_avant_filtre = filtrer(d_avant_brut, d_avant_filtre)
        d_arriere_filtre = filtrer(d_arriere_brut, d_arriere_filtre)
        d_gauche_filtre = filtrer(d_gauche_brut, d_gauche_filtre)
        d_droite_filtre = filtrer(d_droite_brut, d_droite_filtre)

    if obstacle_longueur(d_avant_filtre):
        return {"stop": True, "raison": "Obstacle à l'avant"}

    if obstacle_longueur(d_arriere_filtre):
        return {"stop": True, "raison": "Obstacle à l'arriere"}

    if obstacle_largeur(d_gauche_filtre):
        return {"stop": True, "raison": "Obstacle à gauche"}

    if obstacle_largeur(d_droite_filtre):
        return {"stop": True, "raison": "Obstacle à droite"}

    return {"stop": False, "raison": "Aucun obstacle"}


PORT = "/dev/cu.usbmodem11401"   # à adapter
BAUDRATE = 9600

ser = serial.Serial(PORT, BAUDRATE, timeout=1)
time.sleep(2)

while True:
    ligne = ser.readline().decode("utf-8").strip()

    if not ligne:
        continue

    try:
        distance_avant = float(ligne)

        if distance_avant < 0:
            print("Mesure ultrason invalide")
            continue

        # pour le test, on met des valeurs fictives sûres pour les autres côtés
        resultat = boucle_controle_ultrasons(
            d_avant_brut=distance_avant,
            d_arriere_brut=1000.0,
            d_gauche_brut=1000.0,
            d_droite_brut=1000.0
        )

        print(f"Distance avant = {distance_avant:.1f} mm | {resultat}")

        if resultat["stop"]:
            print(">>> STOP ROBOT")
        else:
            print(">>> MOUVEMENT AUTORISÉ")

    except ValueError:
        print(f"Ligne invalide : {ligne}")