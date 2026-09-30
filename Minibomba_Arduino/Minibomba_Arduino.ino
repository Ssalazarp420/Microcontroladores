/*
  Código Arduino para Controlador L298N (2 Motores)
  - Motor 1 (OUT 1/2): Lógica Invertida en dirección.
  - Motor 2 (OUT 3/4): Lógica Invertida en dirección (igual al 1).
  - Velocidad: PWM Normal (0-255).
*/

// --- PINES DE CONTROL MOTOR 1 (OUT 1 y 2) ---
const int pinVel1 = 9;   // ENA (Debe ser PWM)
const int pinDir1A = 8;  // IN1
const int pinDir1B = 7;  // IN2

// --- PINES DE CONTROL MOTOR 2 (OUT 3 y 4) ---
const int pinVel2 = 3;   // ENB (Debe ser PWM - Pines 3, 5, 6, 9, 10, 11 en UNO)
const int pinDir2A = 5;  // IN3
const int pinDir2B = 4;  // IN4

// --- VARIABLES DE ESTADO ---
// Motor 1
int velPorcentaje1 = 80; 
bool motor1Encendido = false;

// Motor 2
int velPorcentaje2 = 80;
bool motor2Encendido = false;

void setup() {
  // Configuración Pines Motor 1
  pinMode(pinVel1, OUTPUT);
  pinMode(pinDir1A, OUTPUT);
  pinMode(pinDir1B, OUTPUT);

  // Configuración Pines Motor 2
  pinMode(pinVel2, OUTPUT);
  pinMode(pinDir2A, OUTPUT);
  pinMode(pinDir2B, OUTPUT);

  Serial.begin(9600);

  Serial.println("--- Control Dual L298N ---");
  Serial.println("MOTOR 1: 'e' (Encender), 'a' (Apagar), 'v[0-100]' (Velocidad)");
  Serial.println("MOTOR 2: 'i' (Iniciar),  'p' (Parar),  'x[0-100]' (Velocidad)");
  Serial.println("--------------------------");

  // Estado inicial apagado
  apagarMotor1();
  apagarMotor2();
}

void loop() {
  if (Serial.available() > 0) {
    char comando = Serial.read();
    
    switch (comando) {
      // --- COMANDOS MOTOR 1 ---
      case 'e': encenderMotor1(); break;
      case 'a': apagarMotor1();   break;
      case 'v': 
        ajustarVelocidad1(Serial.parseInt());
        break;

      // --- COMANDOS MOTOR 2 ---
      case 'i': encenderMotor2(); break; // 'i' de Iniciar
      case 'p': apagarMotor2();   break; // 'p' de Parar
      case 'x': 
        ajustarVelocidad2(Serial.parseInt()); // 'x' para diferenciar de 'v'
        break;

      // --- COMANDO LIMPIEZA/ERROR ---
      default:
        // Ignorar saltos de línea o caracteres vacíos comunes
        if(comando != '\n' && comando != '\r') {
           // Serial.println("Comando no reconocido."); // Opcional: Descomentar si se quiere depurar
        }
        break;
    }
  }
}

// ==========================================
// FUNCIONES MOTOR 1
// ==========================================

void encenderMotor1() {
  Serial.print("M1 ENCENDIDO al ");
  Serial.print(velPorcentaje1);
  Serial.println("%");

  // Dirección (Lógica Invertida según tu código original)
  digitalWrite(pinDir1A, LOW);
  digitalWrite(pinDir1B, HIGH);

  int valorPWM = map(velPorcentaje1, 0, 100, 0, 255);
  analogWrite(pinVel1, valorPWM);
  motor1Encendido = true;
}

void apagarMotor1() {
  Serial.println("M1 APAGADO.");
  digitalWrite(pinDir1A, LOW);
  digitalWrite(pinDir1B, LOW);
  analogWrite(pinVel1, 0);
  motor1Encendido = false;
}

void ajustarVelocidad1(int nuevoPorcentaje) {
  velPorcentaje1 = constrain(nuevoPorcentaje, 0, 100);
  Serial.print("M1 Vel ajustada: "); Serial.println(velPorcentaje1);

  if (!motor1Encendido && velPorcentaje1 > 0) {
    encenderMotor1();
  } else if (motor1Encendido) {
    if (velPorcentaje1 == 0) apagarMotor1();
    else {
      int valorPWM = map(velPorcentaje1, 0, 100, 0, 255);
      analogWrite(pinVel1, valorPWM);
    }
  }
}

// ==========================================
// FUNCIONES MOTOR 2
// ==========================================

void encenderMotor2() {
  Serial.print("M2 ENCENDIDO al ");
  Serial.print(velPorcentaje2);
  Serial.println("%");

  // Dirección (Replicando la lógica invertida del Motor 1)
  digitalWrite(pinDir2A, LOW);
  digitalWrite(pinDir2B, HIGH);

  int valorPWM = map(velPorcentaje2, 0, 100, 0, 255);
  analogWrite(pinVel2, valorPWM);
  motor2Encendido = true;
}

void apagarMotor2() {
  Serial.println("M2 APAGADO.");
  digitalWrite(pinDir2A, LOW);
  digitalWrite(pinDir2B, LOW);
  analogWrite(pinVel2, 0);
  motor2Encendido = false;
}

void ajustarVelocidad2(int nuevoPorcentaje) {
  velPorcentaje2 = constrain(nuevoPorcentaje, 0, 100);
  Serial.print("M2 Vel ajustada: "); Serial.println(velPorcentaje2);

  if (!motor2Encendido && velPorcentaje2 > 0) {
    encenderMotor2();
  } else if (motor2Encendido) {
    if (velPorcentaje2 == 0) apagarMotor2();
    else {
      int valorPWM = map(velPorcentaje2, 0, 100, 0, 255);
      analogWrite(pinVel2, valorPWM);
    }
  }
}