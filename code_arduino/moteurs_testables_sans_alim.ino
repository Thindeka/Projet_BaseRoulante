// Sans boutons, sans capteurs

const int pinPWM[4] = {5, 6, 9, 10};    // AG, AD, RG, RD
const int pinDIR[4] = {7, 8, 11, 12};   // AG, AD, RG, RD

const int sensMoteur[4] = {1, 1, 1, 1}; // tout est peut être en signe négatif, jsp faut tester

const int vitesseTest = 100; // valeur à parametrer jsp trop comment elle affecte le fonctionnement du "pseudo test "
const int tempsTest = 2000;

void setup() {
  Serial.begin(9600);

  for (int i = 0; i < 4; i++) {
    pinMode(pinPWM[i], OUTPUT);
    pinMode(pinDIR[i], OUTPUT);
    analogWrite(pinPWM[i], 0);
  }

  Serial.println("TEST MOTEURS MECANUM PRET");
  delay(2000);
}

void loop() {
  Serial.println("TEST AVANCE");
  commanderMecanum(vitesseTest, 0, 0);
  delay(tempsTest);

  Serial.println("STOP");
  arreterMoteurs();
  delay(1000);

  Serial.println("TEST RECUL");
  commanderMecanum(-vitesseTest, 0, 0);
  delay(tempsTest);

  Serial.println("STOP");
  arreterMoteurs();
  delay(1000);

  Serial.println("TEST LATERAL DROITE");
  commanderMecanum(0, vitesseTest, 0);
  delay(tempsTest);

  Serial.println("STOP");
  arreterMoteurs();
  delay(1000);

  Serial.println("TEST LATERAL GAUCHE");
  commanderMecanum(0, -vitesseTest, 0);
  delay(tempsTest);

  Serial.println("STOP");
  arreterMoteurs();
  delay(1000);

  Serial.println("TEST ROTATION DROITE");
  commanderMecanum(0, 0, vitesseTest);
  delay(tempsTest);

  Serial.println("STOP");
  arreterMoteurs();
  delay(1000);

  Serial.println("TEST ROTATION GAUCHE");
  commanderMecanum(0, 0, -vitesseTest);
  delay(tempsTest);

  Serial.println("STOP FINAL");
  arreterMoteurs();

  while (true) {
    // Fin du test
  }
}

void commanderUnMoteur(int moteur, int vitesse) {
  vitesse = vitesse * sensMoteur[moteur];
  vitesse = constrain(vitesse, -255, 255);

  Serial.print("Moteur ");
  Serial.print(moteur);
  Serial.print(" | vitesse = ");
  Serial.println(vitesse);

  if (vitesse >= 0) {
    digitalWrite(pinDIR[moteur], HIGH);
    analogWrite(pinPWM[moteur], vitesse);
  } else {
    digitalWrite(pinDIR[moteur], LOW);
    analogWrite(pinPWM[moteur], -vitesse);
  }
}

void commanderMoteursMecanum(int vAG, int vAD, int vRG, int vRD) {
  commanderUnMoteur(0, vAG);
  commanderUnMoteur(1, vAD);
  commanderUnMoteur(2, vRG);
  commanderUnMoteur(3, vRD);
}

void commanderMecanum(int vx, int vy, int omega) {
  int vAG = vx - vy - omega;
  int vAD = vx + vy + omega;
  int vRG = vx + vy - omega;
  int vRD = vx - vy + omega;

  int maxVal = max(max(abs(vAG), abs(vAD)), max(abs(vRG), abs(vRD)));

  if (maxVal > 255) {
    vAG = vAG * 255 / maxVal;
    vAD = vAD * 255 / maxVal;
    vRG = vRG * 255 / maxVal;
    vRD = vRD * 255 / maxVal;
  }

  commanderMoteursMecanum(vAG, vAD, vRG, vRD);
}

void arreterMoteurs() {
  for (int i = 0; i < 4; i++) {
    analogWrite(pinPWM[i], 0);
  }
}