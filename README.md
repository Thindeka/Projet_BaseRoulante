09/04/26


Travail TOF : gestion ORIENTATION 

d_avant (distance TOF avant) 
d_arriere (distance TOF arriere) 

Cas 1 : Base parallèle
-> d_avant = d_arriere

Cas 2 : Base de travers
-> d_avant != d_arriere

Pipeline :

    if d_avant = d_arriere : on est bien parallèle

    else : 
        if d_avant > d_arriere : 
            while d_avant > d_arriere :
                on tourne vers la gauche 
            end
        end 
        while d_avant < d_arriere :
            on tourne vers la droite 
        end
















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
