import serial
import matplotlib.pyplot as plt
import re

# Configuración del puerto serial (ajusta el nombre del puerto)
# Para Windows: 'COM3', 'COM4', etc.
# Para macOS/Linux: '/dev/ttyACM0', '/dev/ttyUSB0', etc.
puerto_serial = serial.Serial('COM4', 115200)

# Inicializar la gráfica
plt.ion()  # Habilita el modo interactivo
fig, ax = plt.subplots()
ax.set_xlim(0, 1920)
ax.set_ylim(0, 1080)
ax.invert_yaxis()  # Invierte el eje Y para que (0,0) esté arriba a la izquierda
puntos, = ax.plot([], [], 'o', color='blue') # 'o' para puntos

# Limpiar los datos después de un tiempo
max_puntos = 20
puntos_x = []
puntos_y = []

print("Esperando datos del ESP32...")

try:
    while True:
        linea = puerto_serial.readline().decode('utf-8').strip()
        
        # Usar una expresión regular para encontrar los valores X e Y
        match = re.search(r'X(\d+)Y(\d+)', linea)
        if match:
            x = int(match.group(1))
            y = int(match.group(2))
            
            puntos_x.append(x)
            puntos_y.append(y)
            
            # Mantener un número máximo de puntos en la gráfica
            if len(puntos_x) > max_puntos:
                puntos_x.pop(0)
                puntos_y.pop(0)
                
            # Actualizar la gráfica
            puntos.set_data(puntos_x, puntos_y)
            fig.canvas.draw()
            fig.canvas.flush_events()

except KeyboardInterrupt:
    print("Programa detenido por el usuario.")
except Exception as e:
    print(f"Ocurrió un error: {e}")
finally:
    puerto_serial.close()
    plt.close()