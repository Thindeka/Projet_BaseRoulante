#define TRIG_PIN 9
#define ECHO_PIN 10

#define ENC_G_A 2
#define ENC_G_B 22

#define ENC_D_A 3
#define ENC_D_B 23

volatile long ticks_gauche = 0;
volatile long ticks_droite = 0;

String commande_python = "";

void encoderGaucheISR() {
  if (digitalRead(ENC_G_B) == HIGH) {
    ticks_gauche++;
  } else {
    ticks_gauche--;
  }
}

void encoderDroiteISR() {
  if (digitalRead(ENC_D_B) == HIGH) {
    ticks_droite++;
  } else {
    ticks_droite--;
  }
}

float lireDistanceUltrasonMm() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);

  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duree = pulseIn(ECHO_PIN, HIGH, 30000);

  if (duree == 0) {
    return -1;
  }

  return duree * 0.343 / 2.0;
}

void setup() {
  Serial.begin(9600);

  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  pinMode(ENC_G_A, INPUT_PULLUP);
  pinMode(ENC_G_B, INPUT_PULLUP);
  pinMode(ENC_D_A, INPUT_PULLUP);
  pinMode(ENC_D_B, INPUT_PULLUP);

  attachInterrupt(digitalPinToInterrupt(ENC_G_A), encoderGaucheISR, CHANGE);
  attachInterrupt(digitalPinToInterrupt(ENC_D_A), encoderDroiteISR, CHANGE);
}

void loop() {
  float distance_avant = lireDistanceUltrasonMm();

  long tg;
  long td;

  noInterrupts();
  tg = ticks_gauche;
  td = ticks_droite;
  interrupts();

  // Format envoyé à Python :
  // distance_avant;ticks_gauche;ticks_droite
  Serial.print(distance_avant);
  Serial.print(";");
  Serial.print(tg);
  Serial.print(";");
  Serial.println(td);

  // Réception commande Python
  if (Serial.available() > 0) {
    commande_python = Serial.readStringUntil('\n');
    commande_python.trim();

    if (commande_python == "STOP") {
      // Plus tard : couper moteurs ici
    }

    if (commande_python == "AVANCE") {
      // Plus tard : commander moteurs ici
    }
  }

  delay(100);
}