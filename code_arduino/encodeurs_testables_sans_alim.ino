// =====================================================
// TEST DES 4 ENCODEURS - ARDUINO MEGA
// =====================================================

// Ordre :
// 0 = Avant Gauche
// 1 = Avant Droite
// 2 = Arrière Gauche
// 3 = Arrière Droite

const int pinEncA[4] = {2, 3, 18, 19};      // Interruptions Mega
const int pinEncB[4] = {22, 23, 24, 25};    // Broches normales

volatile long compteurTics[4] = {0, 0, 0, 0};

// Mets -1 si un encodeur compte dans le mauvais sens
const int sensEncodeur[4] = {1, 1, 1, 1};

void setup() {
  Serial.begin(9600);

  for (int i = 0; i < 4; i++) {
    pinMode(pinEncA[i], INPUT_PULLUP);
    pinMode(pinEncB[i], INPUT_PULLUP);
  }

  attachInterrupt(digitalPinToInterrupt(pinEncA[0]), gererEncodeur0, RISING);
  attachInterrupt(digitalPinToInterrupt(pinEncA[1]), gererEncodeur1, RISING);
  attachInterrupt(digitalPinToInterrupt(pinEncA[2]), gererEncodeur2, RISING);
  attachInterrupt(digitalPinToInterrupt(pinEncA[3]), gererEncodeur3, RISING);

  Serial.println("Test des 4 encodeurs prêt.");

}

void loop() {
  afficherCompteurs();
  delay(500);
}

long lireCompteur(int moteur) {
  noInterrupts();
  long valeur = compteurTics[moteur];
  interrupts();
  return valeur;
}

void afficherCompteurs() {
  Serial.print("AG: ");
  Serial.print(lireCompteur(0));

  Serial.print(" | AD: ");
  Serial.print(lireCompteur(1));

  Serial.print(" | RG: ");
  Serial.print(lireCompteur(2));

  Serial.print(" | RD: ");
  Serial.println(lireCompteur(3));
}

void gererEncodeur(int moteur) {
  if (digitalRead(pinEncB[moteur]) == HIGH) {
    compteurTics[moteur] += sensEncodeur[moteur];
  } else {
    compteurTics[moteur] -= sensEncodeur[moteur];
  }
}



void gererEncodeur0() {
  gererEncodeur(0);
}

void gererEncodeur1() {
  gererEncodeur(1);
}

void gererEncodeur2() {
  gererEncodeur(2);
}

void gererEncodeur3() {
  gererEncodeur(3);
}