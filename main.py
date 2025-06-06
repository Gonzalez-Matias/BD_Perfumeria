import subprocess
import sys
import tkinter as tk
from tkinter import ttk
from views import (
    menu_agregar_persona,
    agregar_movimiento_completo,
    agregar_producto,
    agregar_presentacion,
    mostrar_vista
)

def levantar_contenedor():
    try:
        print("🚀 Levantando el contenedor de base de datos...")
        subprocess.run(["docker-compose", "up", "-d"], check=True)
        print("✅ Contenedor levantado.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al levantar el contenedor: {e}")
        sys.exit(1)

def cerrar_contenedor():
    try:
        print("🛑 Cerrando el contenedor de base de datos...")
        subprocess.run(["docker-compose", "down"], check=True)
        print("✅ Contenedor cerrado.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al cerrar el contenedor: {e}")

if __name__ == "__main__":
    levantar_contenedor()
    try:
        root = tk.Tk()
        root.title("Interfaz Base de Datos Perfumería")
        root.state('zoomed')
        root.configure(bg="#c6c6c6")

        # Estilo de los botones
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton',
                        font=('Segoe UI', 12),
                        padding=10,
                        relief='flat',
                        background="#4B59A8",
                        foreground='white')
        style.map('TButton',
                  background=[('active', "#414D93")])

        # Frame para centrar
        frame = ttk.Frame(root, padding=30)
        frame.place(relx=0.5, rely=0.5, anchor='center')

        # Botones
        botones = [
            ("Agregar Persona", menu_agregar_persona),
            ("Agregar Movimiento Completo", agregar_movimiento_completo),
            ("Agregar Producto", agregar_producto),
            ("Agregar Presentación", agregar_presentacion),
            ("Mostrar Vistas", mostrar_vista)
        ]

        for texto, funcion in botones:
            ttk.Button(frame, text=texto, command=funcion, style='TButton').pack(pady=10, fill='x')

        root.mainloop()
    finally:
        cerrar_contenedor()
