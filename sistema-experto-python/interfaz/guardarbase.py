# interfaz/guardarbase.py

import tkinter as tk
from tkinter import messagebox
import acciones

class GuardarBase:
    def __init__(self):
        self.master = tk.Toplevel()
        self.master.title("Guardar/Cargar Base de Conocimientos")
        self.master.geometry("400x200")
        self.master.resizable(False, False)

        self.lbl_file = tk.Label(self.master, text="Nombre del Archivo (sin extensión):")
        self.lbl_file.pack(pady=10)
        self.txt_file = tk.Entry(self.master)
        self.txt_file.pack(pady=5)

        self.btn_guardar = tk.Button(self.master, text="Guardar Base", command=self.guardar_base_json)
        self.btn_guardar.pack(pady=10)

        self.btn_cargar = tk.Button(self.master, text="Cargar Base", command=self.cargar_base_json)
        self.btn_cargar.pack(pady=10)

        self.btn_quit = tk.Button(self.master, text="Cerrar", command=self.master.destroy)
        self.btn_quit.pack(pady=10)

    def guardar_base_json(self):
        filename = self.txt_file.get().strip()
        if not filename:
            messagebox.showwarning("Advertencia", "Debe especificar un nombre de archivo.")
            return
        try:
            acciones.guardar(f"{filename}.json")
            messagebox.showinfo("Éxito", f"Base de conocimientos guardada en '{filename}.json'.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def cargar_base_json(self):
        filename = self.txt_file.get().strip()
        if not filename:
            messagebox.showwarning("Advertencia", "Debe especificar un nombre de archivo.")
            return
        try:
            acciones.cargar(f"{filename}.json")
            messagebox.showinfo("Éxito", f"Base de conocimientos cargada desde '{filename}.json'.")
            self.master.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))
