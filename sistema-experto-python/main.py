# main.py

import interfaz.menu as menu
from acciones import engine
from experto_general.base import BaseConocimientos
from experto_general.engine import Engine

def main():
    base_conocimientos = BaseConocimientos().from_json('trabajo_construcción.json')  # Actualiza la ruta según corresponda
    engine.set_base(base_conocimientos)  # Establece la base en el motor

    app = menu.Interfaz()
    app.mainloop()

if __name__ == '__main__':
    main()
