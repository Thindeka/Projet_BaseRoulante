# distances en mm

# SEUILS
SEUIL_SECURITE_LONGUEUR = 80  
SEUIL_SECURITE_LARGEUR = 60

# DISTANCES
US_MIN_DIST = 60
US_MAX_DIST = 2000

# FILTRAGE
US_ALPHA = 0.3

# SEUIL
SEUIL_DANGER = 200

# VARIABLES GLOBALES
d_avant_filtre = 0.0
d_arriere_filtre = 0.0
d_gauche_filtre = 0.0
d_droite_filtre = 0.0

init_filtre_us = False



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




def obstacle_sur_longueur (distance : float) -> bool :
    return distance < SEUIL_SECURITE_LONGUEUR




def obstacle_sur_largeur (distance : float) -> bool :
    return distance < SEUIL_SECURITE_LARGEUR



def boucle_controle_ultrasons(d_avant_brut: float, d_arriere_brut: float, d_gauche_brut: float, d_droite_brut: float) -> dict:
    """ Traite les 4 mesures ultrason et retourne une décision de stop.

    Args:
        d_avant_brut (float): mm
        d_arriere_brut (float): mm
        d_gauche_brut (float): mm
        d_droite_brut (float): mm

    Returns:
        dict: de la forme 
        { "stop": bool,
          "obstacle": bool,
          "raison": string
        }
    """

    global d_avant_filtre, d_arriere_filtre, d_gauche_filtre, d_droite_filtre
    global init_filtre_us

    # 1. Vérification des mesures
    if (not mesure_valide(d_avant_brut) or not mesure_valide(d_arriere_brut) or not mesure_valide(d_gauche_brut) or not mesure_valide(d_droite_brut)) :
        return {
            "stop": True,
            "obstacle": True,
            "raison": "Mesure ultrason invalide"
        }

    # 2. Initialisation ou mise à jour du filtre
    if not init_filtre_us :
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

    # 3. Détection obstacle sur la longueur
    if obstacle_sur_longueur(d_avant_filtre):
        return {
            "stop": True,
            "obstacle": True,
            "raison": "Obstacle proche à l'avant",
            "distances_filtrees": {
                "avant": d_avant_filtre,
                "arriere": d_arriere_filtre,
                "gauche": d_gauche_filtre,
                "droite": d_droite_filtre
            }
        }

    if obstacle_sur_longueur(d_arriere_filtre):
        return {
            "stop": True,
            "obstacle": True,
            "raison": "Obstacle proche à l'arriere",
            "distances_filtrees": {
                "avant": d_avant_filtre,
                "arriere": d_arriere_filtre,
                "gauche": d_gauche_filtre,
                "droite": d_droite_filtre
            }
        }

    # 4. Détection obstacle sur la largeur
    if obstacle_sur_largeur(d_gauche_filtre):
        return {
            "stop": True,
            "obstacle": True,
            "raison": "Obstacle proche à gauche",
            "distances_filtrees": {
                "avant": d_avant_filtre,
                "arriere": d_arriere_filtre,
                "gauche": d_gauche_filtre,
                "droite": d_droite_filtre
            }
        }

    if obstacle_sur_largeur(d_droite_filtre):
        return {
            "stop": True,
            "obstacle": True,
            "raison": "Obstacle proche à droite",
            "distances_filtrees": {
                "avant": d_avant_filtre,
                "arriere": d_arriere_filtre,
                "gauche": d_gauche_filtre,
                "droite": d_droite_filtre
            }
        }

    # 5. Aucun obstacle détecté
    return {
        "stop": False,
        "obstacle": False,
        "raison": "Aucun obstacle proche",
        "distances_filtrees": {
            "avant": d_avant_filtre,
            "arriere": d_arriere_filtre,
            "gauche": d_gauche_filtre,
            "droite": d_droite_filtre
        }
    }

    