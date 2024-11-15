# test_duplicados.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import pandas as pd
from depuracion import duplicados

class TestDuplicados(unittest.TestCase):
    def test_duplicados(self):
        # Prueba para la detección de duplicados
        data = pd.DataFrame([
            {"Codigo": "001", "entrada/salida": 1, "rut": "123", "hora": 8, "minuto": 0, "día": 1},
            {"Codigo": "001", "entrada/salida": 1, "rut": "123", "hora": 8, "minuto": 0, "día": 1}
        ])
        # Crear la columna 'Hora' combinando 'hora' y 'minuto'
        data['Hora'] = data['hora'].astype(str).str.zfill(2) + ':' + data['minuto'].astype(str).str.zfill(2)
        
        result = duplicados(data)
        duplicados_detectados = result[result["Error"] == "Entrada duplicada"]
        self.assertEqual(len(duplicados_detectados), 1, "Debe detectar una entrada duplicada")

if __name__ == '__main__':
    unittest.main()

