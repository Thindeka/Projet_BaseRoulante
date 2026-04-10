# distances en mm

# DISTANCES 
US_MIN_DIST = 20
US_MAX_DIST = 2000

# FILTARGE
US_ALPHA = 0.3

# SEUILS
SEUIL_DANGER = 200
SEUIL_PROCHE = 500




def distance_synthetique (distance1 : float, distance2 : float) -> float :
    """ Retourne la distance synthetique d'un côté

    Args:
        distance1 (float)
        distance2 (float)

    Returns:
        float: la distance la plus petite
    """
    return min(distance1, distance2)



def mesure_valide (distance : float) -> bool :
    """ Retourne vrai si la distance est valide

    Args:
        distance (float): distance en mm

    Returns:
        bool 
    """
    return US_MIN_DIST <= distance <= US_MAX_DIST 




def filtrer (nouvelle_val : float, ancienne_val : float) -> float :
    """ filtre la valeur

    Args:
        nouvelle_val (float): en mm
        ancienne_val (float): en mm

    Returns:
        float: valeur filtrée
    """
    return US_ALPHA * nouvelle_val + (1 - US_ALPHA) * ancienne_val




def etat_distance (distance: float) -> str : 
    """ Retourne l'état de distance

    Args:
        distance (float): en mm

    Returns:
        str
    """
    if distance < SEUIL_DANGER:
        return "DANGER"
    if distance < SEUIL_PROCHE:
        return "PROCHE"
    return "LIBRE"