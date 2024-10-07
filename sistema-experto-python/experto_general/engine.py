# experto_general/engine.py

from typing import List, Optional
from experto_general.base import BaseConocimientos
from experto_general.entry import Entry
from experto_general.property import Property
from experto_general.response import Response

class Engine:
    def __init__(self, base: BaseConocimientos):
        self.base = base
        self.accepted_properties: List[Property] = []
        self.denied_properties: List[Property] = []
        self.result: Optional[Entry] = None
        self.current_question: Optional[Property] = None
        self.current_entry: Optional[Entry] = None

    def set_base(self, base: BaseConocimientos):
        """Establece una nueva base de conocimientos para el motor."""
        self.base = base
        self.reset()

    def reset(self):
        """Reinicia el estado del motor para una nueva consulta."""
        self.accepted_properties = []
        self.denied_properties = []
        self.result = None
        self.current_question = None
        self.current_entry = None

    def get_next_question(self) -> Optional[Property]:
        """Determina y devuelve la siguiente propiedad a preguntar."""
        # Ordena las entradas por número de propiedades coincidentes
        sorted_entries = sorted(
            self.base.entries,
            key=lambda e: self._count_matching_properties(e),
            reverse=True
        )

        for entry in sorted_entries:
            if not self._check_rule_2(entry):
                continue
            if not self._check_rule_3(entry):
                continue

            self.current_entry = entry
            for prop in entry.properties:
                if not self._check_rule_1(prop):
                    continue
                self.current_question = prop
                return prop

        return None  # No hay más preguntas

    def set_response(self, response: Response):
        """Registra la respuesta del usuario y actualiza el estado."""
        if self.current_question is None:
            return

        if response == Response.YES:
            self.accepted_properties.append(self.current_question)
        elif response == Response.NO:
            self.denied_properties.append(self.current_question)
            # Descartar la entrada actual si contiene una propiedad negada
            if self.current_question in self.current_entry.properties:
                self.current_entry = None

        self.current_question = None  # Resetear la pregunta actual

    def evaluate(self) -> Optional[Entry]:
        """Evalúa si alguna entrada coincide con las propiedades aceptadas y denegadas."""
        # Busca la mejor coincidencia basada en las propiedades aceptadas
        best_match = None
        max_matches = -1

        for entry in self.base.entries:
            if not self._check_rule_2(entry):
                continue
            if not self._check_rule_3(entry):
                continue

            matches = self._count_matching_properties(entry)
            if matches > max_matches:
                max_matches = matches
                best_match = entry

        return best_match

    def _count_matching_properties(self, entry: Entry) -> int:
        """Cuenta cuántas propiedades de la entrada coinciden con las aceptadas."""
        return sum(1 for prop in entry.properties if prop in self.accepted_properties)

    def _check_rule_1(self, prop: Property) -> bool:
        """Regla 1: La propiedad no se ha preguntado antes"""
        return prop not in self.accepted_properties and prop not in self.denied_properties

    def _check_rule_2(self, entry: Entry) -> bool:
        """Regla 2: La entrada tiene todas las propiedades confirmadas"""
        for prop in self.accepted_properties:
            if prop not in entry.properties:
                return False
        return True

    def _check_rule_3(self, entry: Entry) -> bool:
        """Regla 3: La entrada no tiene ninguna propiedad rechazada"""
        for prop in self.denied_properties:
            if prop in entry.properties:
                return False
        return True
