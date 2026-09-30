# Microcontroladores

Repositorio de prácticas y proyectos con **Arduino**, **ESP32**, sensores y comunicación I2C.

## Contenido

### `Clase_1_Electronica`

Ejemplo introductorio para una placa **ESP32 Dev Module**. Configura:

- Comunicación serial a 9600 baudios.
- GPIO 2 como salida.
- GPIO 3 como entrada.
- Una entrada analógica en `A0`.

Este proyecto sirve como base para comenzar a trabajar con pines digitales, entradas analógicas y la función `setup()`/`loop()` de Arduino.

### `Sensor_VL53L0X`

Proyecto para utilizar dos sensores de distancia **VL53L0X** mediante I2C.

El programa:

- Controla cada sensor mediante los pines `XSHUT` 2 y 3.
- Asigna direcciones I2C diferentes: `0x30` y `0x31`.
- Lee la distancia de ambos sensores en milímetros.
- Muestra los resultados en el monitor serial.
- Informa cuando una medición está fuera de rango.

## Estructura

```text
Microcontroladores/
├── Clase_1_Electronica/
│   └── Clase_1_Electronica.ino
├── Sensor_VL53L0X/
│   └── Sensor_VL53L0X.ino
└── .github/
```

## Requisitos

- Arduino IDE o Visual Studio Code con PlatformIO.
- Placa Arduino compatible o ESP32 Dev Module.
- Cable USB.
- Para el proyecto VL53L0X:
  - 2 sensores VL53L0X.
  - Biblioteca `Adafruit_VL53L0X`.
  - Cables para alimentación, I2C y pines XSHUT.

## Instalación de la biblioteca

Desde el Arduino IDE abre:

**Sketch → Include Library → Manage Libraries**

Busca e instala:

```text
Adafruit VL53L0X
```

También puedes instalar sus dependencias si el administrador de bibliotecas las solicita.

## Uso

1. Clona el repositorio:

```bash
git clone https://github.com/Ssalazarp420/Microcontroladores.git
cd Microcontroladores
```

2. Abre el archivo `.ino` correspondiente.

3. Selecciona la placa y el puerto serial.

4. Compila y sube el programa.

5. Abre el monitor serial con la velocidad configurada:

```text
9600 baudios
```

## Conexión de los sensores VL53L0X

El proyecto utiliza los siguientes pines para controlar la activación de los sensores:

| Elemento | Pin |
|---|---:|
| XSHUT sensor 1 | GPIO 2 |
| XSHUT sensor 2 | GPIO 3 |
| SDA | Según la placa |
| SCL | Según la placa |
|

Ambos sensores comparten el bus I2C, pero se inicializan uno a uno para asignarles direcciones diferentes.

> Consulta el pinout de tu placa antes de realizar las conexiones. No alimentes los sensores con un voltaje diferente al especificado por el fabricante.

## Salida esperada

Al iniciar el proyecto de distancia, el monitor serial muestra mensajes similares a:

```text
Inicializando Sensores...
Sensores OK!
Sensor 1: 120 mm    Sensor 2: 185 mm
```

## Tecnologías

- C++
- Arduino
- ESP32
- I2C
- Sensor VL53L0X
- Biblioteca Adafruit VL53L0X

## Notas

- Las direcciones `0x30` y `0x31` se asignan durante la ejecución.
- Los sensores deben iniciar apagados mediante sus pines `XSHUT` para evitar conflictos con la dirección I2C predeterminada.
- Ajusta los pines si tu placa utiliza una distribución diferente.

## Licencia

Este repositorio no especifica actualmente una licencia de uso.

## Enlace

[Repositorio Microcontroladores](https://github.com/Ssalazarp420/Microcontroladores)
