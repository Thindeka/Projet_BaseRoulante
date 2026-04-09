# VARIABLES GLOBALES

# distances en mm

# CAPTEURS 
MIN_DIST = 50  
MAX_DIST = 800

# FILTARGE
ALPHA = 0.3 ;     

# ALIGNEMENT
SEUIL_PARALLELISME = 10

# CONTROLE 
KP_ROT = 0.02 
ROT_MAX = 0.3

# VALIDATION TEMPORELLE
TEMPS_STABLE_MS = 0


d_avant_filtre = 0
d_arrire_filtre = 0
init_filtre = False



def mesure_valide (d : float) -> bool :
    """ Retourne vrai si la distance d est valide

    Args:
        d (float): distance

    Returns:
        bool 
    """
    return MIN_DIST <= d <= MAX_DIST 




def filtrer (nouvelle_val : float, ancienne_val : float) -> float :
    """_summary_

    Args:
        nouvelle_val (float): _description_
        ancienne_val (float): _description_

    Returns:
        float: valeur filtrée
    """
    return ALPHA * nouvelle_val + (1 - ALPHA) * ancienne_val








