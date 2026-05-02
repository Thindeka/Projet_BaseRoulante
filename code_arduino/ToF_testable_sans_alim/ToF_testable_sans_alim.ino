#include <Wire.h>
#include <Adafruit_VL53L3CX.h>

#define XSHUT_AVANT 4
#define XSHUT_ARRIERE 5

Adafruit_VL53L3CX tof_avant;
Adafruit_VL53L3CX tof_arriere;

VL53LX_MultiRangingData_t mesure_avant;
VL53LX_MultiRangingData_t mesure_arriere;

void setup() {
  Serial.begin(9600);
  Wire.begin();

  pinMode(XSHUT_AVANT, OUTPUT);
  pinMode(XSHUT_ARRIERE, OUTPUT);

  // Eteindre les deux
  digitalWrite(XSHUT_AVANT, LOW);
  digitalWrite(XSHUT_ARRIERE, LOW);

  delay(10);

  // ===== TOF AVANT =====
  digitalWrite(XSHUT_AVANT, HIGH);
  delay(10);

  if (!tof_avant.begin(0x29, &Wire)) {
    Serial.println("Erreur ToF avant");
    while (1);
  }

  tof_avant.setAddress(0x30);

  // ===== TOF ARRIERE =====
  digitalWrite(XSHUT_ARRIERE, HIGH);
  delay(10);

  if (!tof_arriere.begin(0x29, &Wire)) {
    Serial.println("Erreur ToF arriere");
    while (1);
  }

  tof_arriere.setAddress(0x31);

  tof_avant.startRanging();
  tof_arriere.startRanging();

  Serial.println("ToF initialisés");
}

void loop() {

  int distance_avant = -1;
  int distance_arriere = -1;

  if (tof_avant.dataReady()) {
    tof_avant.getRangingData(&mesure_avant);

    distance_avant =
      mesure_avant.RangeData[0].RangeMilliMeter;

    tof_avant.clearInterrupt();
  }

  if (tof_arriere.dataReady()) {
    tof_arriere.getRangingData(&mesure_arriere);

    distance_arriere =
      mesure_arriere.RangeData[0].RangeMilliMeter;

    tof_arriere.clearInterrupt();
  }

  // envoi vers Python
  Serial.print(distance_avant);
  Serial.print(";");
  Serial.println(distance_arriere);


  // lecture commande venant de Python
  if (Serial.available() > 0) {

    String ligne = Serial.readStringUntil('\n');
    ligne.trim();

    float commande_rotation = ligne.toFloat();

    Serial.print("Commande recue : ");
    Serial.println(commande_rotation);

    // plus tard :
    // pilotage moteurs ici
  }

  delay(50);
}