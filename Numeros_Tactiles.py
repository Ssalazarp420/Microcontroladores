import tkinter as tk
from tkinter import messagebox

# Contraseña de ejemplo
contrasena_correcta = "1234"
entrada_actual = ""

# --- Funciones de la interfaz ---

def agregar_numero(numero):
    """Agrega un dígito a la entrada actual y actualiza la casilla de respuesta."""
    global entrada_actual
    entrada_actual += str(numero)
    casilla_respuesta.config(text=entrada_actual)

def borrar_ultimo():
    """Borra el último dígito ingresado."""
    global entrada_actual
    entrada_actual = entrada_actual[:-1]
    casilla_respuesta.config(text=entrada_actual)

def verificar_contrasena():
    """Verifica si la entrada actual coincide con la contraseña correcta."""
    global entrada_actual
    if entrada_actual == contrasena_correcta:
        messagebox.showinfo("Resultado", "¡Contraseña correcta!")
        entrada_actual = ""
    else:
        messagebox.showerror("Resultado", "Contraseña incorrecta. Inténtalo de nuevo.")
        entrada_actual = ""
    casilla_respuesta.config(text=entrada_actual)

# --- Configuración de la ventana principal ---

ventana = tk.Tk()
ventana.title("Teclado Numérico")
ventana.geometry("300x400")
ventana.configure(bg="#2c3e50")

# --- Creación de la casilla de respuesta ---

casilla_respuesta = tk.Label(ventana, text="", font=("Arial", 24), bg="#34495e", fg="white", bd=5, relief="groove")
casilla_respuesta.pack(pady=20, padx=20, ipadx=10, ipady=10, fill="x")

# --- Creación del marco para los botones ---

marco_botones = tk.Frame(ventana, bg="#2c3e50")
marco_botones.pack(pady=10)

# --- Creación de los botones del teclado ---

botones = [
    '1', '2', '3',
    '4', '5', '6',
    '7', '8', '9',
    'Borrar', '0', 'OK'
]

# Distribución de los botones en una cuadrícula
fila = 0
columna = 0
for boton in botones:
    if boton == 'OK':
        btn = tk.Button(marco_botones, text=boton, width=6, height=3, font=("Arial", 14), bg="#2ecc71", fg="white", command=verificar_contrasena)
    elif boton == 'Borrar':
        btn = tk.Button(marco_botones, text=boton, width=6, height=3, font=("Arial", 14), bg="#e74c3c", fg="white", command=borrar_ultimo)
    else:
        btn = tk.Button(marco_botones, text=boton, width=6, height=3, font=("Arial", 14), bg="#3498db", fg="white", command=lambda b=boton: agregar_numero(b))
    
    btn.grid(row=fila, column=columna, padx=5, pady=5)
    columna += 1
    if columna > 2:
        columna = 0
        fila += 1

# Iniciar el bucle principal de la aplicación
ventana.mainloop()