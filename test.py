# distances en mm

# DISTANCES
US_MIN_DIST = 20
US_MAX_DIST = 2000

# FILTRAGE
US_ALPHA = 0.3

# SEUILS
SEUIL_DANGER = 200
SEUIL_PROCHE = 500


def distance_synthetique(distance1: float, distance2: float) -> float:
    """Retourne la distance synthetique d'un côté."""
    return min(distance1, distance2)


def mesure_valide(distance: float) -> bool:
    """Retourne vrai si la distance est valide."""
    return US_MIN_DIST <= distance <= US_MAX_DIST


def filtrer(nouvelle_val: float, ancienne_val: float) -> float:
    """Filtre la valeur."""
    return US_ALPHA * nouvelle_val + (1 - US_ALPHA) * ancienne_val


def etat_distance(distance: float) -> str:
    """Retourne l'état de distance."""
    if distance < SEUIL_DANGER:
        return "DANGER"
    if distance < SEUIL_PROCHE:
        return "PROCHE"
    return "LIBRE"


def lancer_tests():
    print("=== TEST distance_synthetique ===")
    print(distance_synthetique(300, 450))   # attendu : 300
    print(distance_synthetique(120, 80))    # attendu : 80
    print(distance_synthetique(500, 500))   # attendu : 500

    print("\n=== TEST mesure_valide ===")
    print(mesure_valide(10))     # attendu : False
    print(mesure_valide(20))     # attendu : True
    print(mesure_valide(1500))   # attendu : True
    print(mesure_valide(2000))   # attendu : True
    print(mesure_valide(2500))   # attendu : False

    print("\n=== TEST filtrer ===")
    print(filtrer(320, 300))     # attendu : 306.0
    print(filtrer(300, 300))     # attendu : 300.0
    print(filtrer(100, 200))     # attendu : 170.0

    print("\n=== TEST etat_distance ===")
    print(etat_distance(100))    # attendu : DANGER
    print(etat_distance(199))    # attendu : DANGER
    print(etat_distance(200))    # attendu : PROCHE
    print(etat_distance(350))    # attendu : PROCHE
    print(etat_distance(499))    # attendu : PROCHE
    print(etat_distance(500))    # attendu : LIBRE
    print(etat_distance(800))    # attendu : LIBRE


lancer_tests()