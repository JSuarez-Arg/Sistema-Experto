# acciones.py

from experto_general.engine import Engine
from experto_general.base import BaseConocimientos
from tkinter import messagebox

# Instancia global del motor de inferencia
engine_instance = Engine(BaseConocimientos())
engine = engine_instance

def insertar(nombre, prop):
    if nombre and prop:
        entry = engine.base.get_or_add_entry(nombre)
        entry.get_or_add_prop(prop)
        print(f"Entrada '{nombre}' con propiedad '{prop}' añadida correctamente.")
    else:
        print("No se admiten valores vacíos.")
        messagebox.showwarning("Advertencia", "No se admiten valores vacíos.")

def get_base_entries():
    return engine.base.entries

def guardar(entrada):
    if entrada:
        engine.base.to_json(entrada)
        messagebox.showinfo("Éxito", f"Base de conocimientos guardada en '{entrada}'.")
    else:
        messagebox.showwarning("Advertencia", "Debe especificar un nombre de archivo.")

def cargar(entrada):
    if entrada:
        try:
            engine.base.from_json(entrada)
            messagebox.showinfo("Éxito", f"Base de conocimientos cargada desde '{entrada}'.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la base de conocimientos: {e}")
    else:
        messagebox.showwarning("Advertencia", "Debe especificar un nombre de archivo.")
