//Este código inicializa los dos sensores, les asigna una dirección I2C diferente (0x30 y 0x31) y luego lee y muestra la distancia de cada uno por separado en el monitor serial.
#include <Wire.h>
#include <Adafruit_VL53L0X.h>

// Pines XSHUT para cada sensor
#define SENSOR_1_XSHUT 2
#define SENSOR_2_XSHUT 3

// Objetos para cada sensor
Adafruit_VL53L0X lox1 = Adafruit_VL53L0X();
Adafruit_VL53L0X lox2 = Adafruit_VL53L0X();

void setup() {
  Serial.begin(9600);
  while (!Serial);

  // Inicializar pines XSHUT como salida y apagarlos (LOW)
  pinMode(SENSOR_1_XSHUT, OUTPUT);
  pinMode(SENSOR_2_XSHUT, OUTPUT);
  digitalWrite(SENSOR_1_XSHUT, LOW);
  digitalWrite(SENSOR_2_XSHUT, LOW);

  Serial.println("Inicializando Sensores...");

  // Encender y configurar el Sensor 1
  digitalWrite(SENSOR_1_XSHUT, HIGH);
  delay(10);
  if (!lox1.begin(0x30)) { // Asignar nueva dirección I2C
    Serial.println(F("Fallo al iniciar el sensor 1 :("));
    while(1);
  }

  // Encender y configurar el Sensor 2
  digitalWrite(SENSOR_2_XSHUT, HIGH);
  delay(10);
  if (!lox2.begin(0x31)) { // Asignar nueva dirección I2C
    Serial.println(F("Fallo al iniciar el sensor 2 :("));
    while(1);
  }

  Serial.println("Sensores OK!");
}

void loop() {
  VL53L0X_RangingMeasurementData_t measure1;
  lox1.rangingTest(&measure1, false);

  VL53L0X_RangingMeasurementData_t measure2;
  lox2.rangingTest(&measure2, false);

  // Lectura del Sensor 1
  if (measure1.RangeStatus != 4) {
    Serial.print("Sensor 1: ");
    Serial.print(measure1.RangeMilliMeter);
    Serial.print(" mm\t");
  } else {
    Serial.print("Sensor 1: Fuera de rango\t");
  }

  // Lectura del Sensor 2
  if (measure2.RangeStatus != 4) {
    Serial.print("Sensor 2: ");
    Serial.print(measure2.RangeMilliMeter);
    Serial.println(" mm");
  } else {
    Serial.println("Sensor 2: Fuera de rango");
  }

  delay(50);
}