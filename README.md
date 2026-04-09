09/04/26

Thindeka

Travail ToF : gestion ORIENTATION 


d_avant (distance ToF avant) 
d_arriere (distance ToF arriere) 


Cas 1 : Base parallèle
-> d_avant = d_arriere

Cas 2 : Base de travers
-> d_avant != d_arriere

        Lit
        │
        │
        │
        |      ┌──────────────────────┐
        |      │ ToF avant      ↑     │
        |      │                 sens │
        |      │                 base │
        |      │ ToF arrière          │
        |      └──────────────────────┘
        |
        |
        |
        


Pipeline :

Lire les 2 ToF (distance en mm)
-> vérifier que les mesures sont valides (ex : pas de valeur nulle)
-> filtrer les mesures
-> calculer l’erreur (d_avant - d_arriere)
-> décider si la base est parallèle ou non
-> calculer une correction
-> envoyer la commande moteur


Blocs de code :
1. Lecture des capteurs
2. Validation
3. Filtrage
4. Calcul d'erreur
5. Controleur
6. Commande moteur


Cas de sécurité 
1. Un seul ToF voit le lit => ne pas corriger normalement, passer en défaut ou en recherche
2. Une mesure saute brutalement => ignorer si variation trop violente
3. Le lit disparait => arreter la correction
4. Oscillation autour de zéro => utilsier une zone morte





31/03/26 

Thindeka

Séparation officelle des tâches :

- Jihen : élec/cablage
- Alexandre : CAO, conception mécanique
- Thindeka : code

lien intéséssant TOF : https://wiki.ros.org/Drivers/Tutorials/DistanceMeasurementWithToFSensorVL53L1XPython 

Jihen 

- Alimentation → Test a faire
- Commande (cerveau) → Arduino + Bluetooth
- Action (moteurs) → driver + moteurs
- Capteurs → ultrason / IR / sécurité
