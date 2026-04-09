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



def mesure_valide (d) :
    return MIN_DIST <= d <= MAX_DIST 




