# Microcontroladores

Repositorio de prácticas y proyectos con **Arduino**, **ESP32**, sensores, motores, interfaces gráficas y comunicación serial/I2C.

## Contenido

### `Clase_1_Electronica`

Ejemplo introductorio para una placa **ESP32 Dev Module**. Configura:

- Comunicación serial a 9600 baudios.
- GPIO 2 como salida.
- GPIO 3 como entrada.
- Una entrada analógica en `A0`.

### `Sensor_VL53L0X`

Proyecto para utilizar dos sensores de distancia **VL53L0X** mediante I2C.

- Controla los sensores mediante los pines `XSHUT` 2 y 3.
- Asigna las direcciones I2C `0x30` y `0x31`.
- Lee la distancia de ambos sensores en milímetros.
- Muestra los resultados en el monitor serial.
- Informa cuando una medición está fuera de rango.

Requiere la biblioteca `Adafruit_VL53L0X`.

### `Minibomba_Arduino`

Sistema de control de dos motores o bombas mediante un módulo **L298N** y Arduino.

- Motor 1: velocidad PWM en el pin 9; dirección en los pines 8 y 7.
- Motor 2: velocidad PWM en el pin 3; dirección en los pines 5 y 4.
- Control independiente de encendido, apagado y velocidad.
- Velocidad configurable entre 0 y 100 %.
- Comunicación serial a 9600 baudios.

Comandos disponibles:

| Comando | Acción |
|---|---|
| `e` | Enciende el motor 1 |
| `a` | Apaga el motor 1 |
| `v[0-100]` | Ajusta la velocidad del motor 1 |
| `i` | Enciende el motor 2 |
| `p` | Apaga el motor 2 |
| `x[0-100]` | Ajusta la velocidad del motor 2 |

El archivo `control_tanque_v2.py` proporciona una interfaz gráfica en Tkinter para:

- Leer el sensor conectado al Arduino.
- Convertir el voltaje en una altura estimada.
- Visualizar el nivel de un tanque.
- Controlar la bomba manualmente.
- Ejecutar un control automático por altura deseada.
- Ajustar la velocidad de la bomba mediante comandos seriales.

## Scripts auxiliares

### `Numeros_Tactiles.py`

Aplicación gráfica desarrollada con **Tkinter** que simula un teclado numérico táctil.

- Permite ingresar números.
- Incluye botones para borrar y confirmar.
- Verifica una contraseña de ejemplo.
- Muestra mensajes de éxito o error.

> La contraseña incluida en el ejemplo es `1234`. Debe cambiarse antes de utilizar el programa en un entorno real.

### `Graficar_Mouse_Vl53L0X.py`

Programa en Python que recibe coordenadas por puerto serial y las representa en tiempo real con **Matplotlib**.

Espera mensajes con el formato:

```text
X<coordenada_x>Y<coordenada_y>
```

El script mantiene los últimos 20 puntos y configura el área de visualización como una pantalla de 1920 × 1080 píxeles.

## Estructura

```text
Microcontroladores/
├── Clase_1_Electronica/
│   └── Clase_1_Electronica.ino
├── Sensor_VL53L0X/
│   └── Sensor_VL53L0X.ino
├── Minibomba_Arduino/
│   ├── Minibomba_Arduino.ino
│   └── control_tanque_v2.py
├── Graficar_Mouse_Vl53L0X.py
├── Numeros_Tactiles.py
└── .github/
```

## Requisitos

- Arduino IDE o Visual Studio Code con PlatformIO.
- Python 3.8 o superior para los scripts auxiliares.
- Placa Arduino compatible o ESP32 Dev Module.
- Cable USB.
- Para el proyecto VL53L0X: dos sensores VL53L0X y la biblioteca `Adafruit_VL53L0X`.
- Para el proyecto de bombas: módulo L298N, motores o minibombas y un sensor analógico.

## Dependencias de Python

Instala las bibliotecas necesarias con:

```bash
pip install pyserial matplotlib
```

`tkinter` normalmente viene incluido con Python. En algunas distribuciones Linux puede requerir instalación adicional mediante el gestor de paquetes del sistema.

## Instalación de la biblioteca VL53L0X

Desde Arduino IDE abre:

**Sketch → Include Library → Manage Libraries**

Busca e instala:

```text
Adafruit VL53L0X
```

## Uso

1. Clona el repositorio:

```bash
git clone https://github.com/Ssalazarp420/Microcontroladores.git
cd Microcontroladores
```

2. Abre el proyecto o archivo correspondiente.

3. Selecciona la placa y el puerto serial.

4. Compila y sube el programa Arduino.

5. Ajusta en los scripts Python el puerto serial utilizado, por ejemplo `COM4` o `COM5` en Windows, o `/dev/ttyUSB0` en Linux.

6. Ejecuta el script deseado:

```bash
python Numeros_Tactiles.py
python Graficar_Mouse_Vl53L0X.py
python Minibomba_Arduino/control_tanque_v2.py
```

## Conexión de los sensores VL53L0X

| Elemento | Pin |
|---|---:|
| XSHUT sensor 1 | GPIO 2 |
| XSHUT sensor 2 | GPIO 3 |
| SDA | Según la placa |
| SCL | Según la placa |

Ambos sensores comparten el bus I2C, pero se inicializan uno a uno para asignarles direcciones diferentes.

## Monitor serial

La mayoría de los ejemplos utiliza:

```text
9600 baudios
```

El proyecto de lectura de coordenadas debe utilizar la velocidad configurada por el dispositivo que envía los datos. Verifica siempre que la velocidad del script Python y la del microcontrolador coincidan.

## Tecnologías

- C++ / Arduino
- Python
- ESP32
- Arduino
- I2C
- UART / comunicación serial
- Tkinter
- Matplotlib
- Sensor VL53L0X
- Driver L298N

## Notas de seguridad

- No alimentes motores o bombas directamente desde los pines de la placa.
- Utiliza una fuente externa adecuada para motores y conecta correctamente las tierras comunes.
- Verifica los niveles de voltaje antes de conectar sensores o módulos.
- Cambia las contraseñas de ejemplo y evita almacenar credenciales reales en el código.
- Ajusta los puertos seriales a la configuración de tu equipo.

## Licencia

Este repositorio no especifica actualmente una licencia de uso.

## Enlace

[Repositorio Microcontroladores](https://github.com/Ssalazarp420/Microcontroladores)
