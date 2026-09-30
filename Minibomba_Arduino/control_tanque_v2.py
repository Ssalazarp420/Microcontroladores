import tkinter as tk
from tkinter import ttk, messagebox, TclError
import serial
import threading
import time

# --- CONFIGURACIÓN ---
PUERTO_SERIAL = 'COM5' # ¡¡¡CAMBIA ESTO POR TU PUERTO SERIE!!!
BAUD_RATE = 9600
VOLTAJE_REFERENCIA_ARDUINO = 5.0

# --- ESTILO Y DIMENSIONES DEL TANQUE VIRTUAL ---
COLOR_FONDO = "#2E2E2E"
COLOR_TEXTO = "#FFFFFF"
COLOR_DISPLAY = "#1E90FF"
COLOR_AGUA = "#1E90FF"
COLOR_TANQUE = "#AAAAAA"
ANCHO_CANVAS = 200
ALTO_CANVAS = 350
ALTO_REAL_TANQUE_CM = 15.0 # Altura máxima real del tanque en cm
COLOR_SUCCESS = "#228B22"
COLOR_ERROR = "#B22222"
COLOR_BOTON_MANUAL = "#464646"

class AppControlTanque:
    # Diccionario con tus nuevos datos de calibración.
    DATOS_CALIBRACION = {
        0.62: 0, 0.71: 1, 0.88: 2, 1.04: 3, 1.20: 4, 1.38: 5,
        1.57: 6, 1.74: 7, 1.96: 8, 2.14: 9, 2.25: 10
    }
    # Se crea una lista ordenada para la interpolación
    puntos_calibracion = sorted(DATOS_CALIBRACION.items())

    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard de Control de Tanque v5")
        self.root.configure(bg=COLOR_FONDO)
        self.root.geometry("600x620") # Aumentamos la altura para los nuevos controles

        self.arduino = None
        self.valor_sensor_raw = tk.StringVar(value="---")
        self.valor_sensor_voltaje = tk.StringVar(value="--- V")
        self.altura_actual_cm = tk.StringVar(value="--- cm")
        self.status_text = tk.StringVar(value="Inicializando...")
        self.control_activo = False
        
        # --- NUEVO: Variable para el slider de velocidad manual ---
        self.velocidad_manual_pct = tk.IntVar(value=100)

        self._crear_widgets()
        self._dibujar_tanque_estatico()
        self._conectar_arduino()
        self.root.protocol("WM_DELETE_WINDOW", self._al_cerrar)

    def _crear_widgets(self):
        # --- Layout principal con dos columnas ---
        main_frame = tk.Frame(self.root, bg=COLOR_FONDO)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        columna_control = tk.Frame(main_frame, bg=COLOR_FONDO)
        columna_control.grid(row=0, column=0, sticky="ns", padx=(0, 20))
        columna_tanque = tk.Frame(main_frame, bg=COLOR_FONDO)
        columna_tanque.grid(row=0, column=1, sticky="ns")

        # --- COLUMNA DE CONTROL (IZQUIERDA) ---
        # Frame Lectura
        frame_lectura = tk.LabelFrame(columna_control, text="Lectura en Tiempo Real", bg=COLOR_FONDO, fg=COLOR_TEXTO, padx=10, pady=10)
        frame_lectura.pack(pady=10, fill=tk.X)
        tk.Label(frame_lectura, text="Voltaje:", bg=COLOR_FONDO, fg=COLOR_TEXTO).grid(row=0, column=0, sticky="w")
        tk.Label(frame_lectura, textvariable=self.valor_sensor_voltaje, bg=COLOR_FONDO, fg=COLOR_DISPLAY, font=("Segoe UI", 24, "bold")).grid(row=0, column=1, sticky="e")
        tk.Label(frame_lectura, text="Altura Estimada:", bg=COLOR_FONDO, fg=COLOR_TEXTO).grid(row=1, column=0, sticky="w")
        tk.Label(frame_lectura, textvariable=self.altura_actual_cm, bg=COLOR_FONDO, fg="#DAA520", font=("Segoe UI", 24, "bold")).grid(row=1, column=1, sticky="e")

        # Frame Control Automático
        frame_auto = tk.LabelFrame(columna_control, text="Control Automático por Altura", bg=COLOR_FONDO, fg=COLOR_TEXTO, padx=10, pady=10)
        frame_auto.pack(pady=10, fill=tk.X)
        tk.Label(frame_auto, text="Altura Deseada:", bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(side=tk.LEFT, padx=5)
        self.combo_setpoint = ttk.Combobox(frame_auto, font=("Segoe UI", 10), width=8, state="readonly", values=[f"{i} cm" for i in range(11)])
        self.combo_setpoint.pack(side=tk.LEFT, padx=5)
        self.combo_setpoint.current(5)
        self.btn_iniciar = tk.Button(frame_auto, text="INICIAR", command=self._iniciar_control_auto, font=("Segoe UI", 10, "bold"), bg=COLOR_SUCCESS, fg="white")
        self.btn_iniciar.pack(side=tk.LEFT, padx=5)
        self.btn_detener = tk.Button(frame_auto, text="DETENER", command=self._detener_control_auto, font=("Segoe UI", 10, "bold"), bg=COLOR_ERROR, fg="white", state=tk.DISABLED)
        self.btn_detener.pack(side=tk.LEFT, padx=5)
        
        # --- NUEVO: Frame Control Manual ---
        frame_manual = tk.LabelFrame(columna_control, text="Control Manual de la Bomba", bg=COLOR_FONDO, fg=COLOR_TEXTO, padx=15, pady=15)
        frame_manual.pack(pady=20, fill=tk.X)
        self.btn_manual_on = tk.Button(frame_manual, text="ENCENDER", command=self._encender_bomba_manual, font=("Segoe UI", 12, "bold"), bg=COLOR_BOTON_MANUAL, fg="white", width=12, height=2)
        self.btn_manual_on.grid(row=0, column=0, rowspan=2, padx=(0, 20))
        self.btn_manual_off = tk.Button(frame_manual, text="APAGAR", command=self._apagar_bomba_manual, font=("Segoe UI", 12, "bold"), bg=COLOR_BOTON_MANUAL, fg="white", width=12, height=2)
        self.btn_manual_off.grid(row=0, column=1, rowspan=2)
        self.slider_velocidad = tk.Scale(frame_manual, from_=0, to=100, orient=tk.HORIZONTAL, variable=self.velocidad_manual_pct, bg=COLOR_FONDO, fg=COLOR_TEXTO, length=150, troughcolor=COLOR_DISPLAY, highlightthickness=0, command=self._actualizar_label_velocidad)
        self.slider_velocidad.grid(row=0, column=2, padx=(20, 0))
        self.lbl_velocidad_pct = tk.Label(frame_manual, text="Velocidad: 100%", bg=COLOR_FONDO, fg=COLOR_TEXTO, font=("Segoe UI", 10))
        self.lbl_velocidad_pct.grid(row=1, column=2, padx=(20, 0))
        self.slider_velocidad.bind("<ButtonRelease-1>", self._actualizar_velocidad_en_vivo)

        # --- COLUMNA DEL TANQUE (DERECHA) ---
        tk.Label(columna_tanque, text="Visualización del Tanque", bg=COLOR_FONDO, fg=COLOR_TEXTO, font=("Segoe UI", 12)).pack()
        self.canvas_tanque = tk.Canvas(columna_tanque, width=ANCHO_CANVAS, height=ALTO_CANVAS, bg=COLOR_FONDO, highlightthickness=0)
        self.canvas_tanque.pack(pady=10)

        # Barra de estado
        tk.Label(self.root, textvariable=self.status_text, bg=COLOR_DISPLAY, fg="white", font=("Segoe UI", 10)).pack(side=tk.BOTTOM, fill=tk.X, pady=(10,0))

    # El resto del código permanece igual, pero se añaden las nuevas funciones de control manual
    
    def _conectar_arduino(self):
        try:
            self.arduino = serial.Serial(PUERTO_SERIAL, BAUD_RATE, timeout=1)
            time.sleep(2)
            self.hilo_lectura = threading.Thread(target=self._leer_datos_arduino, daemon=True)
            self.hilo_lectura.start()
            self.status_text.set(f"Conectado a Arduino en {PUERTO_SERIAL}. Sistema listo.")
        except serial.SerialException:
            self.status_text.set(f"Error al conectar con {PUERTO_SERIAL}. Revisa el puerto y reinicia.")

    def _dibujar_tanque_estatico(self):
        self.padding = 20
        self.x0, self.y0 = self.padding, self.padding
        self.x1 = ANCHO_CANVAS - self.padding
        self.y1 = ALTO_CANVAS - self.padding
        self.canvas_tanque.create_rectangle(self.x0, self.y0, self.x1, self.y1, outline=COLOR_TANQUE, width=2)
        self.agua_rect = self.canvas_tanque.create_rectangle(self.x0, self.y1, self.x1, self.y1, fill=COLOR_AGUA, outline="")
        for cm in range(0, int(ALTO_REAL_TANQUE_CM) + 1, 5):
            y_pixel = self.y1 - (cm / ALTO_REAL_TANQUE_CM) * (self.y1 - self.y0)
            self.canvas_tanque.create_line(self.x0 - 5, y_pixel, self.x0, y_pixel, fill=COLOR_TANQUE)
            self.canvas_tanque.create_text(self.x0 - 15, y_pixel, text=f"{cm}", fill=COLOR_TEXTO)

    def _actualizar_dibujo_tanque(self, altura_cm):
        altura_cm = max(0, min(altura_cm, ALTO_REAL_TANQUE_CM))
        altura_dibujo_total = self.y1 - self.y0
        nueva_altura_pixel = (altura_cm / ALTO_REAL_TANQUE_CM) * altura_dibujo_total
        nuevo_y0_agua = self.y1 - nueva_altura_pixel
        self.canvas_tanque.coords(self.agua_rect, self.x0, nuevo_y0_agua, self.x1, self.y1)

    def _convertir_voltaje_a_cm(self, voltaje):
        if voltaje <= self.puntos_calibracion[0][0]: return self.puntos_calibracion[0][1]
        if voltaje >= self.puntos_calibracion[-1][0]: return self.puntos_calibracion[-1][1]
        for i in range(len(self.puntos_calibracion) - 1):
            v1, cm1 = self.puntos_calibracion[i]
            v2, cm2 = self.puntos_calibracion[i+1]
            if v1 <= voltaje <= v2:
                return cm1 + (voltaje - v1) * (cm2 - cm1) / (v2 - v1)
        return 0

    def _leer_datos_arduino(self):
        while self.arduino and self.arduino.is_open:
            try:
                linea = self.arduino.readline().decode('utf-8').strip()
                if linea:
                    valor_raw = int(linea)
                    voltaje = (valor_raw / 1023.0) * VOLTAJE_REFERENCIA_ARDUINO
                    altura_cm = self._convertir_voltaje_a_cm(voltaje)
                    self.valor_sensor_raw.set(str(valor_raw))
                    self.valor_sensor_voltaje.set(f"{voltaje:.2f} V")
                    self.altura_actual_cm.set(f"{altura_cm:.1f} cm")
                    self._actualizar_dibujo_tanque(altura_cm)
            except Exception: pass

    def _enviar_comando_velocidad(self, porcentaje):
        if self.arduino and self.arduino.is_open:
            valor_pwm = int((porcentaje / 100) * 255)
            self.arduino.write(f"SPEED,{valor_pwm}\n".encode('utf-8'))

    # --- NUEVO: Funciones de Control Manual ---
    def _encender_bomba_manual(self):
        self._detener_control_auto(silencioso=True)
        porcentaje = self.velocidad_manual_pct.get()
        self.status_text.set(f"Bomba encendida manualmente al {porcentaje}%.")
        self._enviar_comando_velocidad(porcentaje)

    def _apagar_bomba_manual(self):
        self._detener_control_auto(silencioso=True)
        self.status_text.set("Bomba apagada manualmente.")
        self._enviar_comando_velocidad(0)
    
    def _actualizar_label_velocidad(self, valor):
        self.lbl_velocidad_pct.config(text=f"Velocidad: {valor}%")
    
    def _actualizar_velocidad_en_vivo(self, event=None):
        if "manualmente" in self.status_text.get() and "encendida" in self.status_text.get():
             porcentaje = self.velocidad_manual_pct.get()
             self._enviar_comando_velocidad(porcentaje)

    # --- Funciones de Control Automático (modificadas para deshabilitar controles) ---
    def _iniciar_control_auto(self):
        self.control_activo = True
        # Deshabilitar controles manuales y auto
        self.btn_iniciar.config(state=tk.DISABLED)
        self.btn_detener.config(state=tk.NORMAL)
        self.combo_setpoint.config(state=tk.DISABLED)
        self.btn_manual_on.config(state=tk.DISABLED)
        self.btn_manual_off.config(state=tk.DISABLED)
        self.slider_velocidad.config(state=tk.DISABLED)
        
        altura_str = self.combo_setpoint.get()
        altura_objetivo_cm = float(altura_str.replace(" cm", ""))
        voltaje_objetivo = 0
        # Busca el voltaje objetivo en la tabla de calibración
        for v, h in self.DATOS_CALIBRACION.items():
            if h == int(altura_objetivo_cm):
                voltaje_objetivo = v
                break
        
        threading.Thread(target=self._logica_de_control, args=(voltaje_objetivo,), daemon=True).start()

    def _detener_control_auto(self, silencioso=False):
        self.control_activo = False
        self._enviar_comando_velocidad(0)
        if not silencioso: self.status_text.set("Control automático detenido.")
        # Habilitar todos los controles
        self.btn_iniciar.config(state=tk.NORMAL)
        self.btn_detener.config(state=tk.DISABLED)
        self.combo_setpoint.config(state=tk.NORMAL)
        self.btn_manual_on.config(state=tk.NORMAL)
        self.btn_manual_off.config(state=tk.NORMAL)
        self.slider_velocidad.config(state=tk.NORMAL)

    def _logica_de_control(self, voltaje_objetivo):
        umbral_voltaje = 0.05
        while self.control_activo:
            try:
                voltaje_actual_str = self.valor_sensor_voltaje.get().replace(" V", "")
                voltaje_actual = float(voltaje_actual_str)
            except (ValueError, TclError): time.sleep(0.5); continue
            
            if abs(voltaje_actual - voltaje_objetivo) <= umbral_voltaje:
                self.status_text.set(f"¡Nivel Alcanzado! Voltaje: {voltaje_actual:.2f} V")
                break
            
            accion = "SUMINISTRAR" if voltaje_actual < voltaje_objetivo else "SUCCIONAR"
            if messagebox.askokcancel("Acción Requerida", f"Por favor, configura la manguera para {accion} agua y presiona OK."):
                self.status_text.set(f"{accion} agua (Objetivo: {voltaje_objetivo:.2f} V)...")
                self._enviar_comando_velocidad(100) # El control auto siempre usa 100%
            else: break
            
            while self.control_activo:
                try:
                    current_v = float(self.valor_sensor_voltaje.get().replace(" V", ""))
                    if abs(current_v - voltaje_objetivo) <= umbral_voltaje: break
                except (ValueError, TclError): pass
                time.sleep(0.2)
        
        self._detener_control_auto()

    def _al_cerrar(self):
        self.control_activo = False
        if self.arduino and self.arduino.is_open:
            self._enviar_comando_velocidad(0)
            self.arduino.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style(root)
    style.theme_use('clam')
    app = AppControlTanque(root)
    root.mainloop()
