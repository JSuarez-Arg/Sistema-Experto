# interfaz/consultarbase.py

import tkinter as tk
from tkinter import messagebox
from experto_general.response import Response
from acciones import engine

class ConsultarBase:
    def __init__(self):
        self.master = tk.Toplevel()
        self.master.title("Consulta al Sistema Experto")
        self.master.geometry("600x300")
        self.master.resizable(False, False)

        self.lbl_question = tk.Label(self.master, text="Iniciando consulta...", wraplength=500, justify="left")
        self.lbl_question.pack(pady=20)

        self.btn_yes = tk.Button(self.master, text="Sí", width=10, command=self._send_yes)
        self.btn_yes.pack(side=tk.LEFT, padx=50, pady=20)

        self.btn_no = tk.Button(self.master, text="No", width=10, command=self._send_no)
        self.btn_no.pack(side=tk.RIGHT, padx=50, pady=20)

        # Reiniciar el motor para una nueva consulta
        engine.reset()
        next_question = engine.get_next_question()
        if next_question:
            self.lbl_question.config(text=next_question.name)
        else:
            self._finished()

    def _send_yes(self):
        self._handle_response(Response.YES)

    def _send_no(self):
        self._handle_response(Response.NO)

    def _handle_response(self, response: Response):
        engine.set_response(response)
        next_question = engine.get_next_question()
        if next_question:
            self.lbl_question.config(text=next_question.name)
        else:
            self._finished()

    def _finished(self):
        entry = engine.evaluate()
        if entry is None:
            messagebox.showerror("Resultado", "No se encontró ninguna coincidencia.")
        else:
            mensaje = f"Recomendación: {entry.name}\n\nDescripción: {entry.description}\n\nPropiedades Confirmadas:"
            for prop in engine.accepted_properties:
                mensaje += f"\n- {prop.name}"
            messagebox.showinfo("Resultado", mensaje)
        self.master.destroy()

