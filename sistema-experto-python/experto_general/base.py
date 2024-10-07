# experto_general/base.py

import json
from typing import List
from experto_general.entry import Entry

JSON_LATEST = 1

class BaseConocimientos:
    def __init__(self):
        self.entries: List[Entry] = []
        self.description = "Base de Conocimientos"

    def from_json(self, filename: str):
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if data.get('__v') != JSON_LATEST:
            raise ValueError(f"Versión del JSON no soportada: {data.get('__v')}")
        
        self.description = data.get('description', self.description)
        for entry_data in data.get('entries', []):
            entry = self.get_or_add_entry(entry_data['name'])
            entry.description = entry_data.get('description', "")
            for prop_name in entry_data.get('props', []):
                entry.get_or_add_prop(prop_name)
        return self

    def to_json(self, filename: str):
        data = {
            '__v': JSON_LATEST,
            'description': self.description,
            'entries': []
        }
        for entry in self.entries:
            entry_dict = {
                'name': entry.name,
                'description': entry.description,
                'props': [prop.name for prop in entry.properties]
            }
            data['entries'].append(entry_dict)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return data

    def get_or_add_entry(self, name: str) -> Entry:
        for entry in self.entries:
            if entry.is_equal(name):
                return entry
        new_entry = Entry(name)
        self.entries.append(new_entry)
        return new_entry

    def __str__(self):
        result = f"[{self.description}]\n"
        for entry in self.entries:
            result += str(entry) + "\n"
        return result
