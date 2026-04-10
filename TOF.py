# VARIABLES GLOBALES

# distances en mm

# CAPTEURS 
MIN_DIST = 50  
MAX_DIST = 800

# FILTARGE
ALPHA = 0.3 

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



def mesure_valide (d : float) -> bool :
    """ Retourne vrai si la distance d est valide

    Args:
        d (float): distance en mm

    Returns:
        bool 
    """
    return MIN_DIST <= d <= MAX_DIST 




def filtrer (nouvelle_val : float, ancienne_val : float) -> float :
    """ filtre la valeur

    Args:
        nouvelle_val (float): en mm
        ancienne_val (float): en mm

    Returns:
        float: valeur filtrée
    """
    return ALPHA * nouvelle_val + (1 - ALPHA) * ancienne_val




def calcul_erreur (d_avant_filtre : float, d_arriere_filtre : float) -> float :
    """ Calcule l'erreur en mm

    Args:
        d_avant_filtre (float) : mm
        d_arrire_filtre (float) : mm

    Returns:
        float: l'erreur
    """
    return d_avant_filtre - d_arriere_filtre 



def saturer (val : float, min : float, max : float) -> float :
    """ Bloque une valeur entre le min et le max en mm

    Args:
        val (float)
        min (float)
        max (float)
    Returns:
        float: la valeur bloquée
    """

    if val < min :
        return min
    if val > max :
        return max
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
    commande = KP_ROT * erreur
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


# petit test
for i in range (10) :
    cmd = boucle_controle(340,300)
    print(f"tour {i} : cmd = {cmd}")
    











