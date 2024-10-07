# interfaz/insertarbase.py

import tkinter as tk
from tkinter import ttk, messagebox
import acciones

class InsertarBase:
    def __init__(self):
        self.master = tk.Toplevel()
        self.master.title("Insertar Entradas y Propiedades")
        self.master.geometry("600x400")
        self.master.resizable(False, False)

        self.lbl_base = tk.Label(self.master, text="Entradas y Propiedades Existentes")
        self.lbl_base.pack(pady=10)

        self.entradas = ttk.Treeview(self.master)
        self.entradas.pack(expand=True, fill='both', padx=20, pady=10)
        self.entradas.bind("<<TreeviewSelect>>", self.item_selected)

        self.fill_base_tree_view()

        self.lbl_entry = tk.Label(self.master, text="Nombre de la Entrada:")
        self.lbl_entry.pack(pady=5)
        self.txt_entry = tk.Entry(self.master)
        self.txt_entry.pack(pady=5)

        self.lbl_prop = tk.Label(self.master, text="Nombre de la Propiedad:")
        self.lbl_prop.pack(pady=5)
        self.txt_prop = tk.Entry(self.master)
        self.txt_prop.pack(pady=5)

        self.btn_insertar = tk.Button(self.master, text="Insertar Propiedad", command=self.add_propiedad)
        self.btn_insertar.pack(pady=10)

        self.btn_quit = tk.Button(self.master, text="Cerrar", command=self.master.destroy)
        self.btn_quit.pack(pady=10)

    def fill_base_tree_view(self):
        for item in self.entradas.get_children():
            self.entradas.delete(item)
        base = self.entradas.insert("", tk.END, text="Base")
        base_entries = acciones.get_base_entries()
        for entry in base_entries:
            nombre = self.entradas.insert(base, tk.END, text=entry.name, tags=("tag_select",))
            for prop in entry.properties:
                self.entradas.insert(nombre, tk.END, text=prop.name)

    def add_propiedad(self):
        entrada = self.txt_entry.get().strip()
        propiedad = self.txt_prop.get().strip()
        if not entrada or not propiedad:
            messagebox.showwarning("Advertencia", "Ambos campos son obligatorios.")
            return
        try:
            acciones.insertar(entrada, propiedad)
            messagebox.showinfo("Éxito", f"Propiedad '{propiedad}' añadida a la entrada '{entrada}'.")
            self.txt_prop.delete(0, "end")
            self.fill_base_tree_view()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def item_selected(self, event):
        selected_item = self.entradas.focus()
        item_text = self.entradas.item(selected_item, 'text')
        self.txt_entry.delete(0, 'end')
        self.txt_entry.insert(0, item_text)
