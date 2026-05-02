"""
    Arduino:
        lit les 2 ToF gauche avant / gauche arrière
        envoie les distances à Python

    Python :
        calcule l'erreur d'orientation
        décide ROTATION / STOP ORIENTATION

    
"""



import serial
import time

PORT = "..."       
BAUDRATE = 9600

ser = serial.Serial(PORT, BAUDRATE, timeout=1)


# distances en mm

# DISTANCES 
ToF_MIN_DIST = 50  
ToF_MAX_DIST = 800

# FILTARGE
ToF_ALPHA = 0.3 

# ALIGNEMENT
SEUIL_PARALLELISME = 10

# CONTROLE 
KP_ROT = 0.02   # gain proportionnel de rotation = de combien on tourne pour une erreur donnée
ROT_MAX = 0.3   # permet de borner la vitesse de rotation du moteur

# VALIDATION TEMPORELLE
TEMPS_STABLE_MS = 0


d_avant_filtre = 0
d_arriere_filtre = 0
init_filtre = False



def mesure_valide (distance : float) -> bool :
    """ Retourne vrai si la distance est valide

    Args:
        disatnce (float): distance en mm

    Returns:
        bool 
    """
    return ToF_MIN_DIST <= distance <= ToF_MAX_DIST 




def filtrer (nouvelle_val : float, ancienne_val : float) -> float :
    """ filtre la valeur

    Args:
        nouvelle_val (float): en mm
        ancienne_val (float): en mm

    Returns:
        float: valeur filtrée
    """
    return ToF_ALPHA * nouvelle_val + (1 - ToF_ALPHA) * ancienne_val




def calcul_erreur (d_avant_filtre : float, d_arriere_filtre : float) -> float :
    """ Calcule l'erreur en mm

    Args:
        d_avant_filtre (float) : mm
        d_arrire_filtre (float) : mm

    Returns:
        float: l'erreur
    """
    return d_avant_filtre - d_arriere_filtre 



def saturer (val : float, min_val : float, max_val : float) -> float :
    """ Bloque une valeur entre le min et le max en mm

    Args:
        val (float)
        min (float)
        max (float)
    Returns:
        float: la valeur bloquée
    """

    if val < min_val :
        return min_val
    if val > max_val :
        return max_val
    return val




def calcul_commande_rotation (erreur : float) -> float :
    """ Calcule la commande de rotation en fonction de l'erreur (de combien doit tourner le robot)
        commande ∈ [-ROT_MAX ; +ROT_MAX] car on tourne dans les 2 sens

    Args:
        erreur (float) : difference entre la distance des deux capteurs ToF en mm

    Returns:
        float : commande de rotation
    """

    if abs(erreur) < SEUIL_PARALLELISME :
        return 0.0
    
    # commande est une vitesse moteur
    commande = KP_ROT * erreur  # il y a peut être un signe -, jsp trop, faut tester
    commande = saturer(commande, -ROT_MAX, ROT_MAX)   
    
    return commande




def boucle_controle (d_avant_brut : float, d_arriere_brut : float) -> float :
    """ Traîte les mesures ToF et retourne une commande de rotation

    Args:
        d_avant_brut (float) : en mm
        d_arriere_brut (float) : en mm

    Returns:
        float: commande de rotation 
    """

    global d_avant_filtre, d_arriere_filtre, init_filtre


    # 1. Verification des mesures 
    if not mesure_valide(d_avant_brut) or not mesure_valide(d_arriere_brut) :
        print("Mesure ToF invalide")
        return 0.0
    

    # 2. Initialisation du filtre
    if not init_filtre :
        d_avant_filtre = d_avant_brut
        d_arriere_filtre = d_arriere_brut
        init_filtre = True 
    else :
        d_avant_filtre = filtrer(d_avant_brut, d_avant_filtre)
        d_arriere_filtre = filtrer(d_arriere_brut, d_arriere_filtre)


    # 3. Calcul de l'erreur
    erreur = calcul_erreur(d_avant_filtre, d_arriere_filtre) 

    # 4. Calcul commande
    commande_rotation = calcul_commande_rotation(erreur)

    return commande_rotation


    

def reset_filtre():
    global d_avant_filtre, d_arriere_filtre, init_filtre
    d_avant_filtre = 0.0
    d_arriere_filtre = 0.0
    init_filtre = False



def test_scenario(nom: str, mesures: list[tuple[float, float]]):
    print(f"\n--- {nom} ---")
    reset_filtre()

    for i, (avant, arriere) in enumerate(mesures):
        cmd = boucle_controle(avant, arriere)
        err = calcul_erreur(d_avant_filtre, d_arriere_filtre) if init_filtre else 0.0
        print(
            f"tour={i:02d} | "
            f"avant={avant:.1f} | arriere={arriere:.1f} | "
            f"avant_f={d_avant_filtre:.1f} | arriere_f={d_arriere_filtre:.1f} | "
            f"err={err:.1f} | cmd={cmd:.3f}"
        )






# laisse le temps à l'Arduino de redémarrer
time.sleep(2)

print("Début communication ToF Arduino <-> Python")

while True:

    # lecture ligne série
    ligne = ser.readline().decode("utf-8").strip()

    if not ligne:
        continue

    try:
        # exemple reçu : "320;300"
        d_avant_str, d_arriere_str = ligne.split(";")

        d_avant = float(d_avant_str)
        d_arriere = float(d_arriere_str)

    except ValueError:
        print(f"Ligne invalide : {ligne}")
        continue

    # appel de ton pipeline ToF
    commande_rotation = boucle_controle(
        d_avant_brut=d_avant,
        d_arriere_brut=d_arriere
    )

    # affichage debug
    erreur = calcul_erreur(d_avant_filtre, d_arriere_filtre)

    print(
        f"avant={d_avant:.1f} mm | "
        f"arriere={d_arriere:.1f} mm | "
        f"err={erreur:.1f} | "
        f"cmd_rot={commande_rotation:.3f}"
    )

    # envoi commande vers Arduino
    ser.write(f"{commande_rotation}\n".encode("utf-8"))
    print(f"commande envoyee Arduino = {commande_rotation:.3f}")



