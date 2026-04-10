10/04/26

Thindeka


Travail Ultrason

Lit
│
│
│                           US          US
|                      ┌──────────────────────┐
|                      │ ToF avant      ↑     │  US
|                      │                 sens │
|                   US │                 base │  
|                      │ ToF arrière          │  US
|                      └──────────────────────┘
|                           US          US        
|



On a capteurs ultrason

Avant
    us_avant_gauche
    us_avant_droite
Arrière
    us_arriere_gauche
    us_arriere_droite
Gauche
    us_gauche_avant
    us_gauche_arriere
Droite
    us_droite_avant
    us_droite_arriere

Pour chaque côté le but est de résumer les 2 distances mesurées en une seule décision
=> on prend en compte la plus petite distance pour la sécurité


Pipeline :

Lire les 8 ultrasons
[vérifier les mesures]
         ↓            
[filtrer chaque capteur]
         ↓            
[regrouper les capteurs par côté]
         ↓            
[prendre la distance la plus petite par côté]
         ↓            
[classer chaque côté : libre / proche / danger]
         ↓            
[autoriser ou bloquer les mouvements]



À faire : rergouper code commun ToF, Ultrason





Ce qu'il reste à gérer pour le code ToF :
    - gestion des mesures invalides
    - validation temporelle ("je suis parallèle ssi l'erreur en en dessous d'un seuil pendant un certain moment)
    - machine d'états : recherche lit, alignement, aligné, défaut capteur
    - gestion du sens de rotation : va dépendre du cablage
    - bruit (ex : pb un des ToF, mesures aberrantes...)









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
        


Pipeline de la boucle de controle :

1. lire d_avant_brut
2. lire d_arriere_brut
3. vérifier si les deux mesures sont valides
4. initialiser le filtre si c'est le premier passage
5. sinon filtrer
6. calculer l'erreur
7. calculer la commande
8. envoyer la commande


[ToF avant + ToF arrière]
        ↓
[Validation mesures]
        ↓
[Filtrage]
        ↓
[Calcul erreur = d_avant - d_arriere]
        ↓
[Comparaison à un seuil]
        ↓
[Correcteur proportionnel]
        ↓
[Saturation]
        ↓
[Commande moteurs]
        ↓
[Rotation de la base] 



Cas de sécurité 
1. Un seul ToF voit le lit => ne pas corriger normalement, passer en défaut ou en recherche
2. Une mesure saute brutalement => ignorer si variation trop violente
3. Le lit disparait => arreter la correction
4. Oscillation autour de zéro => utilsier une zone morte



Principe du filtrage 
-> le ToF ne capte pas des valeurs completement stable (tremblements)
-> au lieu de prendre la nouvelle valeur telle quelle, on fait un melange entre la valeur ancienne et la valeur nouvelle
-> valeur_filtrée = un peu de la nouvelle + beaucoup de l’ancienne
-> alpha = 0.3 : bon compromis stable et réactif


Principe de la saturation 
-> éviter d'envoyer une commande trop grande


Principe de la correction (commande de roation)
-> plus l'erreur est grande (= plus on est de travers), plus on corrige (= plus on tourne)





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
